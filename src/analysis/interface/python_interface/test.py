import ctypes
import os
import pathlib
from libgenesis import LibGenesis
from s_molecule import SMolecule, py2c_s_molecule
from s_trajectories_c import STrajectoriesC
import py2c_util


def test():
    # 関数を呼び出す
    pdb_filename = pathlib.Path("molecule.pdb")
    with SMolecule.from_pdb_file(pdb_filename) as mol:
        # 結果を処理する
        print("num_atoms = ", mol.num_atoms)
        for i in range(max(0, mol.num_atoms - 5), mol.num_atoms):
            print(mol.atom_coord[i])
            print(mol.atom_no[i], mol.segment_name[i], mol.atom_name[i])

        print("num_atoms = ", mol.num_atoms)
        mol_c = py2c_s_molecule(mol)
        LibGenesis().lib.test_conv_c2f(ctypes.byref(mol_c))


def crd_convert(mol: SMolecule,
                trajectory_filename: str | bytes | os.PathLike,
                ctrl_filename: str | bytes | os.PathLike,
                traj_c: STrajectoriesC):
    mol_c = py2c_s_molecule(mol)
    LibGenesis().lib.crd_convert_c(
            ctypes.byref(mol_c),
            py2c_util.pathlike_to_byte(trajectory_filename),
            py2c_util.pathlike_to_byte(ctrl_filename),
            ctypes.byref(traj_c))
    LibGenesis().lib.deallocate_s_molecule_c(ctypes.byref(mol_c))


def test_crd():
    # 関数を呼び出す
    pdb_path = pathlib.Path(
            "../../../../tests/regression_test/test_analysis/trajectories/BPTI_charmm/BPTI_ionize.pdb")
    psf_path = pathlib.Path(
            "../../../../tests/regression_test/test_analysis/trajectories/BPTI_charmm/BPTI_ionize.psf")
    ctrl_path = pathlib.Path("./test_crd_inp")
            # "./test_crd_inp../../../../tests/regression_test/test_analysis/test_crd_convert/BPTI/inp")
    traj_path = pathlib.Path(
            "../../../../tests/regression_test/test_analysis/trajectories/BPTI_charmm/BPTI_run.dcd")
    traj_c = STrajectoriesC()
    with SMolecule.from_pdb_psf_file(pdb_path, psf_path) as mol:
        crd_convert(mol, traj_path, ctrl_path, traj_c)


if __name__ == "__main__":
    # test()
    test_crd()
