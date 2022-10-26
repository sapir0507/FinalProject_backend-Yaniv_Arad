from flask import Flask
import json
from bson import ObjectId
from flask_cors import CORS

from ROUTES.auth_router import auth
from ROUTES.user_router import users
from ROUTES.department_router import departments
from ROUTES.shift_router import shifts
from ROUTES.employee_router import employees
from ROUTES.log_router import log


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


app = Flask(__name__)

app.json_provider_class = JSONEncoder
app.url_map.strict_slashes = False
CORS(app)

# all the blueprints
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(departments, url_prefix="/departments")
app.register_blueprint(shifts, url_prefix="/shifts")
app.register_blueprint(employees, url_prefix="/employees")
app.register_blueprint(log, url_prefix="/log")

# app.register_blueprint(products, url_prefix="/prods")

app.run()
