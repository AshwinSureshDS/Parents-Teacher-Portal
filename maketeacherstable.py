import sqlite3

# Connect to the database
conn = sqlite3.connect('tiny_wonders.db')
cursor = conn.cursor()

# Create the teachers table
cursor.execute('''
CREATE TABLE teachers (
    username TEXT NOT NULL,
    teacher_id TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    user_type TEXT NOT NULL
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()