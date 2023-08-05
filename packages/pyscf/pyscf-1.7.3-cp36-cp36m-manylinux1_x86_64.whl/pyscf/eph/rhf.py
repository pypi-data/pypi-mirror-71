#!/usr/bin/env python
# Copyright 2014-2020 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Yang Gao <younggao1994@gmail.com>

#
'''
Analytical electron-phonon matrix for restricted hartree fock
'''
import numpy as np
from pyscf.hessian import rhf
from pyscf.lib import logger
import time
from pyscf import lib
import scipy
from pyscf.scf._response_functions import _gen_rhf_response

AU_TO_CM = 2.19475 * 1e5
CUTOFF_FREQUENCY = 80

def kernel(ephobj, mo_energy=None, mo_coeff=None, mo_occ=None, mo_rep=False):
    cput0 = (time.clock(), time.time())
    if mo_energy is None: mo_energy = ephobj.base.mo_energy
    if mo_coeff is None: mo_coeff = ephobj.base.mo_coeff
    if mo_occ is None: mo_occ = ephobj.base.mo_occ

    de = ephobj.hess_elec(mo_energy, mo_coeff, mo_occ)
    ephobj.de = de + ephobj.hess_nuc(ephobj.mol)

    omega, vec = ephobj.get_mode(ephobj.mol, ephobj.de)
    ephobj.omega, ephobj.vec = omega, vec
    ephobj.eph = ephobj.get_eph(ephobj.chkfile, omega, vec, mo_rep)
    return ephobj.eph, ephobj.omega

def solve_hmat(mol, hmat, CUTOFF_FREQUENCY=CUTOFF_FREQUENCY):
    log = logger.new_logger(mol, mol.verbose)
    mass = mol.atom_mass_list() * 1836.15
    natom = len(mass)
    h = np.empty_like(hmat) #[atom, axis, atom, axis]
    for i in range(natom):
        for j in range(natom):
            h[i,j] = hmat[i,j] / np.sqrt(mass[i]*mass[j])
    forcemat = h.transpose(0,2,1,3).reshape(natom*3, natom*3)
    forcemat[abs(forcemat)<1e-12]=0 #improve stability
    w, c = scipy.linalg.eig(forcemat)
    idx = np.argsort(w)[::-1] # sort the mode of the frequency
    w = w[idx]
    c = c[:,idx]
    w_au = w**0.5
    w_au = w_au.real
    w_cm = w_au * AU_TO_CM
    log.info('****Eigenmodes(cm-1)****')
    for i, omega in enumerate(w_cm):
        if omega > CUTOFF_FREQUENCY:
            log.info("Mode %i Omega=%.3f", i, omega)
        else:
            log.info("Mode %i Omega=%.3f, Mode filtered out", i, omega)
    idx = np.where(w_cm>CUTOFF_FREQUENCY)[0]
    w_new = w_au[idx]
    c_new = c[:,idx]
    log.info('****Remaining Eigenmodes(cm-1)****')
    for i, omega in enumerate(w_cm[idx]):
        log.info("Mode %i Omega=%.3f", i, omega)
    return w_new, c_new


def get_mode(ephobj, mol=None, de=None):
    if mol is None: mol = ephobj.mol
    if de is None:
        if ephobj.de is None:
            de = ephobj.hess_elec() + ephobj.hess_nuc()
        else:
            de = ephobj.de
    return solve_hmat(mol, de, ephobj.CUTOFF_FREQUENCY)


def rhf_deriv_generator(mf, mo_coeff, mo_occ):
    nao, nmo = mo_coeff.shape
    mocc = mo_coeff[:,mo_occ>0]
    nocc = mocc.shape[1]
    vresp = _gen_rhf_response(mf, mo_coeff, mo_occ, hermi=1)
    def fx(mo1):
        mo1 = mo1.reshape(-1,nmo,nocc)
        nset = len(mo1)
        dm1 = np.empty((nset,nao,nao))
        for i, x in enumerate(mo1):
            dm = np.dot(x*2, mocc.T) # *2 for double occupancy
            dm1[i] = dm + dm.T
        v1 = vresp(dm1)
        return v1
    return fx

