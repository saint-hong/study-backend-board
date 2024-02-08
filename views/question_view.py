from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from jump2 import db
from jump2.models import Question, Answer, User, answer_voter as av
# QuestionForm class in forms.py
from jump2.forms import QuestionForm, AnswerForm
from jump2.views.auth_view import login_required

from sqlalchemy import func

from datetime import datetime

# markdown, markdown to text
import markdown
# from jump2.markdownfile import html2text

bp = Blueprint('question', __name__, url_prefix='/question')

"""
origin question list endpoint, change code

@bp.route('/list/')
def qlist() :
    
    # get page values in GET request : localhost:5000/question/list/?page=num
    page = request.args.get('page', type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    # paginate func : auto paging
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)
"""
# question list new code with search func
@bp.route('/list/', methods=('GET', 'POST'))
def qlist() :
    
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    question_list = Question.query.order_by(Question.create_date.desc())
    
    if kw :
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username)\
                .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list\
                .join(User)\
                .outerjoin(sub_query, sub_query.c.question_id == Question.id)\
                .filter(Question.subject.ilike(search) |
                        Question.content.ilike(search) |
                        User.username.ilike(search) |
                        sub_query.c.content.ilike(search) |
                        sub_query.c.username.ilike(search))\
                .distinct()
    
    question_list = question_list.paginate(page=page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>/', methods=['GET', 'POST'])
def detail(question_id) : 
    
    answer_form = AnswerForm()
    # 404 error return 
    ## Question.query.get(question_id) ---> Question.query.get_or_404(question_id)
    question = Question.query.get_or_404(question_id)
    
    
    # markdown question content
    question.content = markdown.markdown(question.content, extentions=['nl2br', 'fenced_code'])
    # markdown answer content
    if question.answer_set : 
        for i, answer in enumerate(question.answer_set) :
            question.answer_set[i].content = markdown.markdown(answer.content, extentions=[['nl2br', 'fenced_code']])
    
    # pagenation for answer_list.html
    page = request.args.get('page', type=int, default=1)
    # sort by count answer_voter, av : import answer_voter table
    sub_query = db.session.query(av.c.answer_id, func.count(av.c.user_id).label('count')) \
                          .group_by(av.c.answer_id).subquery()
    answer_list = Answer.query.filter(Answer.question_id == question_id)
    answer_list = answer_list.outerjoin(sub_query, sub_query.c.answer_id == Answer.id).order_by(sub_query.c.count.desc())
    answer_list = answer_list.paginate(page=page, per_page=3)
    
    # answer_list = Answer.query.order_by(Answer.create_date.desc()).filter(Answer.question_id == question_id)
    
    return render_template('question/question_detail.html', question=question, answer_form=answer_form, answer_list=answer_list)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create() : 
    
    form = QuestionForm()
    
    # input data insert into db
    if request.method == 'POST' and form.validate_on_submit() :
        question = Question(subject=form.subject.data, content=form.content.data, 
                            create_date = datetime.now(), user=g.user)
        
        db.session.add(question)
        db.session.commit()
        # main : main.view blueprint, index : routing func
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

# modify question endpoint
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id) :
     
    question = Question.query.get_or_404(question_id)
    
    ## g.user : login user, question.user : create question user
    if g.user != question.user : 
        flash('do not have modification permissions.')
        return redirect(url_for('question.detail', question_id=question_id))
    
    ## if modify save button : POST
    if request.method == 'POST' : 
        form = QuestionForm()
        
        if form.validate_on_submit() :
            ## update to question obj with modified content now
            form.populate_obj(question)
            ## modify datetime save
            question.modify_date = datetime.now()
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    
    ## if modify button request : GET
    else :
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

# delete question endpoint
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id) : 
    
    question = Question.query.get_or_404(question_id)
    
    if g.user != question.user :
        flash('do not have modification permissions.')
        return redirect(url_for('question.detail', question_id=question_id))
    
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question.qlist'))

@bp.route('/vote/<int:question_id>')
@login_required
def vote(question_id) : 
    
    _question = Question.query.get_or_404(question_id)
    
    if g.user == _question.user :
        flash('this is your content do not recommend')
        
    else :
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

