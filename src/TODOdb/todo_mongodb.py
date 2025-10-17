import datetime
import os
import pathlib

import bson
from pymongo import MongoClient

uri: str = "mongodb://localhost:27017/"
client: MongoClient = MongoClient(uri)
auto_todo_db_name = "auto-todo-local"
max_num_documents = 10


def main(project_name: str = "", project_path: str = ".\\TODO.md") -> None:
    database = client["auto-todo-local"]

    now = datetime.datetime.now()

    placeholder_name = "placeholder_name"
    test_path = "\\tests\\TODO.md"
    issues_collection_name: str = "list-issues"

    placeholder_path = f"{pathlib.Path(__file__).parent.parent.resolve()}{test_path}"

    if issues_collection_name not in database.list_collection_names():
        database.create_collection(issues_collection_name)

    placeholder_file = open(placeholder_path)
    project_file = open(project_path)

    encoded_file = bson.encode({placeholder_name: placeholder_file.read()})

    encoded_issues = bson.encode({project_name: project_file.read()})

    print(encoded_file)

    issues_collection = database.get_collection("list-issues")
    issues_collection.insert_one(
        {"time": now, "name": placeholder_name, "issues": encoded_file}
    )
    issues_collection.insert_one(
        {"time": now, "name": project_name, "issues": encoded_issues}
    )

    while issues_collection.count_documents({}) > max_num_documents:
        oldest_issues_id = issues_collection.find_one(
            {"time": {"$exists": "true"}}, sort=[("time", 1)]
        ).get("id")
        issues_collection.delete_one({"_id": oldest_issues_id})

    with issues_collection.find() as cursor:
        for doc in cursor:
            print(bson.decode(doc.get("issues")))
            print(doc.get("time"))

    mongodb_path = pathlib.Path(
        "D:\\Program Files (x86)\\GOG Galaxy\\Games\\Gex"
    ).resolve()
    # dir /a:-d /b/s *Loader.exe
    os.system(f"D: && cd {mongodb_path} && Loader.exe")
