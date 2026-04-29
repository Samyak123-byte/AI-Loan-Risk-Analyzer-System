from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ------------------- DATABASE SETUP -------------------

def create_table():
    conn = sqlite3.connect("loan.db")
    cursor = conn.cursor()

    # Loan table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        income REAL,
        loan REAL,
        result TEXT,
        date TEXT
    )
    """)

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_default_users():
    conn = sqlite3.connect("loan.db")
    cursor = conn.cursor()

    users = [
        ("admin", "admin123", "admin"),
        ("officer", "officer123", "officer"),
        ("user", "user123", "user")
    ]

    for user in users:
        cursor.execute("SELECT * FROM users WHERE username=?", (user[0],))
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                user
            )

    conn.commit()
    conn.close()


# 🔥 Initialize DB
create_table()
insert_default_users()

# ------------------- LOAD MODEL -------------------

model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# ------------------- SAVE DATA -------------------

def save_data(income, loan_amount, result):
    conn = sqlite3.connect("loan.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO loans (income, loan, result, date) VALUES (?, ?, ?, ?)",
        (income, loan_amount, result, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )

    conn.commit()
    conn.close()

# ------------------- LOGIN -------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("loan.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT role FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            session["role"] = user[0]

            # 🔥 Role-based redirect
            if user[0] == "admin":
                return redirect(url_for("dashboard"))
            elif user[0] == "officer":
                return redirect(url_for("officer"))
            else:
                return redirect(url_for("apply"))

        else:
            return render_template("login.html", error="Invalid Credentials ❌")

    return render_template("login.html")

# ------------------- LOGOUT -------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ------------------- HOME -------------------

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")

# ------------------- OFFICER PAGE -------------------

@app.route("/officer")
def officer():
    if "user" not in session or session.get("role") != "officer":
        return redirect(url_for("login"))

    return render_template("officer.html")

# ------------------- USER APPLY PAGE -------------------

@app.route("/apply")
def apply():
    if "user" not in session or session.get("role") != "user":
        return redirect(url_for("login"))

    return render_template("apply.html")

# ------------------- PREDICTION -------------------

@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))

    try:
        gender = int(request.form["gender"])
        married = int(request.form["married"])
        age = int(request.form["age"])
        employment = int(request.form["employment"])
        property_area = int(request.form["property_area"])
        income = float(request.form["income"])
        loan_amount = float(request.form["loan_amount"])
        credit_history = int(request.form["credit_history"])

        features = np.array([[gender, married, age, employment, property_area,
                              income, loan_amount, credit_history]])

        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]

        if prediction == 1:
            result = "Loan Approved ✅"
        else:
            result = "Loan Rejected ❌"

        # Save data
        save_data(income, loan_amount, result)

        # Explanation logic
        reasons = []

        if credit_history == 0:
            reasons.append("Poor Credit History")

        if income < 3000:
            reasons.append("Low Income")

        if loan_amount > income * 0.5:
            reasons.append("Loan too High vs Income")

        if age < 21:
            reasons.append("Applicant too young")

        reason_text = "Strong Profile" if not reasons else ", ".join(reasons)

        return render_template(
            "index.html",
            prediction_text=result,
            prob_text=f"Approval Probability: {probability*100:.2f}%",
            reason_text=reason_text
        )

    except Exception:
        return render_template(
            "index.html",
            prediction_text="Error ❌",
            prob_text="Try again",
            reason_text="Invalid input"
        )

# ------------------- DASHBOARD -------------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("login"))

    conn = sqlite3.connect("loan.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM loans")
    data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM loans")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM loans WHERE result='Loan Approved ✅'")
    approved = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM loans WHERE result='Loan Rejected ❌'")
    rejected = cursor.fetchone()[0]

    conn.close()

    # Chart data
    chart_labels = ["Approved", "Rejected"]
    chart_values = [approved, rejected]

    return render_template(
        "dashboard.html",
        data=data,
        total=total,
        approved=approved,
        rejected=rejected,
        chart_labels=chart_labels,
        chart_values=chart_values
    )

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message").lower()

    # 🔥 Simple rule-based chatbot
    if "loan" in message:
        reply = "To get a loan approved, maintain good credit history and stable income."

    elif "credit" in message:
        reply = "Credit history is very important. A good credit score increases approval chances."

    elif "income" in message:
        reply = "Higher income improves your chances of loan approval."

    elif "rejected" in message:
        reply = "Your loan may be rejected due to low income, poor credit history, or high loan amount."

    elif "approved" in message:
        reply = "Your loan is approved because you have a strong financial profile."

    else:
        reply = "I can help with loan advice, credit score, and approval tips."

    return {"reply": reply}


# ------------------- RUN -------------------

if __name__ == "__main__":
    app.run(debug=True)