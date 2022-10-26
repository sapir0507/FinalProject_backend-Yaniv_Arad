from pymongo import MongoClient
import json
from bson import json_util, ObjectId


class DepartmentDBDal:
    def __init__(self):
        self.__client = MongoClient(port=27017)
        self.__db = self.__client["factoryDB"]
        self.__Collection = self.__db["departmentCollection"]

    def get_all_departments(self):
        arr = []
        arr = list(self.__Collection.find({}))
        return json.loads(json_util.dumps(arr))

    def update_all_departments(self, updated_department_collection):
        try:
            self.__Collection.update_many({}, {"$set": updated_department_collection})
            return True
        except Exception as err:
            print(err)
        finally:
            return False

    def add_department(self, department):
        try:
            self.__Collection.insert_one(department)
            return True
        except Exception as err:
            print(err)
        finally:
            return False

    def delete_department(self, department_id):
        try:
            self.__Collection.delete_one({"_id": ObjectId(department_id)})
            return True
        except Exception as err:
            print(err)
        finally:
            return False

    def update_department(self, department):
        try:
            print(department)
            department_id = ObjectId(department['id'])
            department.pop("id")  # remove the id
            self.__Collection.update_one({"_id": ObjectId(department_id)}, {"$set": department})
            return True
        except Exception as err:
            print(err)
        finally:
            return False

    def get_department_by_id(self, department_id):
        try:
            self.__Collection.find_one({"_id": ObjectId(department_id)})
            return True
        except Exception as err:
            print(err)
        finally:
            return False
