#
import argparse
import pathlib

from ..TODO.TODO import main


def test_todo(mocker) -> None:
    cwd = pathlib.Path(__file__).parent.resolve()
    filename = "placeholder_filename"

    sys_args_debug = [filename, cwd, "-d", "true"]
    sys_args = [filename, cwd, "-v"]

    parser = argparse.ArgumentParser(
        prog="auto_todo",
        description="The VSC extension to create and push TODO lists to the list of issues in your git repo.",
        epilog="For instructions on the usage or for the contact information go to README.md",
    )

    parser.add_argument("filename")
    parser.add_argument("cwd")  # positional argument
    parser.add_argument(
        "-d",
        "--debug",
        help="Set to True for debugging, otherwise False.",
        default="False",
        choices=["False", "True", "T", "F", "true", "false", "t", "f"],
    )  # option that takes a value
    parser.add_argument("-v", "--verbose", action="store_true")  # on/off flag

    mocker.patch("sys.argv", return_value=sys_args_debug)
    main(arg_parser=parser)

    mocker.path("sys.argv", return_value=sys_args)
    main(arg_parser=parser)

    pass
