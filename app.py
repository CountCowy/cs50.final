from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from scanner import takeit
from JePeux import query_openai
import os
import sqlite3



#plan
#get input n shi working, basic home page with form, jinja blah
# - separate feet in the algorythm, count how many entires of long'd or shorted vowels have appeared, then put a || at the end of that word or whatever
#do it with gpt
#flask index
#- history page, instruction on how to scan, support/contact page with credits
#registering and log in feature
#user settings
#- maybe add a toggle for gpt ooutput, darkmode, maybe have onboarding for demographics like why you're using this, teacher/student etc. 
#database to store previous inputs, user info etc.
#admin panel?

conn = sqlite3.connect("widener.db")
mouse = conn.cursor()
mouse.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT NOT NULL);
    """)#note that we dont have any email confirmation yet


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
            
        session['algo'] = algorithm_output
        session['gpt'] = gpt_output
        
        return redirect(url_for('scanned'))
    

    return render_template("index.html",)


@app.route("/scanned")
def scanned():
    """page to display final scansion of inputed line"""
    algo = session.pop('algo')
    gpt = session.pop('gpt')
    return render_template("scanned.html", algorithm_scansion=algo, gpt_scansion=gpt)

@app.route("/register", methods=["GET", "POST"])
def register():
    """user registration page"""
    if request.method == "POST":
        usrname = request.form.get("username")
        email = request.form.get("email")
        
        if not usrname:
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        elif request.form.get("password") != request.form.get("confirm"):
            return apology("passwords do not match", 403)
        
        mouse.execute(
            "SELECT * FROM users WHERE username = ?", (usrname,)
        )
        rows = mouse.fetchall()
        if len(rows):
            return apology("username already exists", 403)
        
        hashedpass = generate_password_hash(request.form.get("password"))
        mouse.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, hashedpass
        )

        rows = mouse.execute(
            "SELECT * FROM users WHERE username = ?", username
        )
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")

    return render_template("register.html")

"""cur.execute(
    "INSERT INTO logs (user, action) VALUES (:user, :action)",
    {"user": username, "action": action} - another option
)"""




def apology(message, code=400): #stolen completely from cs50 finance
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code