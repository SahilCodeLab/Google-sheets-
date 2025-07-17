from flask import Flask, request, jsonify
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from any frontend

# Setup Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Student_CV_Data").sheet1

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get("name"),
        data.get("email"),
        data.get("phone"),
        data.get("skills"),
        data.get("linkedin"),
        data.get("portfolio"),
        data.get("message")
    ]
    sheet.append_row(row)
    return jsonify({"status": "success", "message": "CV submitted successfully ✅"})

if __name__ == "__main__":
    app.run(debug=True)