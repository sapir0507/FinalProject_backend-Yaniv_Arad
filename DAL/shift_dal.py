from pymongo import MongoClient
from bson import json_util, ObjectId
import json


class ShiftsDBDal:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["factoryDB"]
        self.__Collection = self.__db["ShiftCollection"]

    def get_all_shifts(self):
        arr = []
        arr = list(self.__Collection.find({}))
        return json.loads(json_util.dumps(arr))

    def update_all_shifts(self, updated_shift_collection):
        self.__Collection.update_many({}, {"$set": updated_shift_collection})

    def add_shift(self, shift):
        self.__Collection.insert_one(shift)

    def update_shift(self, my_id, shift_obj):
        self.__Collection.update_one({"_id": ObjectId(my_id)}, {"$set": shift_obj})
