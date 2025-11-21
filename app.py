from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from scanner import takeit
from JePeux import query_openai
import os



#plan
#get input n shi working, basic home page with form, jinja blah
# - separate feet in the algorythm, count how many entires of long'd or shorted vowels have appeared, then put a || at the end of that word or whatever
#do it with gpt
#flask index
#- history page, instruction on how to scan, support/contact page with credits
#registering and log in feature
#database to store previous inputs, user info etc.
#admin panel?


custom_template_path = os.path.join(os.path.dirname(__file__), 'pantheon')
app = Flask(__name__, template_folder=custom_template_path)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    """page to input line of poetry"""
    if request.method == "POST":
        #get scansion.
        #redirect to scansion page, with template filled with scansion stuff
        line = request.form.get("usrinput")
        print(line)
        try:
            algorithm_output = takeit(line)
        except Exception as e:
            algorithm_output = e
        try:
            gpt_output = query_openai(line)
        except Exception as e:
            gpt_output = e
        
        return redirect(url_for('scanned', algo=algorithm_output, gpt = gpt_output))
    

    return render_template("index.html",)


@app.route("/scanned")
def scanned():
    """page to display final scansion of inputed line"""
    return render_template("scanned.html", algorithm_scansion=request.args.get('algo'), gpt_scansion=request.args.get('gpt'))


