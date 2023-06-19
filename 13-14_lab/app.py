import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect("data.db")
c = conn.cursor()

# Create the table
c.execute(
    """
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        context TEXT,
        knowledge TEXT,
        response TEXT
    )
"""
)

# Load the data from the JSON file
with open("data.json", "r") as f:
    data = json.load(f)

# Insert the data into the table
for item in data:
    c.execute(
        "INSERT INTO data (context, knowledge, response) VALUES (?, ?, ?)",
        (item["Context"], item["Knowledge"], item["Response"]),
    )

# Commit the changes and close the connection
conn.commit()
conn.close()
