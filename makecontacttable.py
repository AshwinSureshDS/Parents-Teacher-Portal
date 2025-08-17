import sqlite3

# Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect('tiny_wonders.db')
cursor = conn.cursor()

# Create the timetable table
cursor.execute('''
CREATE TABLE contact_details (
    roll_no TEXT PRIMARY KEY,
    class TEXT,
    class_teacher TEXT,
    mother_name TEXT,
    mother_mobile TEXT,
    father_name TEXT,
    father_mobile TEXT,
    parent_email TEXT
);
''')


# Commit and close connection
conn.commit()
conn.close()

print("Contacts table created successfully with empty slots!")