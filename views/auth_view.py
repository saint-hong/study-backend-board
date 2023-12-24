from flask import Blueprint, url_for, render_template, flash, request, session, g

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from jump2 import db
from jump2.forms import UserCreateForm, UserLoginForm
from jump2.models import User

import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view) :
    @functools.wraps(view)
    def wraped_view(*args, **kwargs) :
        if g.user is None :
            _next = request.url if request.method == 'GET' else ''        
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wraped_view

# same "login_required warp func" in minitter api
# before_app_rquest annertation is first starting every routing
@bp.before_app_request
def load_logged_in_user() :
    
    user_id = session.get('user_id')
    if user_id is None :
        g.user = None
    else :
        # save user obj : id, name, email
        g.user = User.query.get(user_id)

@bp.route('/signup/', methods=('GET', 'POST'))
def signup() :
    
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit() :
        user = User.query.filter_by(username=form.username.data).first()
        if not user :
            user = User(username=form.username.data, 
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else :
            flash('aleady exist user')
    ## if GET request get signup page
    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login() :
    
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit() :
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user :
            error = "not exist user"
        elif not check_password_hash(user.password, form.password.data) :
            error = "not correct password"
        if error is None :
            session.clear()
            session['user_id'] = user.id
            ## _next : g.user = None = not login ---> def login_required()
            _next = request.args.get('next', '')
            if _next :
                return redirect(_next)
            else :
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)
        
@bp.route('/logout')
def logout() :
    
    session.clear()
    
    return redirect(url_for('main.index'))


        
                