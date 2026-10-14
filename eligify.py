import sqlite3
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "48d90b04a573c33480b595e2294a1e285351894b48b5e874ff9475ea88479279"
DB = "opportunities.db"

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def setup():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, type TEXT, class_min INTEGER, class_max INTEGER,
        stream TEXT, state TEXT, gender TEXT, cost TEXT,
        deadline TEXT, official_link TEXT, note TEXT, last_verified TEXT)""")
    con.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        cls TEXT, stream TEXT, state TEXT, gender TEXT DEFAULT 'Any')""")
    
    con.commit()
    con.close()

def current_user():
    if "user_id" not in session:
        return None
    con = db()
    u = con.execute("SELECT * FROM users WHERE id = ?",
                    (session["user_id"],)).fetchone()
    con.close()
    return u

@app.route("/")
def home():
    user = current_user()

    if user:
        # Logged in: profile decides everything, URL filters are ignored
        cls = user["cls"] or ""
        stream = user["stream"] or ""
        state = user["state"] or ""
        gender = user["gender"] or "Any"
    else:
        cls = request.args.get("cls", "")
        stream = request.args.get("stream", "")
        state = request.args.get("state", "").strip()
        gender = ""

    query = "SELECT * FROM opportunities WHERE 1=1"
    params = []
    if cls:
        if cls.isdigit():
            query += " AND class_min <= ? AND class_max >= ?"
            params += [int(cls), int(cls)]
        else:  # UG or PG
            query += " AND class_min = ?"
            params.append(cls)
    if stream and cls in ("11", "12"):
        query += " AND (stream = ? OR stream = 'Any')"
        params.append(stream)
    if state:
        query += " AND (state = ? OR state = 'All India')"
        params.append(state)
    if gender:
        query += " AND (gender = ? OR gender = 'Any')"
        params.append(gender)
    query += " ORDER BY id"
    con = db()
    items = con.execute(query, params).fetchall()
    con.close()

    profile_incomplete = bool(user) and not (cls and stream and state)
    return render_template("index.html", items=items, user=user,
                           cls=cls, stream=stream, state=state,
                           profile_incomplete=profile_incomplete)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if len(username) < 3 or len(password) < 6:
            flash("Username needs 3+ characters and password 6+.")
            return render_template("register.html")

        gender = request.form.get("gender", "Any")
        if gender not in ("Female", "Male", "Any"):
            gender = "Any"
        cls = request.form.get("cls", "")
        if cls in ("11", "12"):
            stream = request.form.get("stream", "")
        else:
            stream = request.form.get("course", "").strip()[:100]
        con = db()
        try:
            con.execute(
                "INSERT INTO users (username,password_hash,cls,stream,state,gender) "
                "VALUES (?,?,?,?,?,?)",
                (username, generate_password_hash(password),
                 cls, stream,
                 request.form.get("state", "").strip(), gender))
            con.commit()
        except sqlite3.IntegrityError:
            con.close()
            flash("That username is taken. Try another.")
            return render_template("register.html")
        con.close()
        flash("Account created. Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        con = db()
        u = con.execute("SELECT * FROM users WHERE username = ?",
                        (username,)).fetchone()
        con.close()
        if u and check_password_hash(u["password_hash"], password):
            session.clear()
            session["user_id"] = u["id"]
            session["username"] = u["username"]
            return redirect(url_for("home"))
        flash("Wrong username or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    if request.method == "POST":
        gender = request.form.get("gender", user["gender"] or "Any")
        if gender not in ("Female", "Male", "Any"):
            gender = "Any"
        cls = request.form.get("cls", "")
        if cls in ("11", "12"):
            stream = request.form.get("stream", "")
        else:
            stream = request.form.get("course", "").strip()[:100]
        con = db()
        con.execute("UPDATE users SET cls=?, stream=?, state=?, gender=? WHERE id=?",
                    (cls, stream,
                     request.form.get("state", "").strip(),
                     gender,
                     user["id"]))
        con.commit()
        con.close()
        flash("Profile updated.")
        return redirect(url_for("home"))
    return render_template("profile.html", user=user)


setup()
app.run(debug=True, use_reloader=False)
