from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from app.models_schema import UserSchema, AdminSchema

class MongoService:
    def __init__(self, collection_name, uri="mongodb://localhost:27017", db_name="Clients"):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

        self._connect()

    def _connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            print("Connected to MongoDB")
        except ConnectionFailure as e:
            print("MongoDB connection failed:", e)
            raise

    # Insert one document
    def insert_record(self, data: dict):
        try:
            result = self.collection.insert_one(data)
            return str(result.inserted_id)
        except OperationFailure as e:
            print("Insert failed:", e)
            return None

    # Insert multiple documents
    def insert_many(self, data_list: list):
        try:
            result = self.collection.insert_many(data_list)
            return [str(x) for x in result.inserted_ids]
        except OperationFailure as e:
            print("Insert many failed:", e)
            return None

    # Retrieve all documents
    def get_all(self):
        return list(self.collection.find({}))

    # Search using filters
    def find_by(self, query: dict):
        return list(self.collection.find(query))

    # Optional: Update
    def update(self, query: dict, new_values: dict):
        return self.collection.update_many(query, {"$set": new_values})

class UserRepository:
    def __init__(self):
        self.db_user = MongoService(collection_name="user")
        self.db_admin = MongoService(collection_name="admin")

    def add_user(self, user_data: dict) -> str:
        user = UserSchema(**user_data)  # validate
        return self.db_user.insert_record(user.model_dump())

    def add_admin(self, admin_data: dict) -> str:
        admin = AdminSchema(**admin_data)
        return self.db_admin.insert_record(admin.model_dump())

    def get_users(self, filters=None):
        return self.db_user.get_all()

    def get_admins(self, filters=None):
        return self.db_admin.get_all()

