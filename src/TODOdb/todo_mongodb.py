import datetime
import pathlib
from typing import Any, Optional, Union

import bson
from pymongo import MongoClient, database


class DBManager:
    """Manager class for the mongo database storing issues.
    :param uri:
    :type uri:
    :param max_num_documents:
    :type max_num_documents:

    """

    _client: Optional[MongoClient] = None
    _instance = None

    def __new__(cls) -> Any:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = MongoClient()
        return cls._instance

    def __init__(
        self,
        uri: str = "mongodb://localhost:27017/",
        auto_todo_db_name: str = "auto-todo-local",
        max_num_documents: int = 10,
    ) -> None:
        if not isinstance(self._client, MongoClient):
            raise TypeError("MongoClient was not properly initiated.")

        self._client.uri = uri
        self._database: database.Database = self._client[auto_todo_db_name]
        self.max_num_documents = max_num_documents

    def __call__(
        self, project_name: str = "", project_path: str = ".\\TODO.md"
    ) -> None:
        now = datetime.datetime.now()

        issues_collection_name: str = project_name

        self.update(
            time=now,
            issues_collection_name=issues_collection_name,
            project_path=project_path,
        )

        raise NotImplementedError

    def update(
        self,
        time: Union[None, datetime.datetime] = None,
        issues_collection_name: str = "",
        project_path: str = ".\\TODO.md",
    ) -> None:
        max_num_documents = self.max_num_documents
        now = time
        database = self._database

        placeholder_name = "placeholder_name"
        test_path = "\\tests\\TODO.md"
        placeholder_path = (
            f"{pathlib.Path(__file__).parent.parent.resolve()}{test_path}"
        )

        if issues_collection_name not in database.list_collection_names():
            database.create_collection(issues_collection_name)

        placeholder_file = open(placeholder_path)
        project_file = open(project_path)

        encoded_file = bson.encode({placeholder_name: placeholder_file.read()})

        encoded_issues = bson.encode({"issues": project_file.read()})

        print(encoded_file)

        issues_collection = database.get_collection(issues_collection_name)
        issues_collection.insert_one({"time": now, "issues": encoded_file})
        issues_collection.insert_one({"time": now, "issues": encoded_issues})

        while issues_collection.count_documents({}) > max_num_documents:
            oldest_issues_id = issues_collection.find_one(
                {"time": {"$exists": "true"}}, sort=[("time", 1)]
            ).get("id")
            issues_collection.delete_one({"_id": oldest_issues_id})

        with issues_collection.find() as cursor:
            for doc in cursor:
                print(bson.decode(doc.get("issues")))
                print(doc.get("time"))
        raise NotImplementedError

    # mongodb_path = pathlib.Path(
    #     "D:\\Program Files (x86)\\GOG Galaxy\\Games\\Gex"
    # ).resolve()
    # dir /a:-d /b/s *Loader.exe
    # os.system(f"D: && cd {mongodb_path} && Loader.exe")
