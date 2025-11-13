from tkinter import *
from tkinter import messagebox
from connect_db import connect_db
import datetime

def dashboard_window():
    win = Toplevel()
    win.title("AutoCare Dashboard")
    win.geometry("700x500")
    win.config(bg="#F8FAFC")

    Label(win, text="AutoCare Dashboard", font=("Arial", 20, "bold"),
          bg="#F8FAFC", fg="#0A4D68").pack(pady=20)

    # Frame for stats
    frame = Frame(win, bg="#F8FAFC")
    frame.pack(pady=10)

    # Database connection
    conn = connect_db()
    if not conn:
        messagebox.showerror("Database Error", "Cannot connect to database.")
        return
    cur = conn.cursor()

    # ---- Fetch Data ----
    cur.execute("SELECT COUNT(*) FROM customers")
    total_customers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM billing")
    total_bills = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(total_amt), 0) FROM billing")
    total_revenue = cur.fetchone()[0]

    today = datetime.date.today().strftime("%Y-%m-%d")
    cur.execute("SELECT IFNULL(SUM(total_amt), 0) FROM billing WHERE DATE(bill_date) = %s", (today,))
    today_income = cur.fetchone()[0]

    cur.execute("""
        SELECT services, COUNT(*) AS count
        FROM billing
        GROUP BY services
        ORDER BY count DESC
        LIMIT 1
    """)
    top_service_row = cur.fetchone()
    most_popular = top_service_row[0] if top_service_row else "N/A"

    conn.close()

    # ---- Display Labels ----
    stat_style = {"font": ("Arial", 14, "bold"), "bg": "#E8F0F2", "fg": "#0A4D68", "width": 30, "pady": 10}
    Label(frame, text=f"Total Customers: {total_customers}", **stat_style).pack(pady=5)
    Label(frame, text=f"Total Bills: {total_bills}", **stat_style).pack(pady=5)
    Label(frame, text=f"Total Revenue: ₹{total_revenue}", **stat_style).pack(pady=5)
    Label(frame, text=f"Today's Income: ₹{today_income}", **stat_style).pack(pady=5)
    Label(frame, text=f"Most Popular Service: {most_popular}", **stat_style).pack(pady=5)

    Button(win, text="Close Dashboard", bg="#A4161A", fg="white", width=20, command=win.destroy).pack(pady=20)