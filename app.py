from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

CURRENT_SURVEY_KEY = 'current_survey' 
RESPONSES_KEY = 'responses'


@app.route('/')
def show_survey_start():
    return render_template('survey_choice.html', surveys = surveys )


@app.route('/', methods=["POST"])
def pick_survey():
    survey_choice = request.form['survey_choice']
    survey = surveys[survey_choice]
    session[CURRENT_SURVEY_KEY] = survey_choice

    return render_template('start.html' ,survey = survey)



@app.route('/start', methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:q_num>')
def get_question(q_num):
    responses = session.get(RESPONSES_KEY)
    survey_choice = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_choice]

    if responses is None:
        return redirect('/')

    elif len(responses) != q_num:
        flash('Please answer questions in order!')
        return redirect(f"/questions/{len(responses)}")

    elif len(responses) == len(survey.questions):         
        return redirect('/complete')

    question = survey.questions[q_num]
    return render_template('questions.html', question = question, q_num = q_num)


@app.route('/answer', methods=["POST"])
def handle_answer():
    answer = request.form['answer']
    text = request.form.get('text', '')

    responses = session[RESPONSES_KEY]
    responses.append({'answer': answer, 'text': text})

    session[RESPONSES_KEY] = responses
    survey_choice = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_choice]

    return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def complete():
    responses = session[RESPONSES_KEY]
    survey_choice = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_choice]
    
    return render_template('complete.html', responses = responses, survey = survey)
    