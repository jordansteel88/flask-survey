from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_survey_start():
    responses.clear()
    return render_template('start.html', survey = survey)

@app.route('/start')
def start_survey():
    return redirect('/questions/0')

@app.route('/questions/<int:q_num>')
def get_question(q_num):
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
    responses.append(answer)
    
    return redirect(f"/questions/{len(responses)}")

@app.route('/complete')
def complete():
    return render_template('complete.html')
    