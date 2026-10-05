import random
import pandas as pd

random.seed(42)

names = ["Arun", "Priya", "Karthik", "Divya", "Rahul", "Meena", "Sanjay"]
projects = ["Sales", "Website", "Mobile App", "Finance", "Electronics", "Fashion"]
times = ["10 AM", "2 PM", "4:30 PM", "11 AM"]

# (template, category, priority)
templates = [
    ("Meeting with {n} starts in 15 minutes", "work", "high"),
    ("Deadline for {p} report is today", "work", "high"),
    ("{n} assigned you a task in {p}", "work", "medium"),
    ("Please review the pull request from {n}", "work", "medium"),
    ("Client call rescheduled to {t}", "work", "medium"),
    ("{n} sent you a message", "personal", "medium"),
    ("Missed call from {n}", "personal", "high"),
    ("{n}: are you coming for dinner?", "personal", "medium"),
    ("Reminder: {n}'s birthday is today", "personal", "medium"),
    ("{n} liked your photo", "social", "low"),
    ("{n} started following you", "social", "low"),
    ("{n} commented on your post", "social", "low"),
    ("You have 5 new friend suggestions", "social", "low"),
    ("Flat 50% off on {p} today only", "promotion", "low"),
    ("Your coupon expires tonight, shop now", "promotion", "low"),
    ("New arrivals in {p} just for you", "promotion", "low"),
    ("Big sale: buy 1 get 1 free on {p}", "promotion", "low"),
    ("Your OTP is {o}. Do not share it", "alert", "high"),
    ("Rs {o} debited from your account", "alert", "high"),
    ("Security alert: new login detected", "alert", "high"),
    ("Battery low, 10% remaining", "alert", "medium"),
    ("Your package is out for delivery", "alert", "medium"),
]

rows = []
for _ in range(1500):
    t, cat, pri = random.choice(templates)
    text = t.format(
        n=random.choice(names),
        p=random.choice(projects),
        t=random.choice(times),
        o=random.randint(1000, 99999),
    )
    rows.append({"text": text, "category": cat, "priority": pri})

pd.DataFrame(rows).to_csv("data/notifications.csv", index=False)
print("Created data/notifications.csv with", len(rows), "rows")