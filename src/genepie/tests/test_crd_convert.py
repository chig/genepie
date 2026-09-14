import numpy as np
import pytest
from .conftest import BPTI_PDB, BPTI_PSF, BPTI_DCD
from ..s_molecule import SMolecule
from .. import genesis_exe


def test_crd_convert_basic():
    """Test basic trajectory loading without fitting."""
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    trajs, subset_mol = genesis_exe.crd_convert(
        mol,
        trj_files=[str(BPTI_DCD)],
        trj_format="DCD",
        trj_type="COOR+BOX",
    )

    assert len(trajs) == 1
    traj = trajs[0]
    assert traj.nframe > 0
    assert traj.natom == mol.num_atoms
    assert traj.coords.shape == (traj.nframe, traj.natom, 3)
    print(f"  Loaded {traj.nframe} frames, {traj.natom} atoms")


def test_crd_convert_with_selection():
    """Test trajectory loading with atom selection."""
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    trajs, subset_mol = genesis_exe.crd_convert(
        mol,
        trj_files=[str(BPTI_DCD)],
        trj_format="DCD",
        trj_type="COOR+BOX",
        selection="an:CA",
    )

    assert len(trajs) == 1
    traj = trajs[0]
    assert traj.nframe > 0
    # Subset should have fewer atoms
    assert traj.natom == subset_mol.num_atoms
    assert traj.natom < mol.num_atoms
    print(f"  Selected {traj.natom} CA atoms from {mol.num_atoms} total atoms")


def test_crd_convert_with_fitting():
    """Test trajectory loading with TR+ROT fitting."""
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    trajs, subset_mol = genesis_exe.crd_convert(
        mol,
        trj_files=[str(BPTI_DCD)],
        trj_format="DCD",
        trj_type="COOR+BOX",
        selection="an:CA",
        fitting_selection="an:CA",
        fitting_method="TR+ROT",
    )

    assert len(trajs) == 1
    traj = trajs[0]
    assert traj.nframe > 0
    assert traj.natom == subset_mol.num_atoms
    # Check coordinates are reasonable (not NaN/Inf)
    assert np.all(np.isfinite(traj.coords))
    print(f"  Fitted trajectory with {traj.nframe} frames")


def test_crd_convert_with_centering():
    """Test trajectory loading with centering."""
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    trajs, subset_mol = genesis_exe.crd_convert(
        mol,
        trj_files=[str(BPTI_DCD)],
        trj_format="DCD",
        trj_type="COOR+BOX",
        selection="an:CA",
        centering=True,
        center_coord=(0.0, 0.0, 0.0),
    )

    assert len(trajs) == 1
    traj = trajs[0]
    # Check that coordinates are centered (COM near origin)
    com = np.mean(traj.coords, axis=1)  # COM per frame
    # COM should be near (0, 0, 0) for each frame
    assert np.allclose(com, 0.0, atol=5.0)  # Allow 5 Angstrom tolerance
    print(f"  Centered trajectory with {traj.nframe} frames")


def test_crd_convert_info():
    """Test crd_convert_info function."""
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    info = genesis_exe.crd_convert_info(
        mol,
        trj_files=[str(BPTI_DCD)],
        trj_format="DCD",
        trj_type="COOR+BOX",
    )

    assert len(info.frame_counts) == 1
    assert info.frame_counts[0] > 0
    print(f"  Trajectory info: {info.frame_counts[0]} frames")


def test_crd_convert_dcd_coor_without_box():
    """trj_type="COOR" must not crash (regression: NULL box buffer)."""
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    trajs, subset_mol = genesis_exe.crd_convert(
        mol,
        trj_files=[str(BPTI_DCD)],
        trj_format="DCD",
        trj_type="COOR",
        selection="an:CA",
    )
    traj = trajs[0]
    assert traj.nframe > 0
    assert traj.natom == subset_mol.num_atoms
    assert traj.coords.shape == (traj.nframe, traj.natom, 3)
    assert np.all(traj.pbc_boxes == 0.0)


