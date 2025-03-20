from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# Path to the dataset
CSV_FILE = os.path.join(os.path.dirname(__file__), "data", "Real-Time_Crop_Disease_Dataset.csv")

# ✅ Function to load pest alerts from CSV
def load_pest_data():
    try:
        df = pd.read_csv(CSV_FILE)
        alerts = df.to_dict(orient="records")  # Convert DataFrame to list of dicts
        return alerts
    except Exception as e:
        print(f"❌ Error loading pest data: {e}")
        return []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/pest-alerts")
def get_pest_alerts():
    alerts = load_pest_data()
    return jsonify(alerts)  # ✅ Returns JSON API

@app.route("/pest-alerts/html")
def pest_alerts_html():
    alerts = load_pest_data()
    return render_template("alerts.html", alerts=alerts, total_alerts=len(alerts))  # ✅ Render with total count

@app.route("/search")
def search_alerts():
    state = request.args.get("state", "").strip().lower()
    crop = request.args.get("crop", "").strip().lower()
    
    alerts = load_pest_data()
    
    # ✅ Filter based on state or crop if provided
    if state:
        alerts = [alert for alert in alerts if state in alert["state"].lower()]
    if crop:
        alerts = [alert for alert in alerts if crop in alert["crops"].lower()]

    return render_template("alerts.html", alerts=alerts, total_alerts=len(alerts))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
