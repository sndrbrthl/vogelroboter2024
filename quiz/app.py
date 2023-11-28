
import csv
import random
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import abort, redirect, url_for

from hellodrinkbot import HelloDrinkbot
# If we don't have a Motor hat set EMULATION. We can still run the quiz,
# we just won't get a cocktail
birds=[]
try:
    hd= HelloDrinkbot()
    EMULATION=0
except:
    EMULATION=1

NUM_ANSWERS=3 # how many birds are shown as possible answers
NUM_ROUNDS=4  # how many birds you are shown

AVENO_PUMP = 1 # Pump number for the Aveno
LEMON_PUMP = 3 # Pump number for the Lemon
AVENO_SIZE = 5 # ml
LEMON_SIZE = 3 # ml

app = Flask(__name__)
app.secret_key = b'foobar'
app.debug=True

def read_birds():
    """ reads the list of possible bird answers """
    with open('birds_all.csv',newline='', encoding="UTF8") as lst:
        return [b.strip() for b in lst.readlines()]

def read_quiz():
    """ Read the list of possible questions, with the names and pictures """
    quizlst=[]
    with open('birds_quiz.csv',newline='', encoding="UTF8") as quizfile:
        reader=csv.reader(quizfile)
        for row in reader:
            quizlst.append({'num':row[0],'name':row[1],'url':row[2],'img':row[3]})
    return quizlst

def pick_question_bird():
    """ Which bird are we going to show next? """
    while True:
        bird_num = random.randint(0, len(quizlst)-1)
        if bird_num not in session['used']:
            session['used'].append(bird_num)
            return quizlst[bird_num]

@app.route("/quiz_results")
def quiz_results():
    """ return the results """
    p={}
    p['results']=session['results']
    session['results']=[]
    p['page_title']='Vogel-Quiz Antworten!'
    return render_template("quiz_results.html", p=p)

def check_answer(answer):
    """ check their answer and dispense (or not) the cocktail """

    if 'bird_name' in session:
        if session['bird_name']==answer:
            if EMULATION:
                # don't dispense, we are in emulation mode
                pass
            else:
                hd.dispense(AVENO_PUMP, AVENO_SIZE) # Dispense AVENO
                hd.dispense(LEMON_PUMP, LEMON_SIZE) # Dispense LEMON
        else:
            # sadly they were wrong.
            pass

        # keep track of the results of each question, to display at the end
        try:
            rslt={'bird_name':session['bird_name'], 'img':session['img'], 'answer':answer}
        except:
            rslt={'bird_name':'broken', 'img':'broken', 'answer':'broken'}
        session['results'].append(rslt)
    else:
        # this is the first question, and there should not be results yet.
        session['results']=[]

@app.route("/quiz/<answer>")
@app.route("/quiz")
def quiz(answer=None):
    """ show the quiz, and results, and dispense the cocktail. This code
        suffers from a lack of elegance, but it partially makes up for that
        by appearing to work.
        It uses 'bird' as both a name, and a dict. That is lame"""
    p={}

    if 'question_number' in session:
        session['question_number'] += 1
    else:
        session['question_number']=1
        session['correct_count]'] = 0
        session['results]'] = {}

    if 'used' not in session:
        session['used']=[]

    check_answer(answer) # checks answer, dispenses drink
    # Is their round over? clear the session and return results.
    if session['question_number'] > NUM_ROUNDS:
        p['results']=session['results']
        p['page_title']='Vogel-Quiz Antworten!'
        session.clear()
        return render_template("quiz_results.html", p=p)

    p['birds']=birds
    p['quizlst']=quizlst
    session['bird']=pick_question_bird()
    session['bird_name']=session['bird']['name']
    session['img']=session['bird']['img']
    p['qcnt']=1
    p['q']=session['bird']['num']
    p['answers']=[]
    p['answers'].append(session['bird']['name'])
    while len(p['answers'])<NUM_ANSWERS:
        a_num = random.randint(0, len(birds)-1)
        answer_name = birds[a_num]
        if answer_name not in p['answers'] and answer_name != session['bird']['name']:
            p['answers'].append(p['birds'][a_num])
    random.shuffle(p['answers'])

    p['page_title']='Vogel-Quiz!'
    return render_template("quiz.html", p=p)

@app.route("/bird_list")
def bird_list():
    p={}
    p['birds']=birds
    p['birds'].sort()

    p['page_title']='List of possible birbs'
    return render_template("bird_list.html", p=p)

@app.route("/")
def home():
    p={}
    p['page_title']='Home page!'
    return render_template("home.html", p=p)

birds=read_birds()
quizlst=read_quiz()
