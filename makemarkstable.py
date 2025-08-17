import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('tiny_wonders.db')
cursor = conn.cursor()

# Create the timetable table
cursor.execute('''
CREATE TABLE report_card (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT NOT NULL,
    subject TEXT NOT NULL,
    marks INTEGER NOT NULL
);
''')


# Commit and close connection
conn.commit()
conn.close()

print("Timetable table created successfully with empty slots!")
