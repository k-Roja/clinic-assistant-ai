import sqlite3
from flask import Flask, render_template, request, redirect
from triage import get_triage

app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("clinic.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS appointments ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, "
        "phone TEXT NOT NULL, "
        "date TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        date = request.form["date"]
        conn = get_db()
        conn.execute(
            "INSERT INTO appointments (name, phone, date) VALUES (?, ?, ?)",
            (name, phone, date),
        )
        conn.commit()
        conn.close()
        return redirect("/appointments")
    return render_template("book.html")


@app.route("/appointments")
def appointments():
    conn = get_db()
    rows = conn.execute("SELECT * FROM appointments ORDER BY date").fetchall()
    conn.close()
    return render_template("appointments.html", appointments=rows)


@app.route("/triage", methods=["GET", "POST"])
def triage():
    result = None
    symptoms = ""
    if request.method == "POST":
        symptoms = request.form["symptoms"]
        result = get_triage(symptoms)
    return render_template("triage.html", result=result, symptoms=symptoms)


init_db()

if __name__ == "__main__":
    app.run(debug=True)