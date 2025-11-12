# setup_database.py
import mysql.connector

# ---------- MySQL Configuration ----------
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASS = "tuffy"   # CHANGE THIS TO YOUR MYSQL PASSWORD

# ---------- Connect to MySQL (no database yet) ----------
def setup_db():
    try:
        cn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS
        )
        cur = cn.cursor()
        print("✅ Connected to MySQL Server")
    except mysql.connector.Error as err:
        print("❌ Connection failed:", err)
        exit()

    # ---------- Create database if not exists ----------
    cur.execute("CREATE DATABASE IF NOT EXISTS autocare;")
    print("✅ Database 'autocare' created or already exists")

    # ---------- Use the database ----------
    cur.execute("USE autocare;")

    # ---------- Create tables ----------

    # Customers Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        cust_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        phone VARCHAR(15),
        v_model VARCHAR(40),
        v_number VARCHAR(20)
    );
    """)
    print("✅ Table 'customers' created")

    # Services Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS services (
        serv_id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(30),
        serv_name VARCHAR(50),
        cost FLOAT
    );
    """)
    print("✅ Table 'services' created")

    # Billing Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS billing (
        bill_id INT AUTO_INCREMENT PRIMARY KEY,
        cust_id INT,
        services TEXT,
        total_amt FLOAT,
        bill_date DATETIME,
        FOREIGN KEY (cust_id) REFERENCES customers(cust_id)
    );
    """)
    print("✅ Table 'billing' created")

    # ---------- Insert Default Services ----------
    services_data = [
        # Exterior
        ("Exterior Detailing", "Car Wash", 700),
        ("Exterior Detailing", "Rubbing and Polishing", 2500),
        ("Exterior Detailing", "Ceramic Coating", 22000),
        ("Exterior Detailing", "Graphene Coating", 27000),
        ("Exterior Detailing", "PPF (Paint Protection Film)", 75000),
        ("Exterior Detailing", "Glass Ceramic", 7000),

        # Interior
        ("Interior Detailing", "Vacuum and Wash", 800),
        ("Interior Detailing", "Interior Restoration", 1800),
        ("Interior Detailing", "Basic Wash", 400),
        ("Interior Detailing", "Leather Protection", 1200),

        # Body Work
        ("Body Work", "Denting", 3000),
        ("Body Work", "Painting", 5000),
        ("Body Work", "Bumper Repair", 3500),
        ("Body Work", "Rust Treatment", 4500)
    ]

    # Check if services already exist
    cur.execute("SELECT COUNT(*) FROM services;")
    count = cur.fetchone()[0]

    if count == 0:
        cur.executemany("INSERT INTO services (category, serv_name, cost) VALUES (%s, %s, %s);", services_data)
        cn.commit()
        print("✅ Default services added")
    else:
        print("ℹ️ Services already exist, skipping insertion")

    # ---------- Wrap up ----------
    cur.close()
    cn.close()
    print("\n🎉 Database setup completed successfully!")