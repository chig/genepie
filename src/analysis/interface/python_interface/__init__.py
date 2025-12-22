"""
GENESIS Python Interface

This module is deprecated. Please use 'import genepie' instead.
This wrapper is provided for backward compatibility only.
"""
import warnings
warnings.warn(
    "python_interface is deprecated, use 'import genepie' instead",
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
    GenesisError,
    GenesisFortranError,
    GenesisValidationError,
    GenesisMemoryError,
    GenesisOverflowError,
)

__version__ = "1.0.0"
__all__ = [
    "SMolecule",
    "STrajectories",
    "STrajectoriesArray",
    "genesis_exe",
    "LibGenesis",
    "ctrl_files",
    "GenesisError",
    "GenesisFortranError",
    "GenesisValidationError",
    "GenesisMemoryError",
    "GenesisOverflowError",
]
