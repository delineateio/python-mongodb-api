import os
from typing import Any, List
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError
from tenacity import (
    retry,
    retry_if_not_exception_type,
    wait_exponential,
    stop_after_attempt,
)
from models import Customer, CustomerInfo
from .errors import (
    RepositoryNotConnected,
    RepositoryNotFoundError,
    RepositoryDuplicateKeyError,
)


# Set environment variables
os.environ["API_USER"] = "username"
os.environ["API_PASSWORD"] = "secret"

# Get environment variables
USER = os.getenv("API_USER")
PASSWORD = os.environ.get("API_PASSWORD")


class Repository:
    def __init__(self):
        self.client = MongoClient(os.environ["MDB_URI"])
        self.database = self.client[os.environ["MDB_DB_NAME"]]
        self.collection_name = os.environ["MDB_COLLECTION_NAME"]
        self.startup()

    @retry(
        wait=wait_exponential(multiplier=0.1), stop=stop_after_attempt(3), reraise=True
    )
    def is_connected(self):

        try:
            self.client.server_info()

        except ServerSelectionTimeoutError as err:
            raise RepositoryNotConnected from err

    @retry(
        wait=wait_exponential(multiplier=0.1), stop=stop_after_attempt(3), reraise=True
    )
    def startup(self) -> None:

        try:
            if self.collection_name not in self.database.list_collection_names():
                collection = self.database.create_collection(self.collection_name)
            else:
                collection = self.database.get_collection(self.collection_name)

            if "handle" not in collection.list_indexes():
                collection.create_index(
                    [("handle", ASCENDING)], name="handle", unique=True
                )

        except ServerSelectionTimeoutError as err:
            raise RepositoryNotConnected from err

    @retry(
        wait=wait_exponential(multiplier=0.1), stop=stop_after_attempt(3), reraise=True
    )
    def reset(self) -> None:

        try:
            self.database.items.delete_many({})

        except ServerSelectionTimeoutError as err:
            raise RepositoryNotConnected from err

    @retry(
        wait=wait_exponential(multiplier=0.1), stop=stop_after_attempt(3), reraise=True
    )
    def get_customers(self) -> List[Customer]:

        customers = []
        for customer_info in self.database.items.find(
            {}, {"handle": 1, "forename": 1, "surname": 1, "email": 1}
        ):
            customers.append(CustomerInfo(**customer_info))
        return customers

    @retry(
        retry=retry_if_not_exception_type(RepositoryNotFoundError),
        wait=wait_exponential(multiplier=0.1),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def get_customer(self, handle: str) -> Customer:

        try:
            handle = handle.lower()
            customer = self.database.items.find_one({"handle": handle})
            if not customer:
                raise RepositoryNotFoundError(handle=handle)
            return Customer(**customer)

        except ServerSelectionTimeoutError as err:
            raise RepositoryNotConnected from err

    @retry(
        retry=retry_if_not_exception_type(RepositoryDuplicateKeyError),
        wait=wait_exponential(multiplier=0.1),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def create_customer(self, data: Any):

        try:
            self.database.items.insert_one(data)

        except DuplicateKeyError:
            # pylint: disable=raise-missing-from
            raise RepositoryDuplicateKeyError(handle="test")
