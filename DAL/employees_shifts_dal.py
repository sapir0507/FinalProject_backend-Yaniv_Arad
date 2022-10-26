import json
import bson.json_util
from pymongo import MongoClient
from bson import ObjectId


# from jsonEncoder.jsonEncoder import JSONEncoder


class EmployeesShiftsDBDal:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["factoryDB"]
        self.__Collection = self.__db["employeesShiftsCollection"]

    def get_all_users_and_shifts(self):
        arr = []
        arr = list(self.__Collection.find({}))
        return json.loads(bson.json_util.dumps(arr))

    def get_shift_by_shift_id(self, shift_id):
        arr = []
        arr = list(self.__Collection.find({"shiftID": shift_id}))
        return json.loads(bson.json_util.dumps(arr))

    def get_shift_by_employee_id(self, employee_id):
        array_of_shifts = []
        arr = list(self.__Collection.find({}))
        arr = json.loads(bson.json_util.dumps(arr))
        for shift in arr:
            if employee_id in shift["employeesID"]:
                array_of_shifts.append(shift["shiftID"])
        return array_of_shifts

    def add_shift(self, shift_id):
        self.__Collection.insert_one({
            "shiftID": shift_id,
            "employeesID": []
        })
        return f'Shift with id {shift_id} was added'

    def add_user_to_shift(self, user_id, shift_id):
        arr = self.__Collection.find({"shiftID": shift_id})
        arr = json.loads(bson.json_util.dumps(arr))
        if len(arr) > 0:
            obj = {
                "shiftID": arr[0]["shiftID"],
                "employeesID": arr[0]["employeesID"]
            }
            my_id = arr[0]["_id"]["$oid"]
            obj["employeesID"].append(user_id)
            self.__Collection.update_one({"_id": ObjectId(my_id)}, {"$set": obj})
        return f'user with id {user_id} was added from the shift with id {shift_id}'

    def remove_user_from_shift(self, user_id, shift_id):
        arr = self.__Collection.find({"shiftID": ObjectId(shift_id)})
        arr = json.loads(bson.json_util.dumps(arr))
        if len(arr) > 0:
            # arr[0].pop(user_id)
            obj = {
                "shiftID": arr[0]["shiftID"],
                "employeesID": arr[0]["employeesID"]
            }
            obj["employeesID"].pop(user_id)
            self.__Collection.update_one({"_id": arr[0]["_id"]}, {"$set": obj})
        return f'user with id {user_id} was removed from the shift with id {shift_id}'

    def remove_user_from_all_shifts(self, user_id):
        shifts = self.get_all_users_and_shifts()
        for shift in shifts:
            self.remove_user_from_shift(user_id, shift["_id"])

    def remove_shift(self, shift_id):
        self.__Collection.delete_one({"_id": ObjectId(shift_id)})
        return f"shift with id {shift_id} was deleted"

    def update_shift(self, shift_obj):
        self.__Collection.update_one({"_id": shift_obj["_id"]}, {"$set": shift_obj})
        return f"shift with id {ObjectId(shift_obj['_id'])} was deleted"
