from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_connect import connect_db
import datetime

def generate_bill_window():
    win = Toplevel()
    win.title("Generate Bill")
    win.geometry("600x600")
    win.config(bg="#F8FAFC")

    Label(win, text="Generate Bill", font=("Arial", 18, "bold"), bg="#F8FAFC", fg="#0A4D68").pack(pady=10)
    
    '''# Customer ID input section
    Label(win, text="Enter Customer ID:", bg="#F8FAFC").pack(pady=5)
    entry_cust_id = Entry(win, width=20)
    entry_cust_id.pack(pady=5)'''

    # Customer selection dropdown
    Label(win, text="Select Customer:", bg="#F8FAFC").pack(pady=5)
    
    cn = connect_db()
    if cn is None:
        messagebox.showerror("Database Error", "Cannot connect to database.")
        return
    cur = cn.cursor()
    cur.execute("SELECT cust_id, name, v_model FROM customers")
    customers = cur.fetchall()
    cn.close()

    customer_dict = {}
    customer_display = []

    for cid, cname, cmodel in customers:
        display_text = f"{cname} - {cmodel}"
        customer_dict[display_text] = cid
        customer_display.append(display_text)

    selected_customer = StringVar()
    customer_dropdown = ttk.Combobox(win, textvariable=selected_customer, values=customer_display, width=40)
    customer_dropdown.pack(pady=5)

    # Display available services
    Label(win, text="Select Services:", bg="#F8FAFC").pack(pady=5)
    service_vars = []
    service_list = []

    cn = connect_db()
    if cn is None:
        messagebox.showerror("Database Error", "Cannot connect to database.")
        return
    cur = cn.cursor()
    cur.execute("SELECT serv_id, serv_name, cost FROM services")
    service_list = cur.fetchall()
    cn.close()

    frame_services = Frame(win, bg="#F8FAFC")
    frame_services.pack()

    for s_id, s_name, s_cost in service_list:
        var = IntVar()
        Checkbutton(frame_services, text=f"{s_name} - ₹{s_cost}", variable=var, bg="#F8FAFC").pack(anchor="w", padx=20)
        service_vars.append((var, s_id, s_name, s_cost))

    total_label = Label(win, text="Total: ₹0", font=("Arial", 14, "bold"), bg="#F8FAFC")
    total_label.pack(pady=10)

    def calculate_total():
        total = 0
        for var, s_id, s_name, s_cost in service_vars:
            if var.get() == 1:
                total += s_cost
        total_label.config(text=f"Total: ₹{total}")

    def generate_bill():
        '''cust_id = entry_cust_id.get().strip()
        if not cust_id:
            messagebox.showwarning("Input Error", "Enter a valid customer ID.")
            return'''
        
        selected_name = selected_customer.get()
        if not selected_name:
            messagebox.showwarning("Input Error", "Please select a customer.")
            return

        cust_id = customer_dict.get(selected_name)
        
        selected_services = []
        total = 0
        for var, s_id, s_name, s_cost in service_vars:
            if var.get() == 1:
                selected_services.append(s_name)
                total += s_cost

        if not selected_services:
            messagebox.showwarning("No Service Selected", "Please select at least one service.")
            return
        
        cn = connect_db()
        if cn is None:
            messagebox.showerror("Database Error", "Cannot connect to database.")
            return
        cur = cn.cursor()
        try:
            service_str = ", ".join(selected_services)
            bill_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cur.execute("""
                INSERT INTO billing (cust_id, services, total_amt, bill_date)
                VALUES (%s, %s, %s, %s)
            """, (cust_id, service_str, total, bill_date))
            cn.commit()
            messagebox.showinfo("Success", f"Bill generated successfully!\nTotal: ₹{total}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill: {e}")
        finally:
            cur.close()
            cn.close()

    Button(win, text="Calculate Total", bg="#0A4D68", fg="white", width=15, command=calculate_total).pack(pady=10)
    Button(win, text="Generate Bill", bg="#0A4D68", fg="white", width=15, command=generate_bill).pack(pady=5)
    Button(win, text="Close", bg="#A4161A", fg="white", width=15, command=win.destroy).pack(pady=15)
    win.mainloop()