from tkinter import *
from tkinter import messagebox
from connect_db import connect_db
from main import open_main_window
from dashboard import dashboard_window

def login_window():
    root = Tk()
    root.title("AutoCare Admin Login")
    root.geometry("400x300")
    root.config(bg="#F4F7F8")

    Label(root, text="Admin Login", font=("Arial", 18, "bold"), bg="#F4F7F8", fg="#0A4D68").pack(pady=15)

    Label(root, text="Username:", bg="#F4F7F8").pack()
    entry_user = Entry(root, width=30)
    entry_user.pack(pady=5)

    Label(root, text="Password:", bg="#F4F7F8").pack()
    entry_pass = Entry(root, width=30, show="*")
    entry_pass.pack(pady=5)

    def attempt_login():
        username = entry_user.get().strip()
        password = entry_pass.get().strip()

        if not (username and password):
            messagebox.showwarning("Missing Info", "Enter both username and password.")
            return

        cn = connect_db()
        cur = cn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        result = cur.fetchone()
        cn.close()

        if result:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            root.withdraw()  # ✅ hides the login window instead of destroying it
            open_main_window(root)  # pass the same root to the main window
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    Button(root, text="Login", bg="#0A4D68", fg="white", width=15, command=attempt_login).pack(pady=20)
    entry_pass.bind("<Return>", lambda event: attempt_login())
    Button(root, text="Exit", bg="#A4161A", fg="white", width=15, command=root.destroy).pack()

    root.mainloop()