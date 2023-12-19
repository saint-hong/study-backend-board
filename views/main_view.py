from flask import Blueprint, url_for, current_app
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix = '/')

@bp.route('/ping', methods = ['GET'])
def ping() :     
    return 'pong'

@bp.route('/')
def index() : 
    
    current_app.logger.info("INFO 레벨로 출력")
    # question : question_view blueprint, qlist : routing func 
    return redirect(url_for('question.qlist'))
