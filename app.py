from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# ✅ Load Pest Alert Data from CSV
data_file = os.path.join(os.path.dirname(__file__), "data/Real-Time_Crop_Pest_Data.csv")

try:
    pest_data = pd.read_csv(data_file).to_dict(orient="records")  # Convert CSV to List of Dicts
except Exception as e:
    pest_data = []
    print(f"❌ Error loading pest data: {e}")

@app.route("/")
def home():
    return render_template("index.html")  # ✅ Render Homepage

@app.route("/pest-alerts")
def get_pest_alerts():
    state = request.args.get("state")
    crop = request.args.get("crop")

    filtered_data = pest_data

    # ✅ Apply Filtering (if state or crop is provided)
    if state:
        filtered_data = [p for p in filtered_data if p["location"].lower() == state.lower()]
    if crop:
        filtered_data = [p for p in filtered_data if crop.lower() in p["crops"].lower()]

    return jsonify(filtered_data)

@app.route("/pest-alerts/html")
def pest_alerts_html():
    state = request.args.get("state")
    crop = request.args.get("crop")

    filtered_data = pest_data

    if state:
        filtered_data = [p for p in filtered_data if p["location"].lower() == state.lower()]
    if crop:
        filtered_data = [p for p in filtered_data if crop.lower() in p["crops"].lower()]

    return render_template("alerts.html", alerts=filtered_data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
