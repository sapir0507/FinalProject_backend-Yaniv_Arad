import json
import bson.json_util
from pymongo import MongoClient
from bson import ObjectId


# from jsonEncoder.jsonEncoder import JSONEncoder


class EmployeesDepartmentsDBDal:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["factoryDB"]
        self.__Collection = self.__db["employeesDepartmentsCollection"]

    def get_all_users_and_departments(self):
        arr = []
        arr = list(self.__Collection.find({}))
        return json.loads(bson.json_util.dumps(arr))

    def get_department_by_id(self, department_id):
        arr = []
        arr = list(self.__Collection.find({"departmentID": department_id}))
        return json.loads(bson.json_util.dumps(arr))

    def get_department_by_employee_id(self, employee_id):
        # an employee can only belong to one department
        # array_of_departments = []
        arr = list(self.__Collection.find({}))
        arr = json.loads(bson.json_util.dumps(arr))
        for department in arr:
            if employee_id in department["employeesID"]:
                return department["departmentID"]
        # return array_of_departments

    def add_department(self, department_id):
        self.__Collection.insert_one({
            "departmentID": department_id,
            "employeesID": []
        })
        return f'Department with id {department_id} was added'

    def add_employee_to_department(self, employee_id: str, department_id: str):
        arr = self.__Collection.find({"departmentID": department_id})
        arr = json.loads(bson.json_util.dumps(arr))
        if len(arr) > 0:
            obj = {
                "departmentID": arr[0]["departmentID"],
                "employeesID": arr[0]["employeesID"]
            }
            my_id = arr[0]["_id"]["$oid"]
            obj["employeesID"].append(employee_id.__str__())
            self.__Collection.update_one({"_id": ObjectId(my_id)}, {"$set": obj})
        return f'user with id {employee_id} was added from the department with id {department_id}'

    def remove_employee_from_department(self, employee_id, department_id):
        arr = self.__Collection.find({"departmentID": ObjectId(department_id)})
        arr = json.loads(bson.json_util.dumps(arr))
        if len(arr) > 0:
            # arr[0].pop(user_id)
            obj = {
                "shiftID": arr[0]["shiftID"],
                "employeesID": arr[0]["employeesID"]
            }
            obj["employeesID"].pop(employee_id)
            self.__Collection.update_one({"_id": arr[0]["_id"]}, {"$set": obj})
        return f'user with id {employee_id} was removed from the shift with id {department_id}'

    def remove_employee_from_all_departments(self, employee_id):
        departments = self.get_all_users_and_departments()
        for department in departments:
            self.remove_employee_from_department(employee_id, department["_id"])

    def remove_department(self, department_id):
        self.__Collection.delete_one({"_id": ObjectId(department_id)})
        return f"department with id {department_id} was deleted"

    def update_department(self, department_obj):
        self.__Collection.update_one({"_id": department_obj["_id"]}, {"$set": department_obj})
        return f"department with id {ObjectId(department_obj['_id'])} was deleted"
