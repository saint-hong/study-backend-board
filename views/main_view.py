from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix = '/')

@bp.route('/ping', methods = ['GET'])
def ping() :     
    return 'pong'

@bp.route('/')
def index() : 
    3/0
    # question : question_view blueprint, qlist : routing func 
    return redirect(url_for('question.qlist'))
