from flask import Flask, flash, redirect, render_template, request, session
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


@app.route("/")
def index():
    """Show portfolio of stocks and add money to account"""
    if request.method == "POST":
        #get scansion.
        #redirect to scansion page, with template filled with scansion stuff
        pass
    

    return render_template("index.html",)


