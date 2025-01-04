import tkinter as tk
from tkinter import messagebox
from bag import BagSelection
from stock import StockManagement
from supplier import SupplierManagement
from tkinter import Scrollbar
import record


user_database = {
    "admin": "password",

}

def authenticate(username, password):
    if username in user_database and user_database[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        open_home_page()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def run_bag_selection_page():
    app = BagSelection(root)
   # app.calculate_bill
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

def open_records():
    # Import the run_database_viewer function from records.py
    from record import run_database_viewer
    # Run the function to open the database viewer
    run_database_viewer()


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

    login_window.configure(bg="#6FB1FC")  # Soft blue 

    login_frame = tk.Frame(login_window, bg="#FFFFFF", bd=5)
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    heading_label = tk.Label(login_frame, text="Login page", font=("Helvetica", 24, "bold"), bg="#FFFFFF", fg="#333333")
    heading_label.grid(row=0, column=0, columnspan=2, pady=20)

    label_username = tk.Label(login_frame, text="Username:", font=("Helvetica", 16), bg="#FFFFFF", fg="#333333")
    label_username.grid(row=1, column=0, padx=20, pady=10, sticky="e")
    entry_username = tk.Entry(login_frame, font=("Helvetica", 16))
    entry_username.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    label_password = tk.Label(login_frame, text="Password:", font=("Helvetica", 16), bg="#FFFFFF", fg="#333333")
    label_password.grid(row=2, column=0, padx=20, pady=10, sticky="e")
    entry_password = tk.Entry(login_frame, show="*", font=("Helvetica", 16))
    entry_password.grid(row=2, column=1, padx=20, pady=10, sticky="w")

    login_button = tk.Button(login_frame, text="Login", command=lambda: authenticate(entry_username.get(), entry_password.get()), font=("Helvetica", 16), bg="#4CAF50", fg="white", relief="flat")
    login_button.grid(row=3, column=0, columnspan=2, pady=20)

    minimize_btn = tk.Button(login_window, text="_", font=("Arial", 12), bd=0, bg="#6FB1FC", fg="#333333", command=minimize_login_window)
    minimize_btn.place(x=login_window.winfo_screenwidth()-70, y=0, width=30, height=30)

    close_btn = tk.Button(login_window, text="X", font=("Arial", 12), bd=0, bg="#6FB1FC", fg="#333333", command=close_login_window)
    close_btn.place(x=login_window.winfo_screenwidth()-35, y=0, width=30, height=30)

    login_window.attributes('-fullscreen', True)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bag House Management System")
    root.withdraw()

    nav_bar = tk.Frame(root, bg="#6FB1FC", bd=2)
    nav_bar.pack(side="top", fill="x")

    home_btn = tk.Button(nav_bar, text="Home", command=open_home_page, font=("Arial", 12, "bold"), bg="#6FB1FC", fg="white", relief="flat", padx=10, pady=5)
    home_btn.pack(side="left")

    bag_selection_btn = tk.Button(nav_bar, text="Bag Selection", command=run_bag_selection_page, font=("Arial", 12), bg="#6FB1FC", fg="white", relief="flat", padx=10, pady=5)
    bag_selection_btn.pack(side="left")

    stock_management_btn = tk.Button(nav_bar, text="Stock Management", command=open_stock_management_page, font=("Arial", 12), bg="#6FB1FC", fg="white", relief="flat", padx=10, pady=5)
    stock_management_btn.pack(side="left")

    supplier_management_btn = tk.Button(nav_bar, text="Supplier Management", command=open_supplier_management, font=("Arial", 12), bg="#6FB1FC", fg="white", relief="flat", padx=10, pady=5)
    supplier_management_btn.pack(side="left")

    records_btn = tk.Button(nav_bar, text="Records", command=open_records, font=("Arial", 12), bg="#6FB1FC", fg="white", relief="flat", padx=10, pady=5)
    records_btn.pack(side="left")

    minimize_btn = tk.Button(root, text="_", font=("Arial", 12), bd=0, bg="#f5f5f5", fg="#333333", command=minimize_window)
    minimize_btn.place(x=root.winfo_screenwidth()-70, y=0, width=30, height=30)

    close_btn = tk.Button(root, text="X", font=("Arial", 12), bd=0, bg="#f5f5f5", fg="#333333", command=close_window)
    close_btn.place(x=root.winfo_screenwidth()-35, y=0, width=30, height=30)

    show_login_page()
    root.mainloop()
