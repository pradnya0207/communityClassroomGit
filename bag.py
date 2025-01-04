import tkinter as tk
from tkinter import Label, Checkbutton, Button, IntVar, messagebox, Scrollbar, Toplevel, Entry
from datetime import datetime
import mysql.connector

class BagSelection:
    def __init__(self, root):
        self.root = root
        self.root.title("Bag Selection")
        self.root.configure(bg="#ECEFF1")  #  background color

        
        window_width = 1400
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

       
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="bag"
        )
        self.cursor = self.db.cursor()

        
        self.customer_name = tk.StringVar()
        self.customer_address = tk.StringVar()
        self.customer_mobile = tk.StringVar()
        self.customer_bill_id = tk.StringVar()

        
        self.fetch_bag_data()

        
        customer_frame = tk.Frame(root, bg="#ECEFF1", padx=20, pady=20)
        customer_frame.pack()

        
        Label(customer_frame, text="Customer Name:", font=("Helvetica", 12), fg="#455A64", bg="#ECEFF1").grid(row=0, column=0, padx=5, pady=5)
        Entry(customer_frame, textvariable=self.customer_name, font=("Helvetica", 12)).grid(row=0, column=1, padx=5, pady=5)

        Label(customer_frame, text="Address:", font=("Helvetica", 12), fg="#455A64", bg="#ECEFF1").grid(row=1, column=0, padx=5, pady=5)
        Entry(customer_frame, textvariable=self.customer_address, font=("Helvetica", 12)).grid(row=1, column=1, padx=5, pady=5)

        Label(customer_frame, text="Mobile Number:", font=("Helvetica", 12), fg="#455A64", bg="#ECEFF1").grid(row=2, column=0, padx=5, pady=5)
        Entry(customer_frame, textvariable=self.customer_mobile, font=("Helvetica", 12)).grid(row=2, column=1, padx=5, pady=5)

        # Create a frame for bag selection
        bag_frame = tk.Frame(root, bg="#ECEFF1", padx=20, pady=20)
        bag_frame.pack()

        # Heading for bag selection
        Label(bag_frame, text="Select Bags", font=("Helvetica", 24, "bold"), fg="#455A64", bg="#ECEFF1").grid(row=0, column=0, columnspan=4, pady=15)

        # Create a canvas for bag selection with a scrollbar
        canvas = tk.Canvas(bag_frame, bg="#ECEFF1", height=500)
        canvas.grid(row=1, column=0, columnspan=4, sticky="nsew")

        scrollbar = Scrollbar(bag_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=1, column=4, sticky='ns')
        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas
        inner_frame = tk.Frame(canvas, bg="#ECEFF1")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        start_row = 1
        self.checkbox_vars = []
        self.quantity_entries = []
        for i, bag in enumerate(self.bags, start=1):
            checkbox_var = IntVar()
            self.checkbox_vars.append(checkbox_var)
            Checkbutton(inner_frame, text=f"{bag['name']} - {bag['price']:.2f} - Quantity:", variable=checkbox_var, onvalue=i, offvalue=0, bg="#ECEFF1", font=("Helvetica", 12)).grid(row=i + start_row, column=0, columnspan=2, pady=5, sticky="w")
            
            
            quantity_entry = tk.Spinbox(inner_frame, from_=0, to=10, width=3, font=("Helvetica", 12))
            quantity_entry.grid(row=i + start_row, column=2, pady=5, padx=5, sticky="w")
            self.quantity_entries.append(quantity_entry)

        
        calculate_bill_btn = Button(inner_frame, text="Generate Bill", command=self.generate_bill, bg="#2196F3", fg="white", font=("Helvetica", 16))
        calculate_bill_btn.grid(row=start_row + len(self.bags) + 1, column=0, columnspan=4, pady=20)

    def fetch_bag_data(self):
       
        self.bags = []
        self.cursor.execute("SELECT bid, product_name, price, quantity FROM bag_stock")
        for row in self.cursor.fetchall():
            bag_id, product_name, price, quantity = row
            self.bags.append({"bid": bag_id, "name": product_name, "price": price, "quantity": quantity})

    def generate_bill(self):
        # Validate mobile number
        contact_no = self.customer_mobile.get()
        if not contact_no.isdigit() or len(contact_no) != 10:
            messagebox.showerror("Error", "Contact No. must be a 10-digit number!")
            return

        
        self.cursor.execute("SELECT * FROM customer WHERE mobile = %s", (contact_no,))
        existing_customer = self.cursor.fetchone()

        
        if not existing_customer:
            self.cursor.execute("INSERT INTO customer (mobile, name, address) VALUES (%s, %s, %s)", (contact_no, self.customer_name.get(), self.customer_address.get()))
            self.db.commit()

        
        self.store_bill_details()

        # Create a new window for displaying the bill
        bill_window = Toplevel(self.root)
        bill_window.title("Bag House")
        bill_window.configure(bg="#ECEFF1")

        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        bill_window.geometry(f"{screen_width}x{screen_height}+0+0")

        
        Label(bill_window, text="Bag House", font=("Helvetica", 24, "bold"), fg="#455A64", bg="#ECEFF1").pack()

        
        Label(bill_window, text=f"Customer Name: {self.customer_name.get()}", font=("Helvetica", 12), fg="#455A64", bg="#ECEFF1").pack()

        
        bill_content = self.generate_bill_content()
        Label(bill_window, text=bill_content, font=("Helvetica", 12), bg="#ECEFF1").pack()

        # Button to print bill
        print_btn = Button(bill_window, text="Print", command=lambda: self.print_bill(bill_window), bg="#2196F3", fg="white", font=("Helvetica", 16))
        print_btn.pack(pady=20)

    def generate_bill_content(self):
        
        bill_id = self.get_next_bill_id()

        
        total_price = 0
        bill_content = f"{'Bill':^50}\n\n"
        bill_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        bill_content += f"Bill ID: {bill_id}\n\n"
        bill_content += f"{'Product Name': <30}{'Quantity': <10}\n"
        bill_content += "-" * 40 + "\n"

        
        for i, checkbox_var in enumerate(self.checkbox_vars):
            if checkbox_var.get():
                bag = self.bags[i]
                quantity = int(self.quantity_entries[i].get())
                
                if bag["quantity"] < 1:
                    messagebox.showwarning("Warning", f"Quantity for {bag['name']} is not sufficient.")
                elif bag["quantity"] < 10:
                    messagebox.showwarning("Warning", f"Quantity for {bag['name']} is less. Give order to the supplier.")
                
                # Only calculate total price if quantity is greater than 0
                if quantity > 0:
                    total_price += bag["price"] * quantity
                    bill_content += f"{bag['name']: <30}{quantity: <10}\n"

                    # Update stock quantity in the bag_stock table
                    updated_quantity = bag["quantity"] - quantity
                    self.cursor.execute("UPDATE bag_stock SET quantity = %s WHERE bid = %s", (updated_quantity, bag["bid"]))
                    self.db.commit()

        # Display total price only if the total quantity is greater than 0
        if total_price > 0:
            bill_content += "-" * 40 + "\n"
            bill_content += f"{'Total Price:': <30}rs.{total_price:.2f}"
        
        return bill_content

    def get_next_bill_id(self):
        # Fetch the last bill ID from the database and increment by 1
        self.cursor.execute("SELECT MAX(bill_id) FROM bill")
        last_bill_id = self.cursor.fetchone()[0]
        return last_bill_id + 1 if last_bill_id is not None else 1

    def store_bill_details(self):
        
        mobile = self.customer_mobile.get()

        
        for i, checkbox_var in enumerate(self.checkbox_vars):
            if checkbox_var.get():
                bag = self.bags[i]
                quantity = int(self.quantity_entries[i].get())

                
                self.cursor.execute("INSERT INTO custbill (mobile, product_name, quantity, price) VALUES (%s, %s, %s, %s)", (mobile, bag["name"], quantity, bag["price"]))
                self.db.commit()

    def print_bill(self, window):
        # Print the bill content
        print("Printing bill...")
        window.destroy()

def run_bag_selection_page():
    root = tk.Tk()
    app = BagSelection(root)
    root.mainloop()

if __name__ == "__main__":
    run_bag_selection_page()
