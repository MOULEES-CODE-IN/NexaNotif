import csv
import datetime
import os

import joblib
from flask import Flask, jsonify, render_template, request
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import clean_text

app = Flask(__name__)

cat_model = joblib.load("model/category_model.pkl")
pri_model = joblib.load("model/priority_model.pkl")
vectorizer = cat_model.named_steps["tfidfvectorizer"]

PRIORITY_LABEL = {"high": "Important", "medium": "Normal", "low": "Low"}
QUIET_START, QUIET_END = 23, 7

inbox = []


def in_quiet_hours(hour):
    if QUIET_START > QUIET_END:
        return hour >= QUIET_START or hour < QUIET_END
    return QUIET_START <= hour < QUIET_END


def is_duplicate(text):
    if not inbox:
        return False
    recent = [clean_text(n["text"]) for n in inbox[-20:]]
    sims = cosine_similarity(
        vectorizer.transform([clean_text(text)]), vectorizer.transform(recent)
    )
    return sims.max() >= 0.85


def decide_status(priority, duplicate, hour):
    if duplicate:
        return "blocked"
    if priority == "low":
        return "digest"
    if in_quiet_hours(hour) and priority != "high":
        return "digest"
    return "delivered"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/notify", methods=["POST"])
def notify():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify(error="text is required"), 400

    hour = int(data.get("hour", datetime.datetime.now().hour))
    cleaned = clean_text(text)
    category = cat_model.predict([cleaned])[0]
    priority = pri_model.predict([cleaned])[0]
    duplicate = bool(is_duplicate(text))

    item = {
        "id": len(inbox) + 1,
        "app": data.get("app", "Unknown"),
        "text": text,
        "category": category,
        "priority": priority,
        "priority_label": PRIORITY_LABEL[priority],
        "duplicate": duplicate,
        "hour": hour,
        "status": decide_status(priority, duplicate, hour),
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
    }
    inbox.append(item)
    return jsonify(item)


@app.route("/api/notifications")
def notifications():
    return jsonify(list(reversed(inbox)))


@app.route("/api/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    item = next((n for n in inbox if n["id"] == data["id"]), None)
    if item is None:
        return jsonify(error="not found"), 404

    item["priority"] = data["priority"]
    item["priority_label"] = PRIORITY_LABEL[item["priority"]]
    item["status"] = decide_status(item["priority"], item["duplicate"], item["hour"])

    path = "data/feedback.csv"
    new_file = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["text", "category", "priority"])
        w.writerow([item["text"], item["category"], item["priority"]])
    return jsonify(item)


if __name__ == "__main__":
    app.run(debug=True)