import flask.json
from flask import Blueprint, request, make_response
from jsonEncoder.jsonEncoder import JSONEncoder
from BL.users_bl import UsersBL
from BL.log_bl import LogBL

log = Blueprint('log', __name__)

# prod_bl = ProdBL()
flask.json.JSONEncoder = JSONEncoder


@log.route("/", methods=['POST'])
def get_user_by_username_and_password():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            log = request.json["log"]
            res = LogBL().create_log(log)
            return make_response({"log": "created!"}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)
