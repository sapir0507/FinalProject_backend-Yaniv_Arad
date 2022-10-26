from flask import Blueprint, jsonify, request, make_response

# from BL.prod_bl import ProdBL


products = Blueprint('products', __name__)


# prod_bl = ProdBL()

# Get All
@products.route("/", methods=['GET'])
def get_products():
    # if request.headers and request.headers.get('x-access-token'):
    #     token = request.headers.get('x-access-token')
    #     exist = prod_bl.check_user(token)
    #     if exist == True:
    #         prods = prod_bl.get_products()
    #         return make_response({"prods" : prods},200)
    #     else:
    #         return make_response({"error" : "Not authorized"},401)
    # else:
    return make_response({"error": "No token provided"}, 401)
