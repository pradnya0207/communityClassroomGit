import tkinter as tk
from tkinter import ttk, Button, Label
import mysql.connector

class DatabaseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Database Viewer")
        self.root.configure(bg="#ECEFF1")  

        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")  

        
        sidebar_frame = tk.Frame(root, bg="#546E7A", width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        
        customer_btn = Button(sidebar_frame, text="Customers", command=self.show_customer_records, bg="#2196F3", fg="white", font=("Helvetica", 12), width=25)
        customer_btn.pack(pady=10)

        bill_btn = Button(sidebar_frame, text="Check Bill Records", command=self.show_bill_records, bg="#4CAF50", fg="white", font=("Helvetica", 12), width=25)
        bill_btn.pack(pady=10)

        
        self.customer_tree = None

        
        self.bill_tree = None

    def show_customer_records(self):
        
        self.clear_content()

        
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="bag"
        )
        cursor = db.cursor()

        
        cursor.execute("SELECT * FROM customer")
        records = cursor.fetchall()

        
        customer_title_label = Label(self.root, text="Customers", font=("Helvetica", 16, "bold"), bg="#ECEFF1")
        customer_title_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        # Create a treeview to display the customer records
        self.customer_tree = ttk.Treeview(self.root, style="Custom.Treeview")
        self.customer_tree["columns"] = ("Mobile","Name", "Address")

        # Define columns
        self.customer_tree.column("#0", width=0, stretch=tk.NO)
        self.customer_tree.column("Mobile", anchor=tk.W, width=100)
        self.customer_tree.column("Name", anchor=tk.W, width=150)
        self.customer_tree.column("Address", anchor=tk.W, width=200)
       

        # Create headings
        self.customer_tree.heading("#0", text="", anchor=tk.W)
        self.customer_tree.heading("Mobile", text="Mobile", anchor=tk.W)
        self.customer_tree.heading("Name", text="Name", anchor=tk.W)
        self.customer_tree.heading("Address", text="Address", anchor=tk.W)
       

        
        self.customer_tree.heading("#0", image="")
        self.customer_tree.tag_configure("heading", font=("Helvetica", 12, "bold"), background="#2196F3", foreground="white")

        
        for record in records:
            self.customer_tree.insert("", tk.END, text="", values=record)

       
        self.customer_tree.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def show_bill_records(self):
        
        self.clear_content()

       
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Enter your MySQL password
            database="bag"
        )
        cursor = db.cursor()

        
        cursor.execute("SELECT * FROM custbill")
        records = cursor.fetchall()

        
        bill_title_label = Label(self.root, text="Bills", font=("Helvetica", 16, "bold"), bg="#ECEFF1")
        bill_title_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        
        self.bill_tree = ttk.Treeview(self.root, style="Custom.Treeview")
        self.bill_tree["columns"] = ("Bill ID", "Mobile", "Product Name", "Quantity", "Price", "Date")

        
        self.bill_tree.column("#0", width=0, stretch=tk.NO)
        self.bill_tree.column("Bill ID", anchor=tk.W, width=100)
        self.bill_tree.column("Mobile", anchor=tk.W, width=100)
        self.bill_tree.column("Product Name", anchor=tk.W, width=150)
        self.bill_tree.column("Quantity", anchor=tk.W, width=100)
        self.bill_tree.column("Price", anchor=tk.W, width=100)
        self.bill_tree.column("Date", anchor=tk.W, width=150)

        
        self.bill_tree.heading("#0", text="", anchor=tk.W)
        self.bill_tree.heading("Bill ID", text="Bill ID", anchor=tk.W)
        self.bill_tree.heading("Mobile", text="Mobile", anchor=tk.W)
        self.bill_tree.heading("Product Name", text="Product Name", anchor=tk.W)
        self.bill_tree.heading("Quantity", text="Quantity", anchor=tk.W)
        self.bill_tree.heading("Price", text="Price", anchor=tk.W)
        self.bill_tree.heading("Date", text="Date", anchor=tk.W)

        
        self.bill_tree.heading("#0", image="")
        self.bill_tree.tag_configure("heading", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="white")

        
        for record in records:
            self.bill_tree.insert("", tk.END, text="", values=record)

        
        self.bill_tree.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def clear_content(self):
        
        if self.customer_tree:
            self.customer_tree.destroy()
        if self.bill_tree:
            self.bill_tree.destroy()

def run_database_viewer():
    root = tk.Tk()
    style = ttk.Style(root)
    style.configure("Custom.Treeview", background="#ECEFF1", fieldbackground="#ECEFF1", font=("Helvetica", 12))
    app = DatabaseViewer(root)
    root.mainloop()

if __name__ == "__main__":
    run_database_viewer()
