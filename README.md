# GENESIS

**GENeralized-Ensemble SImulation System** - A molecular dynamics simulation software for biomolecular systems.

## Python Interface (genepie)

The `genepie` package provides a Python interface to GENESIS analysis tools and the ATDYN MD engine.

---

## For Users

### Installation

```bash
# From PyPI (coming soon)
pip install genepie

# Currently available from TestPyPI:
pip install -i https://test.pypi.org/simple/ genepie
```

**Requirements:**
- Python 3.9+
- Linux (x86_64) or macOS (arm64, x86_64)
- glibc 2.28+ for Linux (Ubuntu 20.04+)

### Quick Start

```python
from genepie import genesis_exe, SMolecule

# Load molecular structure
mol = SMolecule.from_file(pdbfile="protein.pdb", psffile="protein.psf")
print(f"Loaded {mol.num_atoms} atoms")

# Load trajectory and calculate RMSD
traj = genesis_exe.crd_convert(
    psffile="protein.psf",
    pdbfile="protein.pdb",
    dcdfile="trajectory.dcd",
    selection_group="an:CA",
)
rmsd = genesis_exe.rmsd_analysis(molecule=mol, trajectories=traj)
print(f"RMSD: {rmsd.mean():.2f} Å")

# Run MD simulation
energies, coords = genesis_exe.run_atdyn_md(
    prmtopfile="protein.prmtop",
    ambcrdfile="protein.inpcrd",
    nsteps=1000,
    ensemble="NVT",
    temperature=300.0,
)
```

### Testing Your Installation

Run basic tests to verify the installation:

```bash
python -m genepie.tests.test_rmsd
python -m genepie.tests.test_crd_convert
python -m genepie.tests.test_trj
python -m genepie.tests.test_rg
```

### Available Analysis Functions

- `crd_convert()` - Coordinate/trajectory conversion
- `trj_analysis()` - Distance, angle, dihedral analysis
- `rmsd_analysis()` - RMSD calculation
- `drms_analysis()` - Distance RMSD calculation
- `rg_analysis()` - Radius of gyration
- `msd_analysis()` - Mean squared displacement
- `diffusion_analysis()` - Diffusion coefficient calculation
- `hb_analysis()` - Hydrogen bond analysis
- `avecrd_analysis()` - Average coordinate calculation
- `wham_analysis()` - WHAM free energy analysis
- `mbar_analysis()` - MBAR free energy analysis
- `kmeans_clustering()` - K-means trajectory clustering

### MD Engine Functions

- `run_atdyn_md()` - Run MD simulation
- `run_atdyn_min()` - Run energy minimization
- `run_atdyn_md_isolated()` - Run MD in subprocess (crash-safe)
- `run_atdyn_min_isolated()` - Run minimization in subprocess

### Supported File Formats

| Format | Topology | Coordinates | Parameters |
|--------|----------|-------------|------------|
| AMBER | `prmtopfile` | `ambcrdfile` | (in prmtop) |
| GROMACS | `grotopfile` | `grocrdfile` | (in grotop) |
| CHARMM | `psffile` | `pdbfile`/`crdfile` | `parfile`, `strfile` |

---

## For Developers

### Installation from Source

```bash
# Clone repository
git clone https://github.com/matsunagalab/genesis.git
cd genesis

# Set up Python environment
python -m venv .venv
source .venv/bin/activate
pip install numpy

# Build GENESIS (requires gfortran)
autoreconf -fi
./configure --disable-mpi CC=gcc FC=gfortran
make -j$(nproc)

# Install in editable mode
pip install -e .
```

**macOS additional steps:**

```bash
# Install dependencies via Homebrew
brew install gcc lapack autoconf automake libtool

# Configure with Homebrew paths
./configure --disable-mpi CC=gcc-14 FC=gfortran \
    LAPACK_LIBS="-L$(brew --prefix lapack)/lib -llapack -lblas"
```

### Running Tests

```bash
# Run basic tests (18 tests)
cd src/genepie/tests
./all_run.sh

# Or run individual tests
python -m genepie.tests.test_rmsd
python -m genepie.tests.test_crd_convert
python -m genepie.tests.test_wham
```

**Integration tests (requires additional data download):**

```bash
# Download chignolin test data (~500 MB)
python -m genepie.tests.download_test_data

# Run integration tests (42 tests)
python -m genepie.tests.test_integration

# Run error handling tests (64 tests)
python -m genepie.tests.test_error_handling
```

**Optional dependencies for full test coverage:**

```bash
pip install mdtraj MDAnalysis  # For integration tests
pip install gdown              # For downloading test data
```

### Project Structure

```
genesis/
├── src/
│   ├── genepie/           # Python interface (main package)
│   │   ├── genesis_exe.py # Analysis function wrappers
│   │   ├── libloader.py   # Shared library loader
│   │   └── tests/         # Test files and data
│   ├── atdyn/             # MD engine
│   └── analysis/          # Analysis tools
├── CLAUDE.md              # Developer guide for Claude Code
└── pyproject.toml         # Package configuration
```

---

## Documentation

- [GENESIS Website](https://www.r-ccs.riken.jp/labs/cbrt/)
- [CLAUDE.md](CLAUDE.md) - Developer guide

## License

LGPL-3.0-or-later. See LICENSE file for details.
