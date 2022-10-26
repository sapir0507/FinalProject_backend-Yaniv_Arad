import flask.json
from flask import Blueprint, request, make_response
from jsonEncoder.jsonEncoder import JSONEncoder
# from BL.prod_bl import ProdBL
from BL.users_bl import UsersBL

users = Blueprint('users', __name__)

# prod_bl = ProdBL()
flask.json.JSONEncoder = JSONEncoder


# Get All
@users.route("/", methods=['GET'])
def get_users():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            all_users = UsersBL().get_users()
            return make_response({"users": all_users}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@users.route("/<id_of_user>", methods=['GET'])
def get_user_by_id(id_of_user):
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            all_users = UsersBL().get_user_by_id(id_of_user)
            return make_response({"users": all_users}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@users.route("/", methods=['POST'])
def get_user_by_username_and_password():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            username = request.json["username"]
            password = request.json["password"]
            user = UsersBL().get_user_by_username_and_email(username, password)
            return make_response({"user": user}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)
