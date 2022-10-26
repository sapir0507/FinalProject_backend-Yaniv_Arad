from BL.auth_bl import AuthBL
from DAL.shift_dal import ShiftsDBDal
from DAL.employees_shifts_dal import EmployeesShiftsDBDal


class ShiftsBL:
    def __init__(self):
        self.__auth_bl = AuthBL()
        self.__shifts_dal = ShiftsDBDal()
        self.__employees_shifts = EmployeesShiftsDBDal()
        self.shifts = []

    def get_shifts(self):
        all_shifts = self.__shifts_dal.get_all_shifts()
        return all_shifts

    def get_shift(self, shift_id):
        all_shifts = self.get_shifts()
        arr = list(filter(lambda x: x["_id"]["$oid"] == shift_id, all_shifts))
        if len(arr) > 0:
            return arr[0]

    def check_user(self, token):
        exist = self.__auth_bl.verify_token(token)
        return exist

    def add_shift(self, shift):
        try:
            self.__shifts_dal.add_shift(shift)
            return True
        except Exception as err:
            print(err)
        finally:
            return False

    def update_shift(self, shift_obj):
        try:
            my_id = shift_obj["id"]
            obj = {
                "Date": shift_obj["Date"],
                "StartingHour": shift_obj["StartingHour"],
                "EndingHour": shift_obj["EndingHour"]
            }
            self.__shifts_dal.update_shift(shift_obj=obj, my_id=my_id)
            return True
        except Exception as err:
            print(err)
        finally:
            return False
