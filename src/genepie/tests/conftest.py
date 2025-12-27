"""Test configuration and shared fixtures for genepie tests."""
import pathlib

# Test data directory
TEST_DIR = pathlib.Path(__file__).parent
DATA_DIR = TEST_DIR / "data"

# BPTI system paths
BPTI_PDB = DATA_DIR / "bpti" / "BPTI_ionize.pdb"
BPTI_PSF = DATA_DIR / "bpti" / "BPTI_ionize.psf"
BPTI_DCD = DATA_DIR / "bpti" / "BPTI_run.dcd"

# RALP-DPPC system paths
RALP_PDB = DATA_DIR / "ralp_dppc" / "RALP_DPPC_run.pdb"
RALP_PSF = DATA_DIR / "ralp_dppc" / "RALP_DPPC.psf"
RALP_DCD = DATA_DIR / "ralp_dppc" / "RALP_DPPC_run.dcd"

# Chignolin system paths (for integration tests - downloaded from Google Drive)
CHIGNOLIN_PDB = DATA_DIR / "chignolin" / "chignolin.pdb"
CHIGNOLIN_PSF = DATA_DIR / "chignolin" / "chignolin.psf"
CHIGNOLIN_DCD = DATA_DIR / "chignolin" / "chignolin.dcd"

# Other test data
MOLECULE_PDB = DATA_DIR / "molecule.pdb"
MSD_DATA = DATA_DIR / "msd.data"
