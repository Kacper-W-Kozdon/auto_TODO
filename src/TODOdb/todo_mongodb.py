import os
import pathlib

import bson
from pymongo import MongoClient

uri: str = "mongodb://localhost:27017/"
client: MongoClient = MongoClient(uri)
auto_todo_db_name = "auto-todo-local"


def main(project_name: str = "", project_path: str = ".\\TODO.md") -> None:
    database = client["auto-todo-local"]

    test_path = "\\tests\\TODO.md"
    placeholder_path = f"{pathlib.Path(__file__).parent.parent.resolve()}{test_path}"

    issues_collection_name: str = "list-issues"
    if issues_collection_name not in database.list_collection_names():
        database.create_collection(issues_collection_name)

    placeholder_file = open(placeholder_path)
    project_file = open(project_path)

    encoded_file = bson.encode({project_name: placeholder_file.read()})

    encoded_issues = bson.encode({project_name: project_file.read()})

    print(encoded_file)

    issues_collection = database.get_collection("list-issues")
    issues_collection.insert_one({f"{project_name}_issues": encoded_file})
    issues_collection.insert_one({f"{project_name}_issues": encoded_issues})

    with issues_collection.find() as cursor:
        for doc in cursor:
            print(bson.decode(doc.get(f"{project_name}_issues")))

    mongodb_path = pathlib.Path(
        "D:\\Program Files (x86)\\GOG Galaxy\\Games\\Gex"
    ).resolve()
    # dir /a:-d /b/s *Loader.exe
    os.system(f"D: && cd {mongodb_path} && Loader.exe")
