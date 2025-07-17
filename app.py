from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)
CORS(app)

# Set scope & auth using credentials.json
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the correct Google Sheet by name (must match)
sheet = client.open("Student_CV_Data").sheet1

@app.route("/submit", methods=["POST"])
def submit_data():
    data = request.json

    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    skills = data.get("skills", "")

    # Add to Google Sheet
    sheet.append_row([name, email, phone, skills])

    return jsonify({"message": "🎉 Data saved to Google Sheet!"}), 200

# Required config for Render.com deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render assigns dynamic ports
    app.run(host="0.0.0.0", port=port, debug=True)