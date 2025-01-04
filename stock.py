import tkinter as tk
from tkinter import ttk, Label, messagebox  # Import messagebox module

import mysql.connector

class StockManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Management")

        # Set window size and position
        window_width = 1400
        window_height = 700
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

       
        bg_color = "#add8e6"  # Light blue

        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Enter your MySQL password
            database="bag"
        )
        self.cursor = self.db.cursor()

        # Create a frame for bag selection
        bag_frame = tk.Frame(root, bg=bg_color, padx=20, pady=20)
        bag_frame.pack(fill=tk.BOTH, expand=True)

        # Heading for bag selection
        Label(bag_frame, text="Bag stock", font=("Helvetica", 24, "bold"), fg="#4169e1", bg=bg_color).pack(pady=15)

        # Create Treeview widget
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=bg_color, foreground="#000000", fieldbackground=bg_color)
        style.map("Treeview", background=[("selected", "#0078d7")])
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 12))
        self.tree = ttk.Treeview(bag_frame, columns=("bid", "Product Name", "Price", "Quantity"), show="headings", selectmode="browse")
        self.tree.heading("#1", text="bid")
        self.tree.heading("#2", text="Product Name")
        self.tree.heading("#3", text="Price")
        self.tree.heading("#4", text="Quantity")
        self.tree.column("#1", anchor=tk.CENTER, width=100)
        self.tree.column("#2", anchor=tk.CENTER, width=200)
        self.tree.column("#3", anchor=tk.CENTER, width=100)
        self.tree.column("#4", anchor=tk.CENTER, width=100)
        self.tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Bind double click event to delete record
        self.tree.bind("<Double-1>", self.delete_record)

        # Fetch and insert data into Treeview
        self.fetch_and_insert_data()

    def fetch_and_insert_data(self):
        # Clear existing data in the Treeview
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Fetch bag stock data from the database
        self.cursor.execute("SELECT bid, product_name, price, quantity FROM bag_stock")
        rows = self.cursor.fetchall()

        # Insert data into Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def delete_record(self, event):
        # Get the selected item from the Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            return

        # Prompt user for confirmation
        if not messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?"):
            return

        # Get data from the selected item
        item_data = self.tree.item(selected_item, 'values')
        if not item_data:
            return

        # Delete the selected record from the database
        delete_query = "DELETE FROM bag_stock WHERE bid = %s"
        self.cursor.execute(delete_query, (item_data[0],))
        self.db.commit()

        # Update Treeview with new data
        self.fetch_and_insert_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockManagement(root)
    root.mainloop()
