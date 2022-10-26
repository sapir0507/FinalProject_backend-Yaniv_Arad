from flask import Blueprint, request, make_response
from BL.auth_bl import AuthBL

auth = Blueprint('auth', __name__)
auth_bl = AuthBL()


@auth.route("/", methods=['GET'])
def test():
    print("auth")


# get all
@auth.route("/login", methods=['POST'])
def login():
    username = request.json["username"]
    password = request.json["email"]

    token = auth_bl.get_token(username, password)
    if token is not None:
        return make_response({"token": token}, 200)
    else:
        return make_response({"error": "user is unauthorized"}, 401)
