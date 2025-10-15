import os
import pathlib

import bson
from pymongo import MongoClient

uri: str = "mongodb://localhost:27017/"
client: MongoClient = MongoClient(uri)

database = client["auto-todo-local"]

placeholder_path = f"{pathlib.Path(__file__).parent.parent.resolve()}\\tests\\TODO.md"

issues_collection_name: str = "list-issues"
if issues_collection_name not in database.list_collection_names():
    database.create_collection(issues_collection_name)

placeholder_file = open(placeholder_path)
encoded_file = bson.encode({"test": placeholder_file.read()})

print(encoded_file)

issues_collection = database.get_collection("list-issues")
issues_collection.insert_one({"issues": encoded_file})
issues_collection.find_one("id = 1")

with issues_collection.find() as cursor:
    for doc in cursor:
        print(bson.decode(doc.get("issues")))

mongodb_path = pathlib.Path("D:\\Program Files (x86)\\GOG Galaxy\\Games\\Gex").resolve()
# dir /a:-d /b/s *Loader.exe
os.system(f"D: && cd {mongodb_path} && Loader.exe")
