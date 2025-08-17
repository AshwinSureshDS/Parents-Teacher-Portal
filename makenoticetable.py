"""import sqlite3

# Connect to the database
conn = sqlite3.connect('tiny_wonders.db')
cursor = conn.cursor()

# Create 'notices' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        date_posted TEXT NOT NULL
    )
''')

print("✅ 'notices' table created successfully!")

# Commit changes and close connection
conn.commit()
conn.close()
"""

from datetime import datetime
import sqlite3

# Connect to the database
conn = sqlite3.connect('tiny_wonders.db')
cursor = conn.cursor()

# Insert data with Python's datetime module
cursor.execute('''
    INSERT INTO notices (title, content, date_posted) 
    VALUES (?, ?, ?)
''', ('Title Example 2', 'This is one more content', datetime.now().strftime("%Y-%m-%d")))

conn.commit()
print("✅ Notice inserted successfully!")
conn.close()
