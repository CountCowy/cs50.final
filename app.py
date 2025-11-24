from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from scanner import takeit
from JePeux import query_openai
import os
import sqlite3
from labienus import apology, login_required

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



custom_template_path = os.path.join(os.path.dirname(__file__), 'pantheon')
app = Flask(__name__, template_folder=custom_template_path)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#database connection
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("widener.db")
        g.db.row_factory = sqlite3.Row
    return g.db
def init_db():
    db = get_db()
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    email TEXT NOT NULL);
    """)#note that we dont have any email confirmation yet
    db.executescript("""
    CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER NOT NULL,
    input_line TEXT NOT NULL,
    algorithm_scan TEXT NOT NULL,
    gpt_scan TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id));
    """)
    
with app.app_context():
    init_db()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """page to input line of poetry"""
    if request.method == "POST":
        db = get_db()
        mouse = db.cursor()
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
        
        mouse.execute(
        "INSERT INTO history (user_id, input_line, algorithm_scan, gpt_scan) VALUES (?, ?, ?, ?)",
        (session["user_id"], line, session['algo'], session['gpt'])
        )
        conn.commit()
        
        return redirect(url_for('scanned'))
    

    return render_template("index.html",)


@app.route("/scanned")
@login_required
def scanned():
    """page to display final scansion of inputed line"""
    algo = session.pop('algo')
    gpt = session.pop('gpt')
    return render_template("scanned.html", algorithm_scansion=algo, gpt_scansion=gpt)

@app.route("/register", methods=["GET", "POST"])
def register():
    """user registration page"""
    if request.method == "POST":
        db = get_db()
        mouse = db.cursor()
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
        print(rows)
        if len(rows):
            return apology("username already exists", 403)
        
        hashedpass = generate_password_hash(request.form.get("password"))
        mouse.execute(
            "INSERT INTO users (username, hash, email) VALUES (?, ?, ?)", (usrname, hashedpass, email)
        )
        
        conn.commit()

        mouse.execute(
            "SELECT * FROM users WHERE username = ?", (usrname,)
        )
        rows = mouse.fetchall()
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        print(session["user_id"], "ID2")
        return redirect("/")

    return render_template("register.html")

"""cur.execute(
    "INSERT INTO logs (user, action) VALUES (:user, :action)",
    {"user": username, "action": action} - another option
)"""


@app.route("/login", methods=["GET", "POST"])
def login():
    """user log in page"""
    if request.method == "POST":
        usrname = request.form.get("username")
        
        if not usrname:
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        mouse.execute(
            "SELECT * FROM users WHERE username = ?", (usrname,)
        )
        rows = mouse.fetchall()
        print(rows)
        if not len(rows) or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403) #language stolen cs50 finance

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/history")
@login_required
def history():
    db = get_db()
    mouse = db.cursor()
    scans = mouse.execute(
        "SELECT * FROM history WHERE user_id = ? ORDER BY timestamp DESC",
        (session["user_id"],)
    ).fetchall()
    
    print("hi")

    return render_template("history.html", scans=scans)

@app.route("/scan/<int:scan_id>")
@login_required
def view_scan(scan_id):
    db = get_db()
    mouse = db.cursor()
    scan = mouse.execute(
        "SELECT * FROM history WHERE id = ? AND user_id = ?",
        (scan_id, session["user_id"],)
    ).fetchone()

    if scan is None:
        return apolgy("This scan doesn't exist", 404)

    return render_template("hitscan.html", scan=scan)


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()
