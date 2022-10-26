import flask.json
from flask import Blueprint, request, make_response
from jsonEncoder.jsonEncoder import JSONEncoder
from BL.employee_bl import EmployeeBL
from BL.users_bl import UsersBL

employees = Blueprint('employees', __name__)

# prod_bl = ProdBL()
flask.json.JSONEncoder = JSONEncoder


# Get All
@employees.route("/", methods=['GET'])
def get_employees():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            all_employees = EmployeeBL().get_employees()
            return make_response({"employees": all_employees}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@employees.route("/<id_of_employee>", methods=['GET'])
def get_employee(id_of_employee):
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            employee = EmployeeBL().get_employee(id_of_employee)
            return make_response({"employee": employee}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@employees.route("/dep/<department_id>", methods=['GET'])
def get_employees_by_department_id(department_id):
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            all_employees = EmployeeBL().get_employees()
            employee_of_the_same_department = list(filter(lambda x: x["DepartmentID"] == department_id, all_employees))
            return make_response({"employees": employee_of_the_same_department}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@employees.route("/", methods=['POST'])
def add_employees():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            employee = request.json["employee"]
            resp = EmployeeBL().add_employee(employee)
            return make_response({"employees": f"employee added: {employee}"}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@employees.route("/", methods=['PUT'])
def edit_employees():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            employee = request.json["employee"]
            EmployeeBL().update_employee(employee)
            return make_response({"employees": f"employee updated: {employee}"}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@employees.route("/<employee_id>", methods=['DELETE'])
def delete_employees(employee_id):
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            EmployeeBL().delete_employee(employee_id)
            return make_response({"employees": "employee deleted"}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@employees.route("/add-to-shift", methods=['POST'])
def add_employee_to_shift():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            employee = request.json["employee"]
            EmployeeBL().add_employee_to_shift(employee_id=employee["employeeId"], shift_id=employee["shiftId"])
            return make_response({"employees": "employee deleted"}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@employees.route("/add-to-department", methods=['POST'])
def add_employee_to_department():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            employee = request.json["employee"]
            resp = EmployeeBL().add_employee_to_department(department_id=employee["department_id"],
                                                           employee_id=employee["employeeId"])
            return make_response({"employees": resp}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)
