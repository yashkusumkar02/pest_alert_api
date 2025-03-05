from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__, template_folder="templates")  # Ensure templates folder is set
CORS(app)

# Load Pest Alert Data
data_file = os.path.join(os.path.dirname(__file__), "data/pest_data.json")

try:
    with open(data_file, "r") as file:
        pest_data = json.load(file)
except Exception as e:
    pest_data = []
    print(f"Error loading pest data: {e}")

@app.route("/")
def home():
    return render_template("index.html")  # ✅ Render Homepage

@app.route("/pest-alerts")
def get_pest_alerts():
    return jsonify(pest_data)  # ✅ Returns JSON API

@app.route("/pest-alerts/html")
def pest_alerts_html():
    return render_template("alerts.html", alerts=pest_data)  # ✅ Render alerts.html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render assigns a dynamic port
    app.run(host="0.0.0.0", port=port, debug=False)
