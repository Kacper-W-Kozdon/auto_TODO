#
import argparse
import os
import pathlib

from ..TODO.TODO import main


def test_todo_debug(mocker) -> None:
    cwd = pathlib.Path(__file__).parent.resolve()
    todo_md_path = f"{cwd}\\TODO.md"
    todo_txt_path = f"{cwd}\\TODO.txt"

    if os.path.exists(todo_md_path) and "tests" in todo_md_path:
        os.remove(todo_md_path)
        print(f"File '{todo_md_path}' deleted successfully.")
    else:
        print(f"File '{todo_md_path}' not found.")

    if os.path.exists(todo_txt_path) and "tests" in todo_txt_path:
        os.remove(todo_txt_path)
        print(f"File '{todo_txt_path}' deleted successfully.")
    else:
        print(f"File '{todo_txt_path}' not found.")

    filename = "placeholder_filename"

    sys_args_debug = [filename, cwd, "-d", "true"]

    sys_args_debug_dict = {"filename": filename, "cwd": cwd, "debug": "true"}

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
    test_ret = main(arg_parser=parser)

    assert test_ret[0] == "Debugging message ends here.", "Debugging argparse failed."

    ret_args_dict = dir(test_ret[1]).items()

    for item in sys_args_debug_dict.items():
        assert item in ret_args_dict

    assert os.path.exists(todo_md_path), "TODO.md failed to be created."
    assert os.path.exists(todo_txt_path), "TODO.txt failed to be created."


def test_todo_main(mocker) -> None:
    cwd = pathlib.Path(__file__).parent.resolve()
    filename = "placeholder_filename"

    sys_args = [filename, cwd, "-v", "--proj_name", "Test", "--list_name", "Test list"]

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

    mocker.path("sys.argv", return_value=sys_args)
    main(arg_parser=parser)
