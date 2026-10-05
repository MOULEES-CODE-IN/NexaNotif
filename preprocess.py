import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\d+", " num ", text)   # numbers like OTPs become one token
    text = re.sub(r"[^a-z\s]", " ", text)  # remove punctuation and symbols
    return re.sub(r"\s+", " ", text).strip()