import sqlite3

# Connect to your database
conn = sqlite3.connect('tiny_wonders.db')
cursor = conn.cursor()

# Add 'class' column to the report_card table
try:
    cursor.execute("ALTER TABLE report_card ADD COLUMN class TEXT")
    print("✅ Column 'class' added successfully.")
except sqlite3.OperationalError:
    print("⚠️ Column 'class' might already exist or there's an issue.")

# Commit and close the connection
conn.commit()
conn.close()
