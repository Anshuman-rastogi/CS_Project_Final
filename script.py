from setup_db import setup_db
setup_db()
from tkinter import *
from tkinter import messagebox
from customers import add_customer_window
from billing import generate_bill_window
from search import search_customer_window

root = Tk()
root.iconbitmap("autocare.ico")
root.title("AutoCare Management System")
root.geometry("700x500")
root.config(bg="#E8F0F2")

Label(root, text="AutoCare Management System", font=("Arial", 22, "bold"),
      bg="#E8F0F2", fg="#0A4D68").pack(pady=30)
Button(root, text="Add Customer", width=25, font=("Arial", 12),
       bg="#0A4D68", fg="white", command=add_customer_window).pack(pady=10)
Button(root, text="Generate Bill", width=25, font=("Arial", 12),
       bg="#0A4D68", fg="white", command=generate_bill_window).pack(pady=10)
Button(root, text="Search Customer", width=25, font=("Arial", 12),
       bg="#0A4D68", fg="white", command=search_customer_window).pack(pady=10)
Button(root, text="Exit", width=25, font=("Arial", 12),
       bg="#A4161A", fg="white", command=root.destroy).pack(pady=10)
root.mainloop()