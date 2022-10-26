import flask.json
from flask import Blueprint, request, make_response
from jsonEncoder.jsonEncoder import JSONEncoder
from BL.department_bl import DepartmentsBL
from BL.users_bl import UsersBL
from BL.employee_bl import EmployeeBL

departments = Blueprint('departments', __name__)

flask.json.JSONEncoder = JSONEncoder


# Get All
@departments.route("/", methods=['GET'])
def get_departments():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            all_departments = DepartmentsBL().get_departments()
            return make_response({"departments": all_departments}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


# @departments.route("/<id_of_department>", methods=['GET'])
# def get_department(id_of_department):
#     if request.headers and request.headers.get('x-access-token'):
#         token = request.headers.get('x-access-token')
#         exist = UsersBL().check_user(token)
#         if exist:
#             department = DepartmentsBL().get_department(id_of_department)
#             return make_response({"department": department}, 200)
#         else:
#             return make_response({"error": "Unauthorized access"}, 401)
#     else:
#         return make_response({"error": "No token provided"}, 401)


@departments.route("/", methods=['POST'])
def add_departments():
    if request.headers and request.headers.get('x-access-token'):
        exist = False
        try:
            token = request.headers.get('x-access-token')
            exist = UsersBL().check_user(token)
        except Exception as e:
            print("user is not authenticated")
        if exist:
            department = request.json["department"]
            print(department)
            DepartmentsBL().add_department(department)
            return make_response({"department": f"employee added: {department}"}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@departments.route("/<department_id>", methods=['DELETE'])
def delete_departments(department_id):
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            DepartmentsBL().delete_department(department_id)
            return make_response({"resp": f"department deleted"}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@departments.route("/<department_id>", methods=['GET'])
def get_department_by_id(department_id):
    print("department id", department_id)
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            dep = DepartmentsBL().get_department_by_id(department_id)
            print("department", dep)
            return make_response({"departments": dep}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@departments.route("/", methods=['PUT'])
def update_department():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            department = request.json["department"]
            dep = DepartmentsBL().update_department(department)
            print(dep)
            return make_response({"department": dep}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)
