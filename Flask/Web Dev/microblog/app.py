import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv() 


app = Flask(__name__)
client = MongoClient(os.environ.get("MONGODB_URI"))
app.db = client.get_default_database()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        entry_content = request.form.get("content")
        formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        # Get top 3 recent entries, sorted by date in descending order
    entries_with_date = [
        (
            entry["content"],
            entry["date"],                
            datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
        )
        for entry in app.db.entries.find({}).sort([("date", -1), ("_id", -1)]).limit(3) # Sort by date descending and limit to 3
    ]
    return render_template("home.html", entries=entries_with_date)

