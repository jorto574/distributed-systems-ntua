from flask import Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    return "Server of Blockchat Node is up and running"