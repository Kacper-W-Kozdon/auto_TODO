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
        print(f"Removing {todo_md_path=}")
        os.remove(todo_md_path)
        print(f"File '{todo_md_path}' deleted successfully.")
    else:
        print(f"File '{todo_md_path}' not found.")

    if os.path.exists(todo_txt_path) and "tests" in todo_txt_path:
        print(f"Removing {todo_txt_path=}")
        os.remove(todo_txt_path)
        print(f"File '{todo_txt_path}' deleted successfully.")
    else:
        print(f"File '{todo_txt_path}' not found.")

    filename = "placeholder_filename"

    sys_args_debug = [filename, str(cwd), "-d", "true"]

    sys_args_debug_dict = {"filename": filename, "cwd": str(cwd), "debug": "true"}

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
    parser.add_argument(
        "-p",
        "--project_name",
        default="Project",
        help="The name of the project displayed as the title of the list.",
    )
    parser.add_argument(
        "-ln",
        "--list_name",
        default="TODO list",
        help="The header preceeding the list.",
    )
    parser.add_argument(
        "-e",
        "--excluded",
        nargs="+",
        help="Files and path to exclude, matched using regex rules.",
    )

    mocker.patch("sys.argv", sys_args_debug)
    test_ret = main(arg_parser=parser)

    assert test_ret[0] == "Debugging message ends here.", "Debugging argparse failed."

    ret_args_dict = test_ret[1].__dict__.items()

    for item in sys_args_debug_dict.items():
        assert item in ret_args_dict

    assert os.path.exists(todo_md_path), "TODO.md failed to be created."
    assert os.path.exists(todo_txt_path), "TODO.txt failed to be created."


def test_todo_main(mocker) -> None:
    cwd = pathlib.Path(__file__).parent.resolve()
    filename = "placeholder_filename"
    project_name = "Test"
    list_name = "Test_list"

    sys_args = [
        filename,
        str(cwd),
        "--project_name",
        project_name,
        "--list_name",
        list_name,
    ]
    sys_args_dict = {
        "filename": filename,
        "cwd": str(cwd),
        "project_name": project_name,
        "list_name": list_name,
    }

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
    parser.add_argument("-v", "--verbose", action="store_false")  # on/off flag
    parser.add_argument(
        "-p",
        "--project_name",
        default="Project",
        help="The name of the project displayed as the title of the list.",
    )
    parser.add_argument(
        "-ln",
        "--list_name",
        default="TODO list",
        help="The header preceeding the list.",
    )
    parser.add_argument(
        "-e",
        "--excluded",
        nargs="+",
        help="Files and path to exclude, matched using regex rules.",
    )

    mocker.patch("sys.argv", sys_args)
    test_ret = main(arg_parser=parser)
    ret_args_dict = test_ret[1].__dict__.items()

    assert f"TODO list for {project_name=} successfully created." == test_ret[0]
    for item in sys_args_dict.items():
        assert item in ret_args_dict
