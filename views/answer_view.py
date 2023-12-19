from flask import Blueprint, request, url_for, render_template, g, flash
from werkzeug.utils import redirect

from jump2 import db
from jump2.models import Question, Answer
from jump2.forms import AnswerForm
from jump2.views.auth_view import login_required

from datetime import datetime

# markdown and markdown to text
import markdown
# from markdownfile.html2text import html2text

bp = Blueprint('answer', __name__, url_prefix = '/answer')

@bp.route('/create/<int:question_id>', methods = ('POST',))
@login_required
def create(question_id) : 
    
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    
    if form.validate_on_submit() :
        ## update real answer in Answer tables
        content = request.form['content']
        answer = Answer(content=content, create_date = datetime.now(), user=g.user)
        ## backref
        question.answer_set.append(answer)
        db.session.commit()
        
        #return redirect(url_for('question.detail', question_id=question_id))
        # redirect to anchor 
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))
    
    
    ## question : question_view blueprint, detail : routing func
    return render_template('question/question_detail.html', question=question, form=form)

# modify answer content endpoint
@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id) : 
    
    answer = Answer.query.get_or_404(answer_id)
    
    if g.user != answer.user : 
        flash('do not have modification permissions.')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    
    if request.method == 'POST' : 
        form = AnswerForm()
        
        if form.validate_on_submit() :
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()
            
            #return redirect(url_for('question.detail', question_id=answer.question.id))
            # redirect to anchor
            return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=answer.question.id), answer.id))
    
    else :
        form = AnswerForm(obj=answer)
        return render_template('answer/answer_form.html', form=form)
    
# delete answer content endpoint
@bp.route('/delete/<int:answer_id>')    
@login_required
def delete(answer_id) :
    
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    
    if g.user != answer.user :
        flash('do not have modification permissions.')
    
    else :
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/vote/<int:answer_id>')
@login_required
def vote(answer_id) : 
    
    _answer = Answer.query.get_or_404(answer_id)
    
    if g.user == _answer.user : 
        flash('this is your content do not recommend')
    
    else :
        _answer.voter.append(g.user)
        db.session.commit()
    ## _answer.question : relationship column about backref
    #return redirect(url_for('question.detail', question_id=_answer.question.id))
    # redirect to anchor
    return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=_answer.question.id), _answer.id))
