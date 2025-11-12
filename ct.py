from db_connect import connect_db

conn = connect_db()
if conn:
    print("✅ Connected to MySQL successfully!")
    conn.close()
else:
    print("❌ Connection failed.")
