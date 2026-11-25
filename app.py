import os

from flask import Flask, redirect, render_template, request, url_for

import db

app = Flask(__name__)
os.makedirs(app.instance_path, exist_ok=True)
app.config["DATABASE"] = os.path.join(app.instance_path, "technolab.db")
db.init_app(app)

with app.app_context():
    db.init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # tymczasowo: na sztywno, zostanie zastąpione bazą danych
        if request.form.get("email") == "serwis@gmail.com" and request.form.get("haslo") == "1234":
            return redirect(url_for("serwis"))
        return redirect(url_for("index"))
    return render_template("logowanie.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # tymczasowo: nic nie zapisujemy, zostanie zastąpione bazą danych
        return redirect(url_for("index"))
    return render_template("rejestracja.html")


@app.route("/serwis")
def serwis():
    return render_template("serwis.html")


if __name__ == "__main__":
    app.run(port=8080, debug=True)