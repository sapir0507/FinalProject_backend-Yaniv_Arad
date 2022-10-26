from DAL.log_dal import LogFileDal


class LogBL:
    def __init__(self):
        self.__logFileDal = LogFileDal()

    def get_all_logs(self):
        logs_from_file = self.__logFileDal.get_all_logs()
        return logs_from_file

    def create_log(self, event):
        return self.__logFileDal.log_action({"id": event['id']}, event)
