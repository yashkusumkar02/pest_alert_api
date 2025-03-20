from flask import Flask, request, jsonify, render_template
from flask_babel import Babel, _  # Import Babel for translations
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

# ✅ Configure available languages
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
babel = Babel(app)

# ✅ Detect User Language
@babel.localeselector
def get_locale():
    return request.args.get("lang", "en")  # Default to English if no language is selected

# ✅ Load Pest Alert Data from CSV
data_file = os.path.join(os.path.dirname(__file__), "data/Real-Time_Crop_Pest_Data.csv")
try:
    pest_data = pd.read_csv(data_file).to_dict(orient="records")  # Convert CSV to List of Dicts
except Exception as e:
    pest_data = []
    print(f"❌ Error loading pest data: {e}")

@app.route("/")
def home():
    return render_template("index.html", title=_("Pest Alert System"))

@app.route("/pest-alerts")
def get_pest_alerts():
    state = request.args.get("state")
    crop = request.args.get("crop")

    filtered_data = pest_data
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

    return render_template("alerts.html", alerts=filtered_data, title=_("Pest Alerts"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
