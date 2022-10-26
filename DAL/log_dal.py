import json
import os
import sys
from DAL.user_dal import UserDBDal


class LogFileDal:
    def __init__(self):
        self.__actions = []
        self.__user_ws_bl = UserDBDal()

    def log_action(self, user_id, event):
        actions = self.get_all_logs()
        current_action = {}
        path = os.path.join(sys.path[0], "DATA/log.json")

        obj = {"CurrentActions": event["actionAllowed"]}
        self.__user_ws_bl.update_user_by_wsid(user_id["id"], obj)

        with open(path, 'w') as f:
            current_action["id"] = user_id["id"]
            current_action["date"] = str(event["date"])
            current_action["maxActions"] = event["maxActions"]
            current_action["actionAllowed"] = event["actionAllowed"]
            current_action["action"] = event["details"]
            # obj = json.dumps(current_action, indent=4, sort_keys=True, default=str)
            self.__actions.append(current_action)
            json.dump(self.__actions, f)
            return "log created"

    def get_all_logs(self):
        path = os.path.join(sys.path[0], "DATA/log.json")
        with open(path, 'r') as f:
            data = json.load(f)
            if isinstance(data, list):
                self.__actions = data
                return data
            else:
                data = []
                self.__actions = data
                return data