def vnuc_generator(ephobj, mol):
    if mol is None: mol = ephobj.mol
    aoslices = mol.aoslice_by_atom()
    def vnuc_deriv(atm_id):
        shl0, shl1, p0, p1 = aoslices[atm_id]
        with mol.with_rinv_at_nucleus(atm_id):
            vrinv = mol.intor('int1e_iprinv', comp=3) # <\nabla|1/r|>
            vrinv *= -mol.atom_charge(atm_id)
        return vrinv + vrinv.transpose(0,2,1)
    return vnuc_deriv

def get_eph(ephobj, mo1, omega, vec, mo_rep):
    if isinstance(mo1, str):
        mo1 = lib.chkfile.load(mo1, 'scf_mo1')
        mo1 = dict([(int(k), mo1[k]) for k in mo1])

    mol = ephobj.mol
    mf = ephobj.base
    vnuc_deriv = ephobj.vnuc_generator(mol)
    aoslices = mol.aoslice_by_atom()
    vind = rhf_deriv_generator(mf, mf.mo_coeff, mf.mo_occ)
    mocc = mf.mo_coeff[:,mf.mo_occ>0]
    dm0 = np.dot(mocc, mocc.T) * 2

    natoms = mol.natm
    nao = mol.nao_nr()

    vcore = []
    for ia in range(natoms):
        h1 = vnuc_deriv(ia)
        v1 = vind(mo1[ia])
        shl0, shl1, p0, p1 = aoslices[ia]
        shls_slice = (shl0, shl1) + (0, mol.nbas)*3
        vj1, vk1= rhf._get_jk(mol, 'int2e_ip1', 3, 's2kl',
                                     ['ji->s2kl', -dm0[:,p0:p1],  # vj1
                                      'li->s1kj', -dm0[:,p0:p1]], # vk1
                                     shls_slice=shls_slice)
        vhf = vj1 - vk1*.5
        vtot = h1 + v1 + vhf + vhf.transpose(0,2,1)
        vcore.append(vtot)
    vcore = np.asarray(vcore).reshape(-1,nao,nao)
    mass = mol.atom_mass_list() * 1836.15
    nmodes, natoms = len(omega), len(mass)
    vec = vec.reshape(natoms, 3, nmodes)
    for i in range(natoms):
        for j in range(nmodes):
            vec[i,:,j] /= np.sqrt(2*mass[i]*omega[j])
    vec = vec.reshape(3*natoms,nmodes)
    mat = np.einsum('xJ,xuv->Juv', vec, vcore)
    if mo_rep:
        mat = np.einsum('Juv,up,vq->Jpq', mat, mf.mo_coeff.conj(), mf.mo_coeff, optimize=True)
    return mat


class EPH(rhf.Hessian):
    def __init__(self, scf_method):
        rhf.Hessian.__init__(self, scf_method)
        self.CUTOFF_FREQUENCY=CUTOFF_FREQUENCY

    get_mode = get_mode
    get_eph = get_eph
    vnuc_generator = vnuc_generator
    kernel = kernel

if __name__ == '__main__':
    from pyscf import gto, scf

    mol = gto.M()
    mol.atom = [['O', [0.000000000000,  -0.000000000775,   0.923671924285]],
                ['H', [-0.000000000000,  -1.432564848017,   2.125164039823]],
                ['H', [0.000000000000,   1.432564848792,   2.125164035930]]]
    mol.unit = 'Bohr'
    mol.basis = 'sto3g'
    mol.verbose=4
    mol.build() # this is a pre-computed relaxed geometry

    mf = scf.RHF(mol)
    mf.conv_tol = 1e-16
    mf.conv_tol_grad = 1e-10
    mf.kernel()

    myeph = EPH(mf)

    grad = mf.nuc_grad_method().kernel()
    print("Force on the atoms/au:")
    print(grad)

    eph, omega = myeph.kernel(mo_rep=True)
    print(np.amax(eph))
