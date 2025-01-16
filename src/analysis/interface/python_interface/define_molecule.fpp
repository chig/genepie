module define_molecule
  use, intrinsic :: iso_c_binding
  use input_mod
  use molecules_mod
  use fileio_pdb_mod
  use constants_mod      ! Likely contains MaxFilename
  use molecules_str_mod  ! Contains s_molecule definition
  use s_molecule_c_mod
  implicit none

  private
  public :: define_molecule_from_pdb

  ! Define MaxFilename if it"s not available from constants_mod
  integer, parameter :: MaxFilename = 256  ! Adjust this value as needed

contains
  subroutine define_molecule_from_pdb(pdb_filename, out_mol) &
      bind(C, name="define_molecule_from_pdb")
    use conv_f_c_util
    implicit none
    ! Input parameters
    character(kind=c_char), intent(in) :: pdb_filename(*)
    ! Output parameters
    type(s_molecule_c), intent(out) :: out_mol
    ! Local variables
    type(s_inp_info) :: inp_info
    type(s_pdb) :: pdb
    type(s_molecule) :: molecule
    character(MaxFilename) :: filename

    call c2f_string(pdb_filename, filename)
    inp_info%pdbfile = trim(filename)
    call input_files(inp_info, pdb=pdb)
    call define_molecules(molecule, pdb=pdb)
    call f2c_s_molecule(molecule, out_mol)
  end subroutine define_molecule_from_pdb

end module define_molecule
