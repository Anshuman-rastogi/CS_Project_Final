from tkinter import *
from tkinter import messagebox, ttk
from connect_db import connect_db

def search_customer_window():
    win = Toplevel()
    win.title("Search Customer")
    win.geometry("750x550")
    win.config(bg="#F8FAFC")

    Label(win, text="Search Customer", font=("Arial", 18, "bold"), bg="#F8FAFC", fg="#0A4D68").pack(pady=10)

    # Filter selection + entry
    filter_type = StringVar(value="Name")
    frame_filter = Frame(win, bg="#F8FAFC")
    frame_filter.pack(pady=5)

    Label(frame_filter, text="Search By:", bg="#F8FAFC").grid(row=0, column=0, padx=5)
    OptionMenu(frame_filter, filter_type, "Name", "Vehicle Number", "Customer ID").grid(row=0, column=1, padx=5)
    search_entry = Entry(frame_filter, width=30)
    search_entry.grid(row=0, column=2, padx=5)

    columns = ("ID", "Name", "Phone", "Model", "Number")
    tree = ttk.Treeview(win, columns=columns, show="headings", height=8)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130)
    tree.pack(pady=10)

    def search_customer():
        query = search_entry.get().strip()
        filter_choice = filter_type.get()
        if not query:
            messagebox.showwarning("Input Error", "Enter something to search.")
            return

        cn = connect_db()
        cur = cn.cursor()

        if filter_choice == "Name":
            sql = "SELECT cust_id, name, phone, v_model, v_number FROM customers WHERE name LIKE %s"
        elif filter_choice == "Vehicle Number":
            sql = "SELECT cust_id, name, phone, v_model, v_number FROM customers WHERE v_number LIKE %s"
        else:
            sql = "SELECT cust_id, name, phone, v_model, v_number FROM customers WHERE cust_id LIKE %s"

        cur.execute(sql, (f"%{query}%",))
        rows = cur.fetchall()

        for item in tree.get_children():
            tree.delete(item)

        if rows:
            for r in rows:
                tree.insert("", "end", values=r)
        else:
            messagebox.showinfo("No Results", "No matching records found.")

        cn.close()

    def view_bills():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a customer first.")
            return

        cust_id = tree.item(selected)['values'][0]
        bill_win = Toplevel(win)
        bill_win.title("View Customer Bills")
        bill_win.geometry("600x400")
        bill_win.config(bg="#F8FAFC")

        Label(bill_win, text=f"Billing History (Customer ID: {cust_id})", 
              font=("Arial", 14, "bold"), bg="#F8FAFC", fg="#0A4D68").pack(pady=10)

        cols = ("Bill ID", "Services", "Total", "Date")
        bill_tree = ttk.Treeview(bill_win, columns=cols, show="headings", height=10)
        for col in cols:
            bill_tree.heading(col, text=col)
            bill_tree.column(col, width=130)
        bill_tree.pack(pady=10)

        cn = connect_db()
        cur = cn.cursor()
        cur.execute("""SELECT bill_id, services, total_amt, bill_date 
                       FROM billing WHERE cust_id = %s ORDER BY bill_date DESC""", (cust_id,))
        bills = cur.fetchall()
        for b in bills:
            bill_tree.insert("", "end", values=b)
        cn.close()

    Button(win, text="Search", bg="#0A4D68", fg="white", width=15, command=search_customer).pack(pady=5)
    search_entry.bind("<Return>", lambda event: search_customer())
    Button(win, text="View Bills", bg="#0A4D68", fg="white", width=15, command=view_bills).pack(pady=5)
    Button(win, text="Close", bg="#A4161A", fg="white", width=15, command=win.destroy).pack(pady=10)

    win.mainloop()