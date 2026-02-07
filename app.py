from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# ---- Simple AI Risk Prediction Logic ----
def calculate_risk(temp, gas, flame):
    risk = 0

    if temp > 40:
        risk += 30
    if gas > 400:
        risk += 40
    if flame == 1:
        risk += 30

    if risk >= 70:
        level = "HIGH"
    elif risk >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return risk, level


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    temp = data.get("temperature", 25)
    gas = data.get("gas", 200)
    flame = data.get("flame", 0)

    risk, level = calculate_risk(temp, gas, flame)

    return jsonify({
        "risk_percentage": risk,
        "risk_level": level
    })


# ---- Demo Data Route (for testing without Arduino) ----
@app.route("/demo")
def demo():
    temp = random.randint(25, 60)
    gas = random.randint(150, 600)
    flame = random.choice([0, 1])

    risk, level = calculate_risk(temp, gas, flame)

    return jsonify({
        "temperature": temp,
        "gas": gas,
        "flame": flame,
        "risk_percentage": risk,
        "risk_level": level
    })


if __name__ == "__main__":
    app.run(debug=True)
