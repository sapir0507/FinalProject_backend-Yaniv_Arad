import json
import bson.json_util
from pymongo import MongoClient
from bson import ObjectId


# from jsonEncoder.jsonEncoder import JSONEncoder


class UserDBDal:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["factoryDB"]
        self.__Collection = self.__db["usersCollection"]

    def get_all_users(self):
        arr = []
        arr = list(self.__Collection.find({}))
        return json.loads(bson.json_util.dumps(arr))

    def add_user(self, obj):
        self.__Collection.insert_one(obj)
        return 'created with ID' + str(obj["_id"])

    def update_all_users(self, updated_users_collection):
        self.__Collection.update_many({}, {"$set": updated_users_collection})
        return f"users updated"

    def update_user_by_id(self, user_id, update_collection):
        self.__Collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_collection})
        return f'user with id {user_id} was updated'

    def update_user_by_wsid(self, user_id, update_collection):
        self.__Collection.update_one({"WSID": user_id}, {"$set": update_collection})
        return f'user with WSID {user_id} was updated'

    def delete_user_by_id(self, user_id):
        self.__Collection.delete_one({"_id": ObjectId(user_id)})
        return f"user with id {user_id} was deleted"
