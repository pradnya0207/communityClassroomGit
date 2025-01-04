import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from tkcalendar import DateEntry

class SupplierManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Supplier Management")
        self.root.configure(bg="#f0f0f0")  
        self.root.geometry("1400x700")  

        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="bag"
        )
        self.cursor = self.db.cursor()

        
        info_frame = tk.Frame(root, bg="#f0f0f0")  
        info_frame.pack(side=tk.TOP, pady=20)

        
        title_label = tk.Label(info_frame, text="SUPPLIER MANAGEMENT", font=("Arial", 16, "bold"), bg="#f0f0f0")
        title_label.grid(row=0, columnspan=2, pady=10)

        
        labels = ["Supplier Name", "Contact No.", "Product", "Quantity", "Price", "Date"]

        self.entry_vars = {}
        for i, label_text in enumerate(labels, start=1):
            label = tk.Label(info_frame, text=label_text, font=("Arial", 12), bg="#f0f0f0")
            label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.E)

            if label_text == "Date":
                cal = DateEntry(info_frame, width=12, background='darkblue', foreground='white', borderwidth=2, font=("Arial", 12))
                cal.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)
                self.entry_vars[label_text] = cal
            else:
                entry_var = tk.StringVar()
                entry = tk.Entry(info_frame, textvariable=entry_var, font=("Arial", 12))
                entry.grid(row=i, column=1, padx=10, pady=5, sticky=tk.W)
                self.entry_vars[label_text] = entry_var

        
        buttons_frame = tk.Frame(info_frame, bg="#f0f0f0")
        buttons_frame.grid(row=len(labels) + 1, columnspan=2, padx=10, pady=10, sticky=tk.EW)

        
        add_button = tk.Button(buttons_frame, text="Add", command=self.add_supplier, font=("Arial", 12), bg="#4169e1", fg="white", width=8)
        add_button.grid(row=0, column=0, padx=5, pady=5)

        
        update_button = tk.Button(buttons_frame, text="Update Quantity", command=self.update_supplier_quantity, font=("Arial", 12), bg="#FFA500", fg="white", width=12)
        update_button.grid(row=0, column=1, padx=5, pady=5)

        
        clear_button = tk.Button(buttons_frame, text="Clear", command=self.clear_fields, font=("Arial", 12), bg="#FF4500", fg="white", width=6)
        clear_button.grid(row=0, column=2, padx=5, pady=5)

       
        display_frame = tk.Frame(root, bg="#f0f0f0")  # Set frame color to light gray
        display_frame.pack(side=tk.TOP, padx=30, pady=20)

        # Create treeview to display supplier data
        self.tree = ttk.Treeview(display_frame, columns=("Invoice No.", "Supplier Name", "Contact No.", "Product", "Quantity", "Price", "Date"), show="headings")
        self.tree.heading("Invoice No.", text="No.")
        self.tree.heading("Supplier Name", text="Supplier Name")
        self.tree.heading("Contact No.", text="Contact No.")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Date", text="Date")

        
        style = ttk.Style()
        style.theme_use("clam")  # Use 'clam' theme for Treeview
        style.configure("mystyle.Treeview", background="#f0f0f0", foreground="black", fieldbackground="#f0f0f0")
        style.configure("mystyle.Treeview.Heading", font=("Arial", 12, "bold"), background="#f0f0f0", foreground="black")
        style.configure("mystyle.Treeview", rowheight=25)  # Set row height

        self.tree.grid(row=0, column=0, sticky="nsew")
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

       
       
        scrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        
        self.tree.bind("<Double-1>", self.delete_supplier)

        
        self.populate_treeview()

    def populate_treeview(self):
        
        records = self.tree.get_children()
        for record in records:
            self.tree.delete(record)

        
        self.cursor.execute("SELECT * FROM supplier")
        rows = self.cursor.fetchall()

        
        for row in rows:
            self.tree.insert("", "end", values=row)

    def add_supplier(self):
        
        supplier_name = self.entry_vars["Supplier Name"].get()
        contact_no = self.entry_vars["Contact No."].get()
        product_name = self.entry_vars["Product"].get()
        quantity = self.entry_vars["Quantity"].get()
        price = self.entry_vars["Price"].get()
        date = self.entry_vars["Date"].get()

        
        if not all([supplier_name, contact_no, product_name, quantity, price, date]):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not contact_no.isdigit() or len(contact_no) != 10:
            messagebox.showerror("Error", "Contact No. must be a 10-digit number!")
            return

        if not quantity.isdigit():
            messagebox.showerror("Error", "Quantity must be a number!")
            return

        if not price.replace('.', '', 1).isdigit():  
            messagebox.showerror("Error", "Price must be a valid number!")
            return

        
        supplier_query = "INSERT INTO supplier (supplier_name, contact_no, product_name, quantity, price, date) VALUES (%s, %s, %s, %s, %s, %s)"
        supplier_values = (supplier_name, contact_no, product_name, quantity, price, date)
        self.cursor.execute(supplier_query, supplier_values)
        self.db.commit()

       
        bag_query = "INSERT INTO bag_stock (product_name, price, quantity) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE price = %s, quantity = %s"
        bag_values = (product_name, price, quantity, price, quantity)
        self.cursor.execute(bag_query, (product_name, price, quantity, price, quantity))
        self.db.commit()

        
        self.populate_treeview()

       
        self.clear_fields()

        messagebox.showinfo("Success", "Supplier added successfully!")

    def update_supplier_quantity(self):
        
        supplier_name = self.entry_vars["Supplier Name"].get()
        product_name = self.entry_vars["Product"].get()
        quantity = self.entry_vars["Quantity"].get()

       
        if not all([supplier_name, product_name, quantity]):
            messagebox.showerror("Error", "Supplier Name, Product, and Quantity fields are required!")
            return

        if not quantity.isdigit():
            messagebox.showerror("Error", "Quantity must be a number!")
            return

        
        self.cursor.execute("SELECT * FROM supplier WHERE supplier_name = %s AND product_name = %s", (supplier_name, product_name))
        supplier = self.cursor.fetchone()
        if not supplier:
            messagebox.showerror("Error", f"No supplier found with name '{supplier_name}' for product '{product_name}'!")
            return

        
        update_query = "UPDATE supplier SET quantity = quantity + %s WHERE supplier_name = %s AND product_name = %s"
        self.cursor.execute(update_query, (quantity, supplier_name, product_name))
        self.db.commit()

       
        bag_query = "INSERT INTO bag_stock (product_name, price, quantity) VALUES (%s, (SELECT price FROM supplier WHERE supplier_name = %s AND product_name = %s), %s) ON DUPLICATE KEY UPDATE quantity = quantity + %s"
        self.cursor.execute(bag_query, (product_name, supplier_name, product_name, quantity, quantity))
        self.db.commit()

        messagebox.showinfo("Success", f"Quantity updated successfully for '{product_name}' for supplier '{supplier_name}'!")

        
        self.populate_treeview()

    def delete_supplier(self, event):
        
        selected_item = self.tree.selection()
        if not selected_item:
            return

        
        if not messagebox.askyesno("Confirmation", "Are you sure you want to delete this supplier?"):
            return

        
        item_data = self.tree.item(selected_item, 'values')
        if not item_data:
            return

        
        delete_query_supplier = "DELETE FROM supplier WHERE invoice_no = %s"
        self.cursor.execute(delete_query_supplier, (item_data[0],))
        self.db.commit()

        
        delete_query_bag = "DELETE FROM bag_stock WHERE product_name = %s"
        self.cursor.execute(delete_query_bag, (item_data[3],))  
        self.db.commit()

       
        self.populate_treeview()

        messagebox.showinfo("Success", "Supplier deleted successfully!")

    def clear_fields(self):
        
        for entry_var in self.entry_vars.values():
            if isinstance(entry_var, tk.StringVar):
                entry_var.set("")
            elif isinstance(entry_var, DateEntry):
                entry_var.delete(0, tk.END)

def run_supplier_management_page():
    root = tk.Tk()
    app = SupplierManagement(root)
    root.mainloop()

if __name__ == "__main__":
    run_supplier_management_page()
