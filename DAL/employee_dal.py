from bson import json_util, ObjectId
import json
from pymongo import MongoClient


class EmployeesDBDal:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["factoryDB"]
        self.__Collection = self.__db["employeeCollection"]

    def get_all_employees(self):
        arr = []
        arr = list(self.__Collection.find({}))
        return json.loads(json_util.dumps(arr))

    def get_employee_by_id(self, employee_id):
        self.__Collection.find_one({"_id": ObjectId(employee_id)})

    def update_all_employees(self, updated_employees_collection):
        self.__Collection.update_many({}, {"$set": updated_employees_collection})

    def add_employee(self, employee):
        employee_id = self.__Collection.insert_one(employee)
        return employee_id.inserted_id

    def update_employee(self, employee):
        self.__Collection.update_one({"_id": ObjectId(employee["_id"])}, {"$set": employee})

    def delete_employee(self, employee_id):
        self.__Collection.delete_one({"_id": ObjectId(employee_id)})
