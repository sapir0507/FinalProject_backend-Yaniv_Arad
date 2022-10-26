import flask.json
from flask import Blueprint, request, make_response
from jsonEncoder.jsonEncoder import JSONEncoder
from BL.shifts_bl import ShiftsBL
from BL.users_bl import UsersBL

shifts = Blueprint('shifts', __name__)

# prod_bl = ProdBL()
flask.json.JSONEncoder = JSONEncoder


# Get All
@shifts.route("/", methods=['GET'])
def get_shifts():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            all_shifts = ShiftsBL().get_shifts()
            return make_response({"shifts": all_shifts}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@shifts.route("/", methods=['POST'])
def add_shift():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            shift = request.json["shift"]
            ShiftsBL().add_shift(shift)
            return make_response({"shifts": f"shift added: {shift}"}, 200)
    else:
        return make_response({"error": "No token provided"}, 401)


@shifts.route("/<id_of_shift>", methods=['GET'])
def get_shift(id_of_shift):
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            shift = ShiftsBL().get_shift(id_of_shift)
            return make_response({"shift": shift}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)


@shifts.route("/", methods=['PUT'])
def update_shift():
    if request.headers and request.headers.get('x-access-token'):
        token = request.headers.get('x-access-token')
        exist = UsersBL().check_user(token)
        if exist:
            shift = request.json["shift"]

            resp = ShiftsBL().update_shift(shift_obj=shift)
            return make_response({"resp": resp}, 200)
        else:
            return make_response({"error": "Unauthorized access"}, 401)
    else:
        return make_response({"error": "No token provided"}, 401)
