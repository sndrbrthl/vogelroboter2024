import random
from flask import Flask
from flask import render_template
from flask import session
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
import os
import vogel_constants as config

from hellodrinkbot import HelloDrinkbot

# If we don't have a Motor hat set EMULATION. We can still run the quiz,
# we just won't get a cocktail
try:
    hd = HelloDrinkbot()
    EMULATION = 0
except Exception:
    EMULATION = 1

app = Flask(__name__)
app.secret_key = b"foobar"


def load_quiz_content():
    """This generates a data structure which represents the quiz options"""

    os_walker = os.walk(config.BIRDS_DIR)
    birds_root_dir, birds_dirs, other_files = next(os_walker)

    quiz_content = {
        "img": {difficulty_name: [] for difficulty_name in config.DIFFICULTIES},
        "audio": [],
        "birds": {bird_name: {} for bird_name in sorted(birds_dirs)},
    }

    for bird_name in birds_dirs:
        bird_path = os.path.join(birds_root_dir, bird_name)
        bird_files = os.scandir(bird_path)
        for bird_file in bird_files:
            if bird_file.name in config.DIFFICULTIES:
                if bird_name not in quiz_content["img"][bird_file.name]:
                    quiz_content["img"][bird_file.name].append(bird_name)

            elif bird_file.name.startswith("img_") and bird_file.name.endswith(".webp"):
                if "img" not in quiz_content["birds"][bird_name]:
                    quiz_content["birds"][bird_name]["img"] = bird_file.name

            elif bird_file.name.startswith("ruf_") and bird_file.name.endswith(".webm"):
                if bird_name not in quiz_content["audio"]:
                    quiz_content["audio"].append(bird_name)
                if "ruf" not in quiz_content["birds"][bird_name]:
                    quiz_content["birds"][bird_name]["ruf"] = bird_file.name

            elif bird_file.name.startswith("son_") and bird_file.name.endswith(".webp"):
                if bird_name not in quiz_content["audio"]:
                    quiz_content["audio"].append(bird_name)
                if "son" not in quiz_content["birds"][bird_name]:
                    quiz_content["birds"][bird_name]["son"] = bird_file.name

    return quiz_content


def generate_quiz_questions(
    mode, level="beginner", num_rounds=config.NUM_ROUNDS, num_answers=config.NUM_ANSWERS
):
    questions = []
    available_answer_birds = quiz_content[mode]
    if mode == "img":
        available_answer_birds = available_answer_birds[level]
    available_answer_birds = set(available_answer_birds)
    for question in range(num_rounds):
        correct_answer = random.choice(list(available_answer_birds))
        available_answer_birds.discard(correct_answer)
        answer_options = random.sample(
            list(set(quiz_content["birds"]) - set([correct_answer])), config.NUM_ANSWERS - 1
        ) + [correct_answer]
        random.shuffle(answer_options)
        questions.append(
            {
                "solution": answer_options.index(correct_answer),
                "options": answer_options,
            }
        )
    return questions


def check_answer(answered_question_index, answer_index, questions):
    """check their answer and dispense (or not) the cocktail"""

    if answered_question_index < config.NUM_ROUNDS:  # is the question number valid
        if answer_index <= config.NUM_ANSWERS:  # is the answer number valid
            if "answer" in questions[answered_question_index]:
                flash("You already answered the last question")
            else:
                if questions[answered_question_index]["solution"] == answer_index:
                    if EMULATION:
                        # don't dispense, we are in emulation mode
                        pass
                    else:
                        hd.dispense(config.AVENO_PUMP, config.AVENO_TIME)  # Dispense AVENO
                        hd.dispense(config.LEMON_PUMP, config.LEMON_TIME)  # Dispense LEMON
                else:
                    # sadly they were wrong.
                    pass

                # keep track of the results of each question, to display at the end
                if "answer" not in questions[answered_question_index]:
                    questions[answered_question_index]["answer"] = answer_index
        else:
            flash(
                "The chosen answer number does not exist. \
                    Are you sure you are using the quiz correctly? ;)"
            )
    else:
        flash(
            "The answered question number does not exist. \
                Are you sure you are using the quiz correctly? ;)"
        )
    return questions


