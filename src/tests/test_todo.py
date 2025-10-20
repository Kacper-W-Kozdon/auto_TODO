#
import pathlib


def test_todo(mocker) -> None:
    cwd = pathlib.Path(__file__).parent.resolve()
    filename = "placeholder_filename"

    sys_args_debug = [filename, cwd, "-d", "true"]
    sys_args = [filename, cwd, "-v"]

    mocker.patch("sys.argv", return_value=sys_args_debug)

    mocker.path("sys.argv", return_value=sys_args)
    pass
