import argparse
import copy
import os
import pathlib
import sys
from typing import Union

import requests.sessions
from dotenv import load_dotenv
from requests import ConnectionError, Request, Session


class Passed_Args:
    pass


def markdown_body(
    url: str,
    headers: dict[str, str],
    session: requests.sessions.Session,
    body_list: list[str],
) -> str:
    ret = ""
    for body in body_list:
        data = '{"text": ""}'
        # print(body)
        data = data.replace('"text": ""', f'"text": "{body}"')

        markdown = Request("POST", url, headers=headers, data=data)
        prepped_markdown = markdown.prepare()
        resp = session.send(prepped_markdown)
        ret += resp.text
    ret = ret.replace("\n", "")
    ret = ret.replace('"', "'")
    return ret


def update_TODO(
    url: str, headers: dict[str, str], session: requests.sessions.Session, body: str
) -> None:
    print("---Updating TODO---\n")
    auth_headers = copy.copy(headers)
    # test_body = "<div><h1 class='heading-element'>SLAB Project</h1></div>"
    data = '{"title": "TODO", "body": "", "state": "open"}'
    data = data.replace('"body": ""', f'"body": "{body}"')
    print(data)

    patch = Request("PATCH", url, headers=auth_headers, data=data)
    prepped_patch = patch.prepare()
    resp = session.send(prepped_patch)
    if str(resp.status_code) != "200":
        raise ConnectionError(
            f"Failed to update TODO with {resp.status_code=}.",
            request=prepped_patch,
            response=resp,
        )

    print("SUCCESS")


def create_TODO(
    url: str, headers: dict[str, str], session: requests.sessions.Session, body: str
) -> None:
    print("---Creating TODO---\n")
    auth_headers = copy.copy(headers)
    data = '{"title": "TODO", "body": "", "state": "open"}'
    data = data.replace('"body": ""', f'"body": "{body}"')

    create = Request("POST", url, headers=auth_headers, data=data)
    prepped_create = create.prepare()
    resp = session.send(prepped_create)
    if str(resp.status_code) != "200":
        raise ConnectionError(
            f"Failed to create TODO with {resp.status_code=}.",
            request=prepped_create,
            response=resp,
        )

    print("SUCCESS")


def main(arg_parser: argparse.ArgumentParser) -> None:
    load_dotenv()
    passed_args = Passed_Args()
    sys_args = copy.copy(sys.argv)

    arg_parser.parse_args(args=sys_args, namespace=passed_args)
    todo_body = []

    root = pathlib.Path(__file__).parent.resolve()
    print(root)

    with open(f"{root}\\TODO.md", "r") as todo_file:
        for line in todo_file:
            line = line.replace("\n", "")
            line = line.replace("\\", "")
            line = line.replace('"', "'")
            todo_body.append(line)

    token = os.getenv("TOKEN")

    url = "https://api.github.com/repos/Kacper-W-Kozdon/slab/issues/1"
    markdown_url = "https://api.github.com/markdown"

    authorize_headers: dict[str, str] = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    markdown_headers: dict[str, str] = {
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "text/html",
        "Authorization": f"Bearer {token}",
    }

    markdown_data = todo_body

    session = Session()

    get = Request("GET", url, headers=authorize_headers)
    prepped = get.prepare()
    response = session.send(prepped)

    print(markdown_body(markdown_url, markdown_headers, session, markdown_data))

    if response.json().get("id") is not None:
        body = markdown_body(markdown_url, markdown_headers, session, markdown_data)
        update_TODO(url, authorize_headers, session, body)
    else:
        body = markdown_body(markdown_url, markdown_headers, session, markdown_data)
        create_TODO(url, authorize_headers, session, body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    excluded: Union[list[str], None] = None
    todo_list_name: Union[str, None] = None
    project_name: Union[str, None] = None

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
    main(arg_parser=parser)
