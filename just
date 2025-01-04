import tkinter as tk
from tkinter import messagebox
from customer import Customer  # Import the Customer class

# Simple user database (for demonstration purposes)
user_database = {
    "a": "a",
    "user1": "12345",
    # Add more users if needed
}

def authenticate(username, password):
    if username in user_database and user_database[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_home_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_home_page():
    # Create the home page window
    home_page = tk.Toplevel()
    home_page.title("Home Page")

    # Set window size and position
    window_width = 600
    window_height = 400
    screen_width = home_page.winfo_screenwidth()
    screen_height = home_page.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    home_page.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Add widgets and content for the home page
    welcome_label = tk.Label(home_page, text="Welcome to the Bag Shop Management System!", font=("Helvetica", 20, "bold"), fg="#3498db")
    welcome_label.pack(pady=20)

    # Buttons for different functionalities with styled appearance
    stock_button = tk.Button(home_page, text="Check Stock", command=check_stock, font=("Helvetica", 14), bg="#27ae60", fg="white", padx=20, pady=10)
    customer_button = tk.Button(home_page, text="Customer Registration", command=customer_registration, font=("Helvetica", 14), bg="#e74c3c", fg="white", padx=20, pady=10)
    supplier_button = tk.Button(home_page, text="Supplier Management", command=supplier_management, font=("Helvetica", 14), bg="#f39c12", fg="white", padx=20, pady=10)

    # Place buttons on the home page
    stock_button.pack(pady=10)
    customer_button.pack(pady=10)
    supplier_button.pack(pady=10)

    # Start the main loop for the home page window
    home_page.mainloop()

# Example functions for the buttons (replace with your own functionality)
def check_stock():
    messagebox.showinfo("Check Stock", "Stock information goes here.")

def customer_registration():
    root = tk.Tk()
    app = Customer(root)
    root.mainloop()

def supplier_management():
    messagebox.showinfo("Supplier Management", "Supplier management page goes here.")

def show_login_page():
    root = tk.Tk()
    root.title("Login Page")

    # Set window size and position
    window_width = 500
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Set background color
    root.configure(bg="pink")

    # Create a frame to contain login elements
    login_frame = tk.Frame(root, bg="#2c3e50", bd=10)
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Create a heading label inside the frame
    heading_label = tk.Label(login_frame, text="Login Panel", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="#ecf0f1")
    heading_label.pack(pady=10)

    # Create and place widgets with enhanced styling inside the frame
    label_username = tk.Label(login_frame, text="Username:", font=("Helvetica", 12), bg="#2c3e50", fg="white")
    entry_username = tk.Entry(login_frame, font=("Helvetica", 12))
    label_password = tk.Label(login_frame, text="Password:", font=("Helvetica", 12), bg="#2c3e50", fg="white")
    entry_password = tk.Entry(login_frame, show="*", font=("Helvetica", 12))

    login_button = tk.Button(login_frame, text="Login", command=lambda: authenticate(entry_username.get(), entry_password.get()), bg="#27ae60", fg="white", font=("Helvetica", 12))

    # Place widgets with pack and anchor to center inside the frame
    label_username.pack(pady=5)
    entry_username.pack(pady=5)
    label_password.pack(pady=5)
    entry_password.pack(pady=5)
    login_button.pack(pady=20)

    # Make the window maximizable
    root.state('zoomed')

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    show_login_page()
import tkinter as tk
from tkinter import StringVar, Label, Entry, Button, messagebox
import mysql.connector
import bag  # Assuming bag.py contains the code for the project selection page

class Customer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x300")
        self.root.title("Customer Registration Form")
        self.root.configure(bg="pink")

        # Create a connection to the MySQL database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bag"
        )
        self.cursor = self.db.cursor()

        # Create a frame to center content
        frame = tk.Frame(self.root, bg="#ffffff", padx=20, pady=20)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Heading
        Label(frame, text="Customer Registration Form", font=("Helvetica", 18, "bold"), fg="#3498db", bg="#ffffff").grid(row=0, column=0, columnspan=2, pady=10)

        # Labels and Entries
        labels = ["Name", "Phone no", "Address"]
        for i, label_text in enumerate(labels, start=1):
            Label(frame, text=label_text, font=("Helvetica", 14), bg="#ffffff").grid(row=i, column=0, pady=10, padx=5, sticky=tk.W)

        self.namevalue = StringVar()
        self.phone_novalue = StringVar()
        self.addressvalue = StringVar()

        entries = [Entry(frame, textvariable=self.namevalue, font=("Helvetica", 12)),
                   Entry(frame, textvariable=self.phone_novalue, font=("Helvetica", 12)),
                   Entry(frame, textvariable=self.addressvalue, font=("Helvetica", 12))]

        for i, entry in enumerate(entries, start=1):
            entry.grid(row=i, column=1, pady=10, padx=5)

        # Submit Button
        Button(frame, text="Submit", command=self.open_project_selection, bg="#27ae60", fg="white", font=("Helvetica", 14)).grid(row=4, column=0, columnspan=2, pady=20)

    def open_project_selection(self):
        # Reset cleaned_phone_no
        cleaned_phone_no = ''

        # Getting values from StringVar variables
        name = self.namevalue.get()
        phone_no = self.phone_novalue.get()
        address = self.addressvalue.get()

        print("Name:", name)
        print("Phone no:", phone_no)
        print("Address:", address)

        # Phone number validation
        cleaned_phone_no = ''.join(c for c in phone_no if c.isdigit())

        if not cleaned_phone_no.isdigit() or len(cleaned_phone_no) != 10:

            messagebox.showerror("Error", "Please enter a valid 10-digit phone number.")
            return


        # Inserting data into the MySQL database
        insert_query = "INSERT INTO cust (name, phone, address) VALUES (%s, %s, %s)"
        values = (name, cleaned_phone_no, address)
        self.cursor.execute(insert_query, values)

        # Commit the changes to the database
        self.db.commit()

        # Displaying the values in a messagebox
        message = f"Name: {name}\nPhone no: {cleaned_phone_no}\nAddress: {address}\nData stored in MySQL database."
        messagebox.showinfo("Customer Details", message)

        # Open the project selection page
        self.open_project_page()

    def open_project_page(self):
        self.root.destroy()  # Close the current window

        # Create a new window for the project selection page
        project_root = tk.Tk()
        project_app = bag.BagStock(project_root)  # Assuming BagStock is a class in bag.py
        project_root.mainloop()

def run_customer_registration_form():
    root = tk.Tk()
    app = Customer(root)
    root.mainloop()

if __name__ == "__main__":
    run_customer_registration_form()
this is two files code if i run this code sequenciely then  customer register.py in that file phone 
numbar validation is npot working properly  after giving correct 10 didig number it is showing error
 but if i only run customer.py file then it working ehat is proble fix it plz  
 give the comple code of both files one is main.py tn that file there is login page after
  succfully login we wnt home page and in home page we click customer 
 registation thaen we went customer.py file  so give this both files modified code
 8888888888888888********************************************************************
 import tkinter as tk
from tkinter import messagebox
from bag import BagSelection
from stock import StockManagement
from supplier import SupplierManagement

user_database = {
    "a": "a",
    "user1": "12345",
    # Add more users if needed
}

def authenticate(username, password):
    if username in user_database and user_database[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_home_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def run_bag_selection_page():
    app = BagSelection(root)
    app.calculate_bill
    root.mainloop()

def open_stock_management_page():
   # root.withdraw()
    run_stock_management_page()

def run_stock_management_page():
    root_stock = tk.Tk()
    app_stock = StockManagement(root_stock)
    root_stock.mainloop()

def open_supplier_management():
    root_supplier = tk.Toplevel(root)
    app_supplier = SupplierManagement(root_supplier)
    root_supplier.mainloop()

def open_reports():
    print("Opening Reports Page")

def open_home_page():
    root.deiconify()
    login_window.destroy()
    root.attributes('-fullscreen', True)

def minimize_window():
    root.iconify()

def close_window():
    root.destroy()

def minimize_login_window():
    login_window.iconify()

def close_login_window():
    login_window.destroy()

def show_login_page():
    global login_window
    login_window = tk.Toplevel(root)
    login_window.title("Login Page")

    window_width = 800
    window_height = 500
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    login_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    login_window.configure(bg="#f5f5f5")

    login_frame = tk.Frame(login_window, bg="#ffffff", bd=5)
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    heading_label = tk.Label(login_frame, text="Login Panel", font=("Helvetica", 24, "bold"), bg="#ffffff", fg="#333333")
    heading_label.grid(row=0, column=0, columnspan=2, pady=20)

    label_username = tk.Label(login_frame, text="Username:", font=("Helvetica", 16), bg="#ffffff", fg="#333333")
    label_username.grid(row=1, column=0, padx=20, pady=10, sticky="e")
    entry_username = tk.Entry(login_frame, font=("Helvetica", 16))
    entry_username.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    label_password = tk.Label(login_frame, text="Password:", font=("Helvetica", 16), bg="#ffffff", fg="#333333")
    label_password.grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_password = tk.Entry(login_frame, show="*", font=("Helvetica", 16))
    entry_password.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    login_button = tk.Button(login_frame, text="Login", command=lambda: authenticate(entry_username.get(), entry_password.get()), font=("Helvetica", 16), bg="#4CAF50", fg="white", relief="flat")
    login_button.grid(row=3, column=0, columnspan=2, pady=20)

    minimize_btn = tk.Button(login_window, text="_", font=("Arial", 12), bd=0, bg="#f5f5f5", fg="#333333", command=minimize_login_window)
    minimize_btn.place(x=login_window.winfo_screenwidth()-70, y=0, width=30, height=30)

    close_btn = tk.Button(login_window, text="X", font=("Arial", 12), bd=0, bg="#f5f5f5", fg="#333333", command=close_login_window)
    close_btn.place(x=login_window.winfo_screenwidth()-35, y=0, width=30, height=30)

    login_window.attributes('-fullscreen', True)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bag House Management System")
    root.withdraw()

    nav_bar = tk.Frame(root, bg="#4CAF50", bd=2)
    nav_bar.pack(side="top", fill="x")

    home_btn = tk.Button(nav_bar, text="Home", command=open_home_page, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
    home_btn.pack(side="left", padx=10, pady=5)

    bag_selection_btn = tk.Button(nav_bar, text="Bag Selection", command=run_bag_selection_page, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
    bag_selection_btn.pack(side="left", padx=10, pady=5)

    stock_management_btn = tk.Button(nav_bar, text="Stock Management", command=open_stock_management_page, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
    stock_management_btn.pack(side="left", padx=10, pady=5)

    supplier_management_btn = tk.Button(nav_bar, text="Supplier Management", command=open_supplier_management, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
    supplier_management_btn.pack(side="left", padx=10, pady=5)

    reports_btn = tk.Button(nav_bar, text="Reports", command=open_reports, font=("Arial", 12), bg="#4CAF50", fg="white", relief="flat")
    reports_btn.pack(side="left", padx=10, pady=5)

    minimize_btn = tk.Button(root, text="_", font=("Arial", 12), bd=0, bg="#f5f5f5", fg="#333333", command=minimize_window)
    minimize_btn.place(x=root.winfo_screenwidth()-70, y=0, width=30, height=30)

    close_btn = tk.Button(root, text="X", font=("Arial", 12), bd=0, bg="#f5f5f5", fg="#333333", command=close_window)
    close_btn.place(x=root.winfo_screenwidth()-35, y=0, width=30, height=30)

    show_login_page()
    root.mainloop()
