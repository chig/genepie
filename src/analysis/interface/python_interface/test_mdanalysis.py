import pathlib
import unittest
from s_trajectories import STrajectories
import MDAnalysis as mda


class TestMDTraj(unittest.TestCase):

    def test_from_mdanalysis_universe(self):
        pdb_path = pathlib.Path("BPTI_ionize.pdb")
        uni = mda.Universe(pdb_path)
        # uni.atoms.guess_bonds()
        trj, mol = STrajectories.from_mdanalysis_universe(uni)
        with trj:
            pass


if __name__ == "__main__":
    unittest.main()
