"""
Backward compatibility wrapper for genepy -> genepie.
Please use 'import genepie' instead of 'import genepy'.
"""
import warnings
warnings.warn(
    "genepy is deprecated, use 'import genepie' instead",
    DeprecationWarning,
    stacklevel=2
)

from genepie import (
    SMolecule,
    STrajectories,
    STrajectoriesArray,
    genesis_exe,
    LibGenesis,
    ctrl_files,
)

__all__ = [
    "SMolecule",
    "STrajectories",
    "STrajectoriesArray",
    "genesis_exe",
    "LibGenesis",
    "ctrl_files",
]