def test_crd_convert_single_pdb_as_one_frame():
    """A single-structure PDB is read as a one-frame trajectory."""
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    for trj_type in ("COOR", "COOR+BOX"):
        trajs, subset_mol = genesis_exe.crd_convert(
            mol,
            trj_files=[str(BPTI_PDB)],
            trj_format="PDB",
            trj_type=trj_type,
            selection="an:CA",
        )
        assert len(trajs) == 1
        traj = trajs[0]
        assert traj.nframe == 1
        assert traj.natom == subset_mol.num_atoms
        idx = genesis_exe.selection(mol, "an:CA") - 1
        np.testing.assert_allclose(traj.coords[0], mol.atom_coord[idx])
        box = np.diag(traj.pbc_boxes[0])
        if trj_type == "COOR+BOX":
            # CRYST1 record of BPTI_ionize.pdb
            np.testing.assert_allclose(box, [69.836, 82.285, 68.100])
        else:
            assert np.all(box == 0.0)


def _write_multi_model_pdb(path, molecule, traj):
    """Write traj as a MODEL/ENDMDL PDB in the layout of write_pdb_trj."""
    with open(path, "w") as f:
        for k in range(traj.nframe):
            b = np.diag(traj.pbc_boxes[k])
            f.write(f"CRYST1{b[0]:9.3f}{b[1]:9.3f}{b[2]:9.3f}"
                    "  90.00  90.00  90.00 P 1           1\n")
            f.write(f"MODEL     {k + 1:4d}\n")
            for i in range(traj.natom):
                x, y, z = traj.coords[k, i]
                atom_name = str(molecule.atom_name[i]).strip()[:4]
                res_name = str(molecule.residue_name[i]).strip()[:4]
                f.write(f"ATOM  {i + 1:5d}  {atom_name:<4s}{res_name:<4s}"
                        f"X{int(molecule.residue_no[i]):4d}    "
                        f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00  0.00\n")
            f.write("TER\nENDMDL\n")
        f.write("END\n")


def test_crd_convert_multi_model_pdb_matches_dcd(tmp_path):
    """MODEL/ENDMDL frames are counted and read like the DCD they came from."""
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    dcd_trajs, subset_mol = genesis_exe.crd_convert(
        mol,
        trj_files=[str(BPTI_DCD)],
        trj_format="DCD",
        trj_type="COOR+BOX",
        selection="an:CA",
    )
    ref = dcd_trajs[0]
    assert ref.nframe > 1

    pdb_path = tmp_path / "multi.pdb"
    _write_multi_model_pdb(pdb_path, subset_mol, ref)

    pdb_trajs, _ = genesis_exe.crd_convert(
        subset_mol,
        trj_files=[str(pdb_path)],
        trj_format="PDB",
        trj_type="COOR+BOX",
    )
    got = pdb_trajs[0]
    assert got.nframe == ref.nframe
    np.testing.assert_allclose(got.coords, ref.coords, atol=1e-3)
    np.testing.assert_allclose(got.pbc_boxes, ref.pbc_boxes, atol=1e-3)

    # ana_period applies to PDB frames as well
    sub_trajs, _ = genesis_exe.crd_convert(
        subset_mol,
        trj_files=[str(pdb_path)],
        trj_format="PDB",
        trj_type="COOR",
        ana_period=2,
    )
    assert sub_trajs[0].nframe == ref.nframe // 2
    np.testing.assert_allclose(sub_trajs[0].coords, ref.coords[1::2], atol=1e-3)


def test_crd_convert_pdb_without_atoms_raises(tmp_path):
    """A PDB with no ATOM records has zero frames and must be rejected."""
    from ..exceptions import GenesisError
    pdb_path = tmp_path / "empty.pdb"
    pdb_path.write_text("REMARK nothing here\nEND\n")
    mol = SMolecule.from_file(pdb=BPTI_PDB, psf=BPTI_PSF)
    with pytest.raises(GenesisError):
        genesis_exe.crd_convert(
            mol,
            trj_files=[str(pdb_path)],
            trj_format="PDB",
            trj_type="COOR",
        )
