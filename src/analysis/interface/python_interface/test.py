import ctypes
import os
import pathlib
from libgenesis import LibGenesis
from s_molecule import SMolecule, py2c_s_molecule
from s_trajectories import STrajectoriesArray
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


def crd_convert(molecule: SMolecule,
                ctrl_filename: str | bytes | os.PathLike) -> STrajectoriesArray:
    buf = ctypes.c_void_p(None)
    num_trajs_c = ctypes.c_int(0)
    mol_c = py2c_s_molecule(molecule)
    LibGenesis().lib.crd_convert_c(
            ctypes.byref(mol_c),
            py2c_util.pathlike_to_byte(ctrl_filename),
            ctypes.byref(buf),
            ctypes.byref(num_trajs_c))
    LibGenesis().lib.deallocate_s_molecule_c(ctypes.byref(mol_c))
    return STrajectoriesArray(buf, num_trajs_c.value)


def test_crd():
    # 関数を呼び出す
    pdb_path = pathlib.Path(
            "../../../../tests/regression_test/test_analysis/trajectories/BPTI_charmm/BPTI_ionize.pdb")
    psf_path = pathlib.Path(
            "../../../../tests/regression_test/test_analysis/trajectories/BPTI_charmm/BPTI_ionize.psf")
    ctrl_path = pathlib.Path("./test_crd_inp")
            # "./test_crd_inp../../../../tests/regression_test/test_analysis/test_crd_convert/BPTI/inp")
    # traj_path = pathlib.Path(
    #         "../../../../tests/regression_test/test_analysis/trajectories/BPTI_charmm/BPTI_run.dcd")
    with SMolecule.from_pdb_psf_file(pdb_path, psf_path) as mol:
        with crd_convert(mol, ctrl_path) as trajs:
            pass


def trj_analysis(molecule: SMolecule, trajs :STrajectoriesArray,
                 ctrl_path: str | bytes | os.PathLike):
    mol_c = py2c_s_molecule(molecule)
    num_trajs = ctypes.c_int(len(trajs.traj_c_array))

    num_distance = ctypes.c_int(0)
    num = ctypes.c_int(0)
    result_distance = ctypes.c_void_p(None)

    LibGenesis().lib.trj_analysis_c(
            ctypes.byref(mol_c),
            trajs.src_c_obj,
            ctypes.byref(num_trajs),
            py2c_util.pathlike_to_byte(ctrl_path),
            ctypes.byref(result_distance),
            ctypes.byref(num_distance),
            ctypes.byref(num)
            )


def test_trj_analysis():
    # 関数を呼び出す
    pdb_path = pathlib.Path(
            "../../../../tests/regression_test/test_analysis/trajectories/BPTI_charmm/BPTI_ionize.pdb")
    psf_path = pathlib.Path(
            "../../../../tests/regression_test/test_analysis/trajectories/BPTI_charmm/BPTI_ionize.psf")
    crd_ctrl_path = pathlib.Path("./test_crd_inp")
    trj_analysis_ctrl_path = pathlib.Path("./test_trj_analysis_inp")

    with SMolecule.from_pdb_psf_file(pdb_path, psf_path) as mol:
        with crd_convert(mol, crd_ctrl_path) as trajs:
            trj_analysis(mol, trajs, trj_analysis_ctrl_path)


if __name__ == "__main__":
    # test()
    test_crd()
    # test_trj_analysis()
