import os
import pathlib
import genesis_exe


def test_wham_analysis():
    ctrl_path = pathlib.Path("test_wham_analysis_inp")
    genesis_exe.wham_analysis(ctrl_path)


def main():
    if os.path.exists("out"):
        os.remove("out")
    test_wham_analysis()


if __name__ == "__main__":
    main()
