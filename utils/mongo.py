from pymongo import MongoClient
from urllib.parse import quote


class MongoUtils:
    def __init__(
        self,
        username: str,
        password: str,
        cluster: str,
        database: str,
    ) -> None:
        self.client: MongoClient = MongoClient(
            f"mongodb+srv://{quote(username, safe='')}:{quote(password, safe='')}@{cluster}?retryWrites=true&w=majority"
        )
        self.db = self.client[database]
