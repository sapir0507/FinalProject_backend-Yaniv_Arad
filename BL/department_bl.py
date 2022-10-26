from BL.auth_bl import AuthBL
from DAL.department_dal import DepartmentDBDal
from DAL.employees_departments_dal import EmployeesDepartmentsDBDal


class DepartmentsBL:
    def __init__(self):
        self.__auth_bl = AuthBL()
        self.__departments_dal = DepartmentDBDal()
        self.__employees_departments_dal = EmployeesDepartmentsDBDal()
        self.shifts = []

    def get_departments(self):
        return self.__departments_dal.get_all_departments()

    def get_department_by_id(self, department_id):
        rep = self.__employees_departments_dal.get_department_by_id(department_id)
        return rep

    def check_user(self, token):
        exist = self.__auth_bl.verify_token(token)
        return exist

    def get_department(self, department_id):
        return self.__departments_dal.get_department_by_id(department_id)

    def update_department(self, department):
        return self.__departments_dal.update_department(department)

    def delete_department(self, department_id):
        return self.__departments_dal.delete_department(department_id)

    def add_department(self, department):
        return self.__departments_dal.add_department(department)
