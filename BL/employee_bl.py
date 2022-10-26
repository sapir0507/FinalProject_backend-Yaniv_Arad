from BL.auth_bl import AuthBL
from DAL.employee_dal import EmployeesDBDal
from DAL.shift_dal import ShiftsDBDal
from DAL.employees_shifts_dal import EmployeesShiftsDBDal
from DAL.employees_departments_dal import EmployeesDepartmentsDBDal


class EmployeeBL:
    def __init__(self):
        self.__auth_bl = AuthBL()
        self.__employees_dal = EmployeesDBDal()
        self.__shifts_dal = ShiftsDBDal()
        self.__employees_shifts_dal = EmployeesShiftsDBDal()
        self.__employees_departments_dal = EmployeesDepartmentsDBDal()
        self.shifts = []

    def get_employees(self):
        self.shifts = []
        emp = self.__employees_dal.get_all_employees()
        for employee in emp:
            l1 = self.__employees_departments_dal.get_department_by_employee_id(str(employee["_id"]["$oid"]))
            l2 = self.__employees_shifts_dal.get_shift_by_employee_id(str(employee["_id"]["$oid"]))

            employee["shifts"] = l2  # array of shifts (IDs)
            employee["DepartmentID"] = l1  # department (ID)
        return emp

    def get_employee(self, employee_id):
        self.shifts = []
        emp = self.__employees_dal.get_employee_by_id(employee_id)
        l1 = self.__employees_departments_dal.get_department_by_employee_id(str(emp["_id"]["$oid"]))
        l2 = self.__employees_shifts_dal.get_shift_by_employee_id(str(emp["_id"]["$oid"]))

        emp["DepartmentID"] = l1  # department (ID)
        emp["shifts"] = l2
        return emp

    def check_user(self, token):
        exist = self.__auth_bl.verify_token(token)
        return exist

    def add_employee(self, employee):
        try:
            department = employee.pop("DepartmentID")
            employee_id = self.__employees_dal.add_employee(employee)
            print(employee_id, department)
            self.__employees_departments_dal.add_employee_to_department(employee_id=employee_id,
                                                                        department_id=department)
            return employee_id
        except Exception as err:
            print(err)
        finally:
            return False

    def update_employee(self, employee_id):
        try:
            self.__employees_dal.update_employee(employee_id)
            return True
        except Exception as err:
            print(err)
        finally:
            return False

    def delete_employee(self, employee_id):
        try:
            self.__employees_dal.delete_employee(employee_id)
            self.__employees_shifts_dal.remove_user_from_all_shifts(employee_id)
            return True
        except Exception as err:
            print(err)
        finally:
            return False

    def add_employee_to_shift(self, shift_id, employee_id):
        relevant_shift = self.__employees_shifts_dal.get_shift_by_employee_id(shift_id)
        all_shifts = self.__shifts_dal.get_all_shifts()
        for shift in all_shifts:
            if shift["_id"]["$oid"] == shift_id and len(relevant_shift) == 0:
                self.__employees_shifts_dal.add_shift(shift_id)
                return self.__employees_shifts_dal.add_user_to_shift(user_id=employee_id, shift_id=shift_id)
            elif shift["_id"]["$oid"] == shift_id and len(relevant_shift) > 0:
                self.__employees_shifts_dal.add_user_to_shift(user_id=employee_id, shift_id=shift_id)
        return f"employee with id {employee_id} or shift with id {shift_id} doesn't exist"

    def add_employee_to_department(self, department_id, employee_id):
        # find if there's an employee with id 'employee id' inside the department, and if so, don't add them again
        department = self.__employees_departments_dal.get_department_by_id(department_id)
        if employee_id not in department[0]["employeesID"]:
            # remove employee from all the other departments
            self.__employees_departments_dal.remove_employee_from_all_departments(employee_id=employee_id)
            # add the employee to his new department
            self.__employees_departments_dal.add_employee_to_department(employee_id, department_id)
            return "employee added"
        return "employee already exists in said department"

    def delete_employee_from_shift(self, shift_id, employee_id):
        shift_info = self.__get_shift_with_id(shift_id)
        if not len(shift_info) > 0:
            return f"shift with id {shift_id} doesn't exist"
        else:
            if employee_id not in shift_info[0]["employeesID"]:
                return f"employee with id {employee_id} doesn't exist in shift with id {shift_id}"
            else:
                return self.__employees_shifts_dal.remove_user_from_shift(shift_id, employee_id)

    def __get_shift_with_id(self, shift_id):
        arr = []
        all_shifts = self.__shifts_dal.get_all_shifts()
        shift_info = list(filter(lambda x: x["_id"] == shift_id, all_shifts))
        if len(shift_info) > 0:
            return shift_info
        return arr

    def __get_all_employee_shifts(self, employee_id: str):
        self.shifts = []
        shift_info = self.__employees_shifts_dal.get_all_users_and_shifts()
        if len(shift_info) > 0:
            for shift in shift_info:
                arr = list(filter(lambda x: employee_id in x["employeesID"], shift_info))
                if len(arr) > 0:
                    self.shifts.append(shift["shiftID"])
        return self.shifts
