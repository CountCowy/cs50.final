from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from scanner import takeit
from JePeux import query_openai
import os
from labienus import apology, login_required
from supabase import create_client, Client

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
app.secret_key = os.environ.get("SECRET_KEY", "devsecretkey")


app.started = False
@app.before_request
def clear_session_on_start():
    if not app.started:
        session.clear()
        app.started = True
        

supabase_url = os.environ.get("SUPABASE_URL")
supabase_api_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_api_key)

    
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
        
        data = {
            "user_id": session["user_id"],
            "input_line": line,
            "algorithm_scan": session["algo"],
            "gpt_scan": session["gpt"],
        }
        
        try:
            response = supabase.table("history").insert(data).execute()
        except APIError as e:
            print("Supabase error:", e)
            return apology("Database error: " + e, 500)
        
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
        usrname = request.form.get("username")
        email = request.form.get("email")
        
        if not usrname:
            return apology("must provide username", 403)
        if not usrname:
            return apology("must provide email", 403)
        if not request.form.get("password"):
            return apology("must provide password", 403)
        if request.form.get("password") != request.form.get("confirm"):
            return apology("passwords do not match", 403)
        
        
        #check username
        response = supabase.table("profiles").select("*").eq("username", usrname).execute()

        if len(response.data):
            return apology("username already exists", 403)
        
        redirect_url = request.host_url.rstrip("/") + "/login"
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": request.form.get("password"),
                "options": {
                    "data": {"username": usrname}, #goes to metadata
                    "email_redirect_to": redirect_url}
            })
        except Exception as e:
            flash("Registration failed:", e)
            return redirect(url_for("register"))
        
        
        flash("Account created! Check your email to confirm before logging in.")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """user log in page"""
    
    session.clear()

    if request.method == "POST":
        
        if not request.form.get("email"):
            return apology("must provide email", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        try:
            response = supabase.auth.sign_in_with_password({
                "email": request.form.get("email"),
                "password": request.form.get("password")
            })
        except Exception as e:
            print(e)
            return apology("invalid email/password", 403)

        user = response.user
        if user is None:
            print("no user")
            return apology("invalid email/password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id
        session["email"] = request.form.get("email")        
    
        #get username
        response = supabase.table("profiles").select("*").eq("id", session["user_id"]).execute()
        session["username"] = response.data[0]["username"]
        print(session["username"])


            
        # Redirect user to home page
        flash("Logged in successfully")
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
    scans_response = (
    supabase
    .table("history")
    .select("*")
    .eq("user_id", session["user_id"])
    .order("timestamp", desc=True)
    .execute())
    
    return render_template("history.html", scans=scans_response.data)

@app.route("/scan/<int:scan_id>")
@login_required
def view_scan(scan_id):
    scans_response = (
    supabase
    .table("history")
    .select("*")
    .eq("id", scan_id)
    .eq("user_id", session["user_id"])
    .single()
    .execute())

    if scans_response.data is None:
        return apolgy("This scan doesn't exist", 404)

    return render_template("hitscan.html", scan=scans_response.data)

@app.route("/instructions")
@login_required
def instructions():
    
    return render_template("instructions.html")
        
        
@app.route("/auth/confirmed")
def auth_confirmed():
    # Supabase sends a verification access_token in the URL
    access_token = request.args.get("access_token")

    if not access_token:
        return apology("Missing confirmation token", 400)

    # Now exchange the token for a session
    session_response = supabase.auth.exchange_code_for_session(access_token)
    
    user = session_response.user

    if not user:
        return apology("Invalid or expired confirmation link.", 400)
    
    
    # Store user info in Flask session
    session["user_id"] = user.id               # Supabase UUID
    session["email"] = user.email
    session["username"] = user.user_metadata.get("username")

    # Optionally store tokens if you want auto-refresh
    session["access_token"] = supa_session.access_token
    session["refresh_token"] = supa_session.refresh_token
    
    return redirect("/")
