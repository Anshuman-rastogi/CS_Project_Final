from setup_db import setup_db
setup_db()
from dashboard import dashboard_window
from tkinter import *
from tkinter import messagebox
import sys
from add_customer import add_customer_window
from generate_bill import generate_bill_window
from search_customer import search_customer_window

def open_main_window(root):
    win = Toplevel(root)
    win.title("AutoCare Management System")
    win.geometry("700x500")
    win.config(bg="#E8F0F2")

    Label(win, text="AutoCare Management System", font=("Arial", 22, "bold"), 
       bg="#E8F0F2", fg="#0A4D68").pack(pady=30)

    Button(win, text="Add Customer", width=25, font=("Arial", 12), 
       bg="#0A4D68", fg="white", command=add_customer_window).pack(pady=10)

    Button(win, text="Billing", width=25, font=("Arial", 12),
       bg="#0A4D68", fg="white", command=generate_bill_window).pack(pady=10)

    Button(win, text="Search Customer", width=25, font=("Arial", 12),
       bg="#0A4D68", fg="white", command=search_customer_window).pack(pady=10)
    
    Button(win, text="View Dashboard", width=25, font=("Arial", 12),
       bg="#0A4D68", fg="white", command=dashboard_window).pack(pady=10)

    Button(win, text="Exit Program", width=25, font=("Arial", 12),
       bg="#A4161A", fg="white", command=lambda: exit_program(root)).pack(pady=10)
    
    def exit_program(root):
      confirm = messagebox.askyesno("Exit", "Are you sure you want to exit AutoCare?")
      if confirm:
        # ✅ Close all windows and end the app completely
         root.destroy()
         sys.exit()  # optional safety to ensure total shutdown

    
    win.mainloop()