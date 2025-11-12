from tkinter import *
from tkinter import messagebox
from db_connect import connect_db

def add_customer_window():
    win = Toplevel()
    win.title("Add New Customer")
    win.geometry("400x400")
    win.config(bg="#F8FAFC")

    Label(win, text="Add Customer Details", font=("Arial", 16, "bold"), bg="#F8FAFC", fg="#0A4D68").pack(pady=10)

    # Entry form
    Label(win, text="Customer Name:", bg="#F8FAFC").pack(pady=5)
    entry_name = Entry(win, width=30)
    entry_name.pack(pady=5)

    Label(win, text="Phone Number:", bg="#F8FAFC").pack(pady=5)
    entry_phone = Entry(win, width=30)
    entry_phone.pack(pady=5)

    Label(win, text="Vehicle Model:", bg="#F8FAFC").pack(pady=5)
    entry_model = Entry(win, width=30)
    entry_model.pack(pady=5)

    Label(win, text="Vehicle Number:", bg="#F8FAFC").pack(pady=5)
    entry_number = Entry(win, width=30)
    entry_number.pack(pady=5)

    def save_customer():
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        model = entry_model.get().strip()
        number = entry_number.get().strip()

        if not (name and phone and model and number):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        cn = connect_db()
        if cn is None:
            messagebox.showerror("Database Error", "Cannot connect to database.")
            return
        
        cur = cn.cursor()
        try:
            cur.execute("""
                INSERT INTO customers (name, phone, v_model, v_number)
                VALUES (%s, %s, %s, %s)
            """, (name, phone, model, number))
            cn.commit()
            messagebox.showinfo("Success", "Customer added successfully!")
            entry_name.delete(0, END)
            entry_phone.delete(0, END)
            entry_model.delete(0, END)
            entry_number.delete(0, END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {e}")
        finally:
            cur.close()
            cn.close()

    Button(win, text="Save Customer", bg="#0A4D68", fg="white", width=15, command=save_customer).pack(pady=20)
    Button(win, text="Close", bg="#A4161A", fg="white", width=15, command=win.destroy).pack()
    win.mainloop()