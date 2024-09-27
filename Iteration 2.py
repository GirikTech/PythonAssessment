import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

# Class to represent a user with a username and password
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Class to represent a product with a name and price
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

# Main application class for the Invoice Maker
class InvoiceMaker:
    def __init__(self):
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Invoice Maker - Iteration 2")
        self.root.geometry("400x500", ) # Set window size


        # Load existing user data from a JSON file
        self.users = self.load_data("users.json")
        self.current_user = None # To store the logged-in user
        self.products = []  # List to store added products
        
        self.setup_ui() # Setup the UI components
        

     # Function to setup the user interface
    def setup_ui(self):
        # Notebook widget to manage multiple frames (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")
        

        # Creating frames for login, signup, product addition, and invoice display
        self.login_frame = ttk.Frame(self.notebook)
        self.signup_frame = ttk.Frame(self.notebook)
        self.product_frame = ttk.Frame(self.notebook)
        self.invoice_frame = ttk.Frame(self.notebook)

        # Adding frames (tabs) to the notebook
        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.signup_frame, text="Sign Up")

        # Login Frame UI elements
        ttk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        ttk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*") # Hide password input
        self.password_entry.pack(pady=5)
        ttk.Button(self.login_frame, text="Login", command=self.login).pack(pady=10) # Button to trigger login

        # Signup Frame UI elements
        ttk.Label(self.signup_frame, text="Username:").pack(pady=5)
        self.new_username_entry = ttk.Entry(self.signup_frame)
        self.new_username_entry.pack(pady=5)
        ttk.Label(self.signup_frame, text="Password:").pack(pady=5)
        self.new_password_entry = ttk.Entry(self.signup_frame, show="*")  # Hide password input
        self.new_password_entry.pack(pady=5)
        ttk.Button(self.signup_frame, text="Sign Up", command=self.signup).pack(pady=10) # Button to trigger signup

        # Product Frame UI elements
        ttk.Label(self.product_frame, text="Product Name:").pack(pady=5)
        self.product_name_entry = ttk.Entry(self.product_frame)
        self.product_name_entry.pack(pady=5)
        ttk.Label(self.product_frame, text="Product Price:").pack(pady=5)
        self.product_price_entry = ttk.Entry(self.product_frame)
        self.product_price_entry.pack(pady=5)
        ttk.Button(self.product_frame, text="Add Product", command=self.add_product).pack(pady=10) # Button to add products
        self.product_list = tk.Listbox(self.product_frame, height=5) # Listbox to display added products
        self.product_list.pack(pady=10)
        ttk.Button(self.product_frame, text="Generate Invoice", command=self.show_invoice).pack(pady=10) # Button to generate invoice

        # Invoice Frame UI elements
        self.invoice_text = tk.Text(self.invoice_frame, height=10, width=40) # Text area to display the invoice
        self.invoice_text.pack(pady=10)
        ttk.Button(self.invoice_frame, text="Save Invoice", command=self.save_invoice).pack(pady=10) # Button to save invoice

    # Function to load data from a JSON file
    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f) # Load and return data from file
        except FileNotFoundError:
            return {} # Return empty dictionary if file not found
    
    # Function to save data to a JSON file
    def save_data(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f) # Save data to file in JSON format

    # Function to handle user login
    def login(self):
        username = self.username_entry.get() # Get entered username
        password = self.password_entry.get() # Get entered password
        if username in self.users and self.users[username] == password: # Check if user exists and password matches
            self.current_user = User(username, password) # Set the current user
            self.notebook.forget(self.login_frame) # Remove login frame
            self.notebook.forget(self.signup_frame) # Remove signup frame
            self.notebook.add(self.product_frame, text="Products")  # Add product frame to notebook
            messagebox.showinfo("Success", f"Welcome, {username}!")  # Show success message
        else:
            messagebox.showerror("Error", "Invalid username or password") # Show error message for invalid login

    # Function to handle user signup
    def signup(self):
        username = self.new_username_entry.get() # Get entered new username
        password = self.new_password_entry.get() # Get entered new password
        if username and password:
            if username not in self.users: # Check if username does not already exist
                self.users[username] = password # Add new user to users dictionary
                self.save_data(self.users, "users.json") # Save updated users to file
                messagebox.showinfo("Success", "Account created! You can now log in.") # Show success message
                self.notebook.select(self.login_frame) # Switch to login frame
            else:
                messagebox.showerror("Error", "Username already exists") # Show error if username already exists
        else:
            messagebox.showerror("Error", "Please enter both username and password") # Show error for empty fields
    
    # Function to add a product to the list
    def add_product(self):
        name = self.product_name_entry.get() # Get the product name
        price = self.product_price_entry.get() # Get the product price
        try:
            price = float(price)  # Try converting price to float
            if price < 0:
                raise ValueError # Raise error if price is not positive
            product = Product(name, price) # Create a Product object
            self.products.append(product) # Add product to the list
            self.product_list.insert(tk.END, f"{name}: ${price:.2f}") # Insert product into the Listbox
            self.product_name_entry.delete(0, tk.END) # Clear the product name entry
            self.product_price_entry.delete(0, tk.END) # Clear the product price entry
        except ValueError:
            messagebox.showerror("Error", "Invalid price. Please enter a positive number.") # Show error for invalid price

    # Function to show the invoice
    def show_invoice(self):
        if not self.products:
            messagebox.showerror("Error", "No products added yet") # Show error if no products are added
            return

        total = sum(product.price for product in self.products) # Calculate total price
        invoice_text = f"Invoice for {self.current_user.username}\n" # Start invoice text
        invoice_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" # Add current date and time
        for product in self.products:
            invoice_text += f"{product.name}: ${product.price:.2f}\n" # List each product and its price
        invoice_text += f"\nTotal: ${total:.2f}" # Add total to invoice text

        self.invoice_text.delete(1.0, tk.END) # Clear the invoice display area
        self.invoice_text.insert(tk.END, invoice_text) # Insert the invoice text
        self.notebook.forget(self.product_frame) # Remove the product frame
        self.notebook.add(self.invoice_frame, text="Invoice") # Add the invoice frame
        self.notebook.select(self.invoice_frame) # Switch to the invoice frame

    # Function to save the invoice to a file
    def save_invoice(self):
        invoice_content = self.invoice_text.get(1.0, tk.END) # Get the content of the invoice
        filename = f"invoice_{self.current_user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt" # Generate a unique filename
        with open(filename, 'w') as f:
            f.write(invoice_content) # Write the invoice content to the file
        messagebox.showinfo("Success", f"Invoice saved to {filename}") # Show success message

    # Function to run the main loop of the application
    def run(self):
        self.root.mainloop()

# Entry point of the program
if __name__ == "__main__":
    app = InvoiceMaker() # Create an instance of the InvoiceMaker class
    app.run() # Run the application