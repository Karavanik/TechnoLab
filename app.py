import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import db

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-change-me")
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
        email = request.form.get("email", "").strip().lower()
        haslo = request.form.get("haslo", "")
        user = db.get_db().execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], haslo):
            flash("Nieprawidłowy email lub hasło.", "error")
            return render_template("logowanie.html"), 401

        session.clear()
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        session["imie"] = user["imie"]
        return redirect(url_for("serwis" if user["role"] == "serwis" else "klient"))
    return render_template("logowanie.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Wylogowano.", "success")
    return redirect(url_for("login"))


def validate_password(haslo):
    """Zwraca listę błędów hasła (pusta lista = hasło poprawne)."""
    errors = []
    if len(haslo) < 8:
        errors.append("Hasło musi mieć co najmniej 8 znaków.")
    if not any(c.isdigit() for c in haslo):
        errors.append("Hasło musi zawierać cyfrę.")
    if not any(c.isupper() for c in haslo):
        errors.append("Hasło musi zawierać wielką literę.")
    return errors


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        imie = request.form.get("imie", "").strip()
        email = request.form.get("email", "").strip().lower()
        haslo = request.form.get("haslo", "")

        errors = []
        if not imie:
            errors.append("Podaj imię.")
        if not email:
            errors.append("Podaj email.")
        errors += validate_password(haslo)

        if not errors:
            try:
                database = db.get_db()
                database.execute(
                    "INSERT INTO users (imie, email, password_hash) VALUES (?, ?, ?)",
                    (imie, email, generate_password_hash(haslo)),
                )
                database.commit()
            except sqlite3.IntegrityError:
                errors.append("Konto z tym adresem email już istnieje.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("rejestracja.html", imie=imie, email=email)

        flash("Konto zostało utworzone. Możesz się zalogować.", "success")
        return redirect(url_for("login"))
    return render_template("rejestracja.html")


@app.route("/klient")
def klient():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("klient.html")


@app.route("/zgloszenie")
def zgloszenie():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("zgloszenie.html")


@app.route("/serwis")
def serwis():
    if session.get("role") != "serwis":
        return redirect(url_for("login"))
    return render_template("serwis.html")


if __name__ == "__main__":
    app.run(port=8080, debug=True)