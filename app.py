from flask import Flask, render_template, jsonify
import random
from collections import deque

app = Flask(__name__)

# Store last 20 risk values
risk_history = deque(maxlen=20)

# AI-based risk calculation (rule-based intelligence)
def calculate_risk(temp, gas, flame):
    risk = 0

    if temp > 50:
        risk += 30
    elif temp > 35:
        risk += 15

    if gas > 400:
        risk += 40
    elif gas > 250:
        risk += 20

    if flame == 1:
        risk += 50

    risk = min(risk, 100)

    if risk < 30:
        level = "LOW"
    elif risk < 60:
        level = "MEDIUM"
    else:
        level = "HIGH"

    return risk, level


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/demo")
def demo():
    temp = random.randint(25, 60)
    gas = random.randint(150, 600)
    flame = random.choice([0, 1])

    risk, level = calculate_risk(temp, gas, flame)

    risk_history.append(risk)

    return jsonify({
        "temperature": temp,
        "gas": gas,
        "flame": flame,
        "risk_percentage": risk,
        "risk_level": level
    })


@app.route("/risk-history")
def risk_history_api():
    return jsonify(list(risk_history))

