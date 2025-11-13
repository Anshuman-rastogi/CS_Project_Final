from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from connect_db import connect_db
import datetime
import os

def generate_bill_window():
    # Create a new window for generating bills
    win = Toplevel()
    win.title("Generate Bill")
    win.geometry("600x700")
    win.config(bg="#F8FAFC")

    Label(win, text="Generate Bill", font=("Arial", 18, "bold"), bg="#F8FAFC", fg="#0A4D68").pack(pady=10)

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

    # Create checkboxes for each service
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
            bill_id = cur.lastrowid
            service_str = ", ".join(selected_services)
            show_receipt(cust_id, bill_id, service_str, total, bill_date)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate bill: {e}")
        finally:
            cur.close()
            cn.close()

    Button(win, text="Calculate Total", bg="#0A4D68", fg="white", width=15, command=calculate_total).pack(pady=10)
    Button(win, text="Generate Bill", bg="#0A4D68", fg="white", width=15, command=generate_bill).pack(pady=5)
    Button(win, text="Close", bg="#A4161A", fg="white", width=15, command=win.destroy).pack(pady=15)
    win.mainloop()
    
# ------------------ BILL RECEIPT POP-UP ------------------ #
def show_receipt(cust_id, bill_id, services, total, date):
    receipt = Toplevel()
    receipt.title("Customer Receipt")
    receipt.geometry("400x550")
    receipt.config(bg="#FFFFFF")

    Label(receipt, text="AutoCare Invoice", font=("Arial", 18, "bold"), bg="white", fg="#0A4D68").pack(pady=10)
    Label(receipt, text=f"Bill ID: {bill_id}", bg="white").pack()
    Label(receipt, text=f"Customer ID: {cust_id}", bg="white").pack()
    Label(receipt, text=f"Date: {date}", bg="white").pack()
    Label(receipt, text="----------------------------", bg="white").pack(pady=5)

    cn = connect_db()
    cur = cn.cursor()
    cur.execute("SELECT name, v_model, v_number FROM customers WHERE cust_id=%s", (cust_id,))
    cust = cur.fetchone()
    cn.close()

    cust_name, model, number = cust if cust else ("Unknown", "-", "-")

    Label(receipt, text="Services Availed:", font=("Arial", 12, "bold"), bg="white").pack()
    text_box = Text(receipt, width=40, height=10, bg="#F8F8F8")
    text_box.pack(pady=5)
    text_box.insert(END, services.replace(", ", "\n"))
    text_box.config(state=DISABLED)

    Label(receipt, text=f"Total: ₹{total}", font=("Arial", 14, "bold"), bg="white", fg="#0A4D68").pack(pady=10)
    Label(receipt, text="Thank you for choosing AutoCare!", bg="white", fg="gray").pack(pady=5)

    def save_receipt():
        folder = "bills"
        os.makedirs(folder, exist_ok=True)

        filename = os.path.join(folder, f"Bill_{bill_id}.txt")

        # Fetch customer info for better receipt details
        cn = connect_db()
        cur = cn.cursor()
        cur.execute("SELECT name, v_model, v_number FROM customers WHERE cust_id=%s", (cust_id,))
        cust = cur.fetchone()
        cn.close()

        cust_name, model, number = cust if cust else ("Unknown", "-", "-")

        with open(filename, "w", encoding="utf-8") as f:
            f.write("==============================================\n")
            f.write("            AutoCare Detailing Centre         \n")
            f.write("==============================================\n")
            f.write(f"Bill ID      : {bill_id}\n")
            f.write(f"Date & Time  : {date}\n\n")
            f.write(f"Customer ID  : {cust_id}\n")
            f.write(f"Customer Name: {cust_name}\n")
            f.write(f"Vehicle Model: {model}\n")
            f.write(f"Vehicle No.  : {number}\n")
            f.write("----------------------------------------------\n")
            f.write("Services Availed:\n")
            for s in services.split(", "):
                f.write(f"  • {s}\n")
            f.write("----------------------------------------------\n")
            f.write(f"Total Amount : ₹{total}\n")
            f.write("----------------------------------------------\n\n")
            f.write("Thank you for choosing AutoCare!\n")
            f.write("We appreciate your trust in our services.\n\n")
            f.write("==============================================\n")

    Button(receipt, text="Save as Text", bg="#0A4D68", fg="white", width=20, command=save_receipt).pack(pady=10)
    Button(receipt, text="Close", bg="#A4161A", fg="white", width=20, command=receipt.destroy).pack(pady=5)