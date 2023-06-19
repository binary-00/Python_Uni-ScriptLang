import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("data.db")
c = conn.cursor()

# Query the database
c.execute("SELECT * FROM data LIMIT 23")
rows = c.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()