@app.route("/")
def home():
    p = {}
    p["page_title"] = "Home page!"
    return render_template("home.html", p=p)


@app.route("/admin")
def admin():
    p = {}
    with open("vogel_constants.py") as vc:
        lst = vc.readlines()

    p["vogel_constants"] = "".join(lst)
    p["quiz_content"] = quiz_content

    p["page_title"] = "List of possible birds"
    return render_template("admin.html", p=p)


# quiz: welcome
@app.route("/quiz/welcome")
def quiz_welcome():
    """Initial welcome screen of the quiz. This should be open by default when in public."""
    p = {}
    if int(request.args.get("clear", 0)) == 1:
        session.clear()
    p["page_title"] = "Welcome to the birds quiz!"
    return render_template("quiz_welcome.html", p=p)


# quiz: prepare
@app.route("/quiz/prepare")
def quiz_prepare():
    """This asks the user to clean up and put a cup underneath the penguin."""
    p = {}
    p["page_title"] = "First things first"
    return render_template("quiz_prepare.html", p=p)


# quiz: modus
@app.route("/quiz/mode")
def quiz_mode():
    """This asks the user to select the mode of the quiz."""
    p = {}
    p["page_title"] = "Seeing or hearing?"
    return render_template("quiz_mode.html", p=p)


# (quiz: difficulty)
@app.route("/quiz/level")
def quiz_level():
    p = {}

    if "mode" not in session:
        session["mode"] = request.args.get("mode", False)
    if session["mode"] not in ("img", "audio"):
        flash(
            "The provided quiz mode does not exist. \
              Are you sure you are using the quiz correctly? ;)"
        )
        redirect(url_for("quiz_mode"))

    p["mode"] = session["mode"]
    if session["mode"] == "img":
        p["page_title"] = "Please select your desired difficulty"
    elif session["mode"] == "audio":
        p["page_title"] = "Are you ready?"
    return render_template("quiz_level.html", p=p)


# quiz: question
@app.route("/quiz/<int:question_num>")
@app.route("/quiz")
def quiz(question_num=None):
    """
    show the quiz, and results, and dispense the cocktail. This code
    suffers from a lack of elegance, but it partially makes up for that
    by appearing to work.
    """
    p = {}

    # PREPARING
    if session["mode"] == "img":
        if "level" not in session:
            session["level"] = request.args.get("level", False)
        if session["level"] not in config.DIFFICULTIES:
            flash(
                "The provided difficulty level does not exist. \
                Are you sure you are using the quiz correctly? ;)"
            )
            redirect(url_for("quiz_level"))

    if "questions" not in session:
        session["questions"] = generate_quiz_questions(
            mode=session["mode"],
            level=session.get("level", "Beginner"),
            num_rounds=config.NUM_ROUNDS,
            num_answers=config.NUM_ANSWERS,
        )

    # GETTING USER ANSWER
    if question_num > 1:
        answered_question = int(request.args.get("aq", 0))
        answer = int(request.args.get("a", 0))

        # CHECKING USER ANSWER
        session["questions"] = check_answer(
            answered_question - 1, answer - 1, session["questions"]
        )  # checks and stores answer, dispenses drink

    # RENDERING RESULTS
    # Is their round over? clear the session and return results.
    if question_num > config.NUM_ROUNDS:
        return render_template("quiz_donate.html", p=p)

    # RENDERING QUESTION PAGE
    p["question_num"] = question_num
    p["questions"] = session["questions"]
    p["mode"] = session["mode"]
    p["quiz_content"] = quiz_content
    p["page_title"] = "Vogel-Quiz!"
    return render_template("quiz.html", p=p)


# quiz: donate
@app.route("/quiz/donate")
def quiz_donate():
    """Displays a donation page."""
    p = {}
    p["page_title"] = "Please feed the bird!"
    return render_template("quiz_donate.html", p=p)


# quiz: results
@app.route("/quiz/results")
def quiz_results():
    """return the results"""
    p = {}
    p["quiz_content"] = quiz_content
    p["questions"] = session["questions"]
    p["page_title"] = "Vogel-Quiz Antworten!"
    return render_template("quiz_results.html", p=p)


quiz_content = load_quiz_content()
