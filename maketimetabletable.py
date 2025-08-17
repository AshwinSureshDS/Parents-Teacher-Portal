import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('tiny_wonders.db')
cursor = conn.cursor()

# Create the timetable table
cursor.execute('''
CREATE TABLE IF NOT EXISTS timetable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time_slot TEXT,
    monday TEXT,
    tuesday TEXT,
    wednesday TEXT,
    thursday TEXT,
    friday TEXT,
    saturday TEXT
)
''')

# Insert sample data (empty initially)
time_slots = [
    "9:00 - 9:45",
    "9:45 - 10:30",
    "10:30 - 11:15",
    "11:15 - 12:00",
    "12:00 - 12:45",
    "12:45 - 1:30",
    "1:30 - 2:15",
    "2:15 - 3:00"
]

for slot in time_slots:
    cursor.execute("INSERT INTO timetable (time_slot) VALUES (?)", (slot,))

# Commit and close connection
conn.commit()
conn.close()

print("Timetable table created successfully with empty slots!")
