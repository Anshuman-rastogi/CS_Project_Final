from tkinter import *
from tkinter import messagebox, ttk
from db_connect import connect_db

def search_customer_window():
    win = Toplevel()
    win.title("Search Customer")
    win.geometry("700x500")
    win.config(bg="#F8FAFC")

    Label(win, text="Search Customer", font=("Arial", 18, "bold"), bg="#F8FAFC", fg="#0A4D68").pack(pady=10)

    # Search bar
    Label(win, text="Search by (Name / Vehicle Number / ID):", bg="#F8FAFC").pack(pady=5)
    search_entry = Entry(win, width=40)
    search_entry.pack(pady=5)

    # Table (Treeview)
    columns = ("ID", "Name", "Phone", "Model", "Number")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(pady=20)

    def search_customer():
        query = search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter something to search.")
            return

        cn = connect_db()
        if cn is None:
            messagebox.showerror("Database Error", "Cannot connect to database.")
            return
        cur = cn.cursor()
        try:
            sql = """SELECT cust_id, name, phone, v_model, v_number 
                     FROM customers 
                     WHERE name LIKE %s OR v_number LIKE %s OR cust_id LIKE %s"""
            cur.execute(sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
            results = cur.fetchall()
            
            # Clear old results
            for row in tree.get_children():
                tree.delete(row)

            if results:
                for row in results:
                    tree.insert("", "end", values=row)
            else:
                messagebox.showinfo("No Results", "No matching records found.")

        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")
        finally:
            cur.close()
            cn.close()

    Button(win, text="Search", bg="#0A4D68", fg="white", width=15, command=search_customer).pack(pady=10)
    Button(win, text="Close", bg="#A4161A", fg="white", width=15, command=win.destroy).pack(pady=5)

    win.mainloop()