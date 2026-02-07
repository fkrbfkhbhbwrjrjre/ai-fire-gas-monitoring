from flask import Flask, render_template, jsonify
import random
from collections import deque

app = Flask(__name__)

# Store last 20 RAW risk values
raw_risk_history = deque(maxlen=20)

# Store last 20 SMOOTHED risk values
smoothed_risk_history = deque(maxlen=20)


# ---------------- AI RISK CALCULATION ----------------
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

    return min(risk, 100)


def smooth_risk():
    if len(raw_risk_history) == 0:
        return 0
    return int(sum(raw_risk_history) / len(raw_risk_history))


def risk_level(risk):
    if risk < 30:
        return "LOW"
    elif risk < 60:
        return "MEDIUM"
    else:
        return "HIGH"


# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/demo")
def demo():
    temp = random.randint(25, 60)
    gas = random.randint(150, 600)
    flame = random.choice([0, 1])

    raw_risk = calculate_risk(temp, gas, flame)
    raw_risk_history.append(raw_risk)

    smooth = smooth_risk()
    smoothed_risk_history.append(smooth)

    return jsonify({
        "temperature": temp,
        "gas": gas,
        "flame": flame,
        "risk_percentage": smooth,
        "risk_level": risk_level(smooth)
    })


@app.route("/risk-history")
def risk_history():
    return jsonify(list(smoothed_risk_history))
