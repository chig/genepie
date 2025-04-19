import os
import pathlib
import unittest
from typing import Optional, Union
import numpy as np
from ctrl_files import TrajectoryParameters
import genesis_exe
from s_molecule import SMolecule
from s_trajectories import STrajectories, STrajectoriesArray


class CustomTestCase(unittest.TestCase):
    """"""
    TEST_ROOT = pathlib.Path("../../../../tests/regression_test")
    PDB_PATH = pathlib.Path("BPTI_ionize.pdb")
    PSF_PATH = pathlib.Path("BPTI_ionize.psf")
    TRJ_PATH = pathlib.Path("BPTI_run.dcd")

    def assertAlmostEqualNumpyNDArray(
            self, expected, actual,
            rtol: Optional[float] = None,
            atol: Optional[float] = None,
            msg: Optional[str] = None,
            ):
        if rtol is None:
            rtol = 1.e-7
        if atol is None:
            atol = 0
        if not np.allclose(expected, actual, rtol=rtol, atol=atol):
            standard_msg = (f"{expected}.coords != {actual}.coords "
                            + f"within rtol={rtol}, atol={atol}")
            self.fail(self._formatMessage(msg, standard_msg))

    def assertAlmostEqualSTrajectories(
            self, e_trj: STrajectories, a_trj: STrajectories,
            places: Optional[int] = None,
            msg: Optional[str] = None,
            delta: Optional[float] = None):
        if (places is None) and (delta is None):
            places = 4
        if (not isinstance(e_trj, STrajectories)
            or not isinstance(a_trj, STrajectories)):
            self.fail("Both arguments must be instances of STrajectories.")
        self.assertEqual(e_trj.natom, a_trj.natom, msg)
        self.assertEqual(e_trj.nframe, a_trj.nframe, msg)
        self.assertAlmostEqual(
                e_trj.coords, a_trj.coords, places, msg, delta)
        self.assertAlmostEqual(
                e_trj.pbc_boxes, a_trj.pbc_boxes, places, msg, delta)

    def assertAlmostEqualSMolecule(
            self, e_mol: STrajectories, a_mol: STrajectories,
            places: Optional[int] = None,
            msg: Optional[str] = None,
            delta: Optional[float] = None):
        if (places is None) and (delta is None):
            places = 4
        self.assertEqual(e_mol.num_deg_freedom, a_mol.num_deg_freedom, msg)
        self.assertEqual(e_mol.num_atoms, a_mol.num_atoms, msg)
        self.assertEqual(e_mol.num_bonds, a_mol.num_bonds, msg)
        self.assertEqual(e_mol.num_enm_bonds, a_mol.num_enm_bonds, msg)
        self.assertEqual(e_mol.num_angles, a_mol.num_angles, msg)
        self.assertEqual(e_mol.num_dihedrals, a_mol.num_dihedrals, msg)
        self.assertEqual(e_mol.num_impropers, a_mol.num_impropers, msg)
        # ...

    def assertAlmostEqual(self, expected, actual,
                          places: Optional[int] = None,
                          msg: Optional[str] = None,
                          delta: Optional[float] = None):
        if isinstance(expected, np.ndarray) and isinstance(actual, np.ndarray):
            if delta is None:
                if places is not None:
                    atol = 10**(-places)
                else:
                    atol = None
            else:
                atol = delta
            if (expected.dtype == np.float64) and (actual.dtype == np.float64):
                self.assertAlmostEqualNumpyNDArray(
                        expected, actual, rtol=0.0, atol=atol, msg=msg)
                return
        elif (isinstance(expected, STrajectories)
              and isinstance(actual, STrajectories)):
            self.assertAlmostEqualSTrajectories(
                    expected, actual, places, msg, delta)
            return
        elif (isinstance(expected, SMolecule)
              and isinstance(actual, SMolecule)):
            self.assertAlmostEqualSMolecule(
                    expected, actual, places, msg, delta)
            return
        if (places is None) and (delta is None):
            places = 7
        super().assertAlmostEqual(
                expected, actual, places, msg, delta)

    @staticmethod
    def create_traj_by_genesis(
            dcd: Union[str, bytes, os.PathLike],
            pdb: Union[str, bytes, os.PathLike] = '',
            top: Union[str, bytes, os.PathLike] = '',
            gpr: Union[str, bytes, os.PathLike] = '',
            psf: Union[str, bytes, os.PathLike] = '',
            ref: Union[str, bytes, os.PathLike] = '',
            fit: Union[str, bytes, os.PathLike] = '',
            prmtop: Union[str, bytes, os.PathLike] = '',
            ambcrd: Union[str, bytes, os.PathLike] = '',
            ambref: Union[str, bytes, os.PathLike] = '',
            grotop: Union[str, bytes, os.PathLike] = '',
            grocrd: Union[str, bytes, os.PathLike] = '',
            groref: Union[str, bytes, os.PathLike] = '',
            ) \
            -> tuple[STrajectoriesArray, SMolecule]:
        mol = SMolecule.from_file(
                pdb=pdb, top=top, gpr=gpr, psf=psf, ref=ref, fit=fit,
                prmtop=prmtop, ambcrd=ambcrd, ambref=ambref,
                grotop=grotop, grocrd=grocrd, groref=groref)
        trajs = genesis_exe.crd_convert(
                mol,
                traj_params = [
                    TrajectoryParameters(
                        trjfile = dcd,
                        md_step = 10,
                        mdout_period = 1,
                        ana_period = 1,
                        repeat = 1,
                        ),
                    ],
                trj_format = "DCD",
                trj_type = "COOR+BOX",
                trj_natom = 0,
                selection_group = ["all", ],
                fitting_method = "NO",
                fitting_atom = 1,
                check_only = False,
                pbc_correct = "NO",
                )
        return (trajs, mol)
