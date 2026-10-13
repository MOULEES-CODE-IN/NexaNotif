# NexaNotif: AI-Based Smart Notification Management System

NexaNotif classifies notifications by category and priority using machine learning,
blocks duplicates, applies quiet-hours rules, and learns from user feedback.

## Features
- Category prediction (work, personal, social, promotion, alert)
- Priority prediction (Important / Normal / Low) using TF-IDF + Naive Bayes
- Duplicate detection using cosine similarity
- Delivery rules: Delivered, Digest, or Blocked (with quiet hours)
- User feedback loop: corrections are saved and used when retraining
- Web dashboard built with Flask, HTML, CSS, and JavaScript

## Tech Stack
Python, Flask, scikit-learn, pandas, joblib, HTML/CSS/JavaScript

## Project Structure
```
nexanotif/
├── data/generate_data.py   # creates the training dataset
├── model/train.py          # trains and saves the models
├── templates/index.html    # dashboard UI
├── preprocess.py           # text cleaning
├── app.py                  # Flask backend
└── requirements.txt
```

## How to Run
```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate data and train the models
python data/generate_data.py
python model/train.py

# 4. Start the app
python app.py
```
Open http://127.0.0.1:5000 in your browser.

## How It Works
User notification, then Flask API, then text preprocessing + TF-IDF, then Naive Bayes
classifiers (category and priority), then duplicate check, then delivery rules, then
status (Delivered / Digest / Blocked), then dashboard. User feedback is saved to
`data/feedback.csv` and used when the models are retrained.

## Note
The dataset is synthetic and template-based, so accuracy is near perfect. It validates
the pipeline; real-world performance would need a real labeled dataset.
