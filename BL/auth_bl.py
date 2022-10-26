import jwt
import datetime
from DAL.user_dal import UserDBDal
from DAL.auth_dal import AuthWSDal


class AuthBL:
    def __init__(self):
        self.__user_ws_bl = UserDBDal()
        self.__auth_ws_dal = AuthWSDal()
        self.__key = "server_key"
        self.__algorithm = "HS256"

    def get_token(self, username, password):
        user = self.__check_user(username, password)
        token = None
        if user is not None:
            token = jwt.encode(user, self.__key, self.__algorithm)
        return token

    def verify_token(self, token):
        data = jwt.decode(token, self.__key, self.__algorithm)
        date = datetime.datetime.now()
        print("jwt data", data)
        try:
            # token is past the expiration date
            if data["date"] != f"{date.day}-{date.month}-{date.year}":
                # update the database
                if data["currentActions"] != data["actions"]:
                    self.__user_ws_bl.update_user_by_wsid(user_id=data["userid"], update_collection={
                        "currentActions": data["actions"]
                    })
                return False

            if data["currentActions"] == 0:  # logout
                return False

            if isinstance(data['userid'], int) or isinstance(data['userid'], str):
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def __check_user(self, username, password):
        user = {}
        users = self.__auth_ws_dal.get_all_users()

        arr = list(filter(lambda x: x["username"] == username and x["email"] == password, users))
        date = datetime.datetime.now()
        if len(arr) > 0:
            db_users = self.__user_ws_bl.get_all_users()
            for some_user in db_users:
                if some_user["FullName"] == arr[0]["name"]:
                    user['userid'] = arr[0]["id"]
                    user["fullName"] = arr[0]["name"]
                    user["actions"] = some_user["MaxActions"]
                    user[
                        "date"] = f"{date.day}-{date.month}-{date.year}"
                    user["currentActions"] = some_user["CurrentActions"]
                    print(user)
                    return user
            return None
        return None
