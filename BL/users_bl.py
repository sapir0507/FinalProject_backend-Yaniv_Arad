from BL.auth_bl import AuthBL
from DAL.user_dal import UserDBDal
from DAL.auth_dal import AuthWSDal
import jwt
from bson import ObjectId


class UsersBL:
    def __init__(self):
        self.__auth_bl = AuthBL()
        self.__users_dal = UserDBDal()
        self.__auth_dal = AuthWSDal()
        self.shifts = []

    def get_users(self):
        resp = self.__users_dal.get_all_users()
        return resp

    def get_user_by_id(self, user_id):
        all_users = self.get_users()
        arr = list(filter(lambda x: x["_id"]['$oid'] == user_id, all_users))
        if len(arr) > 0:
            return arr[0]
        else:
            return arr

    def get_user_by_username_and_email(self, username, email):
        all_users = self.__auth_dal.get_all_users()
        arr = list(filter(lambda x: x["username"] == username and x["email"] == email, all_users))
        if len(arr) > 0:
            user_id = arr[0]["id"]
            all_users = self.get_users()
            arr2 = list(filter(lambda x: str(x["WSID"]) == str(user_id), all_users))
            if len(arr2) > 0:
                return arr2[0]
        return []

    def update_user_by_id(self, user_id, obj):
        self.__users_dal.update_user_by_id(user_id, obj)

    def delete_user_by_id(self, user_id):
        self.__users_dal.delete_user_by_id(user_id)

    def delete_all_users(self):
        all_users = self.get_users()
        for user in all_users:
            self.delete_user_by_id(user["_id"])

    def add_user(self, obj):
        self.__users_dal.add_user(obj)

    def check_user(self, token):
        exist = self.__auth_bl.verify_token(token)
        return exist


