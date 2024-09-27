import tkinter as tk
from tkinter import messagebox
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
        # Initialise the main window
        self.root = tk.Tk()
        self.root.title("Invoice Maker - Iteration 1")
        self.current_user = None  # To store the logged-in user
        self.products = []  # List to store added products
        self.setup_ui()  # Setup the UI components

    # Function to setup the user interface
    def setup_ui(self):
        # Frames for different sections of the application
        self.login_frame = tk.Frame(self.root)
        self.product_frame = tk.Frame(self.root)
        self.invoice_frame = tk.Frame(self.root)

        # Login Frame UI elements
        tk.Label(self.login_frame, text="Username:").pack()
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.pack()
        tk.Label(self.login_frame, text="Password:").pack()
        self.password_entry = tk.Entry(self.login_frame, show="*")  # Hide password input
        self.password_entry.pack()
        tk.Button(self.login_frame, text="Login", command=self.login).pack()  # Button to trigger login

        # Product Frame UI elements
        tk.Label(self.product_frame, text="Product Name:").pack()
        self.product_name_entry = tk.Entry(self.product_frame)
        self.product_name_entry.pack()
        tk.Label(self.product_frame, text="Product Price:").pack()
        self.product_price_entry = tk.Entry(self.product_frame)
        self.product_price_entry.pack()
        tk.Button(self.product_frame, text="Add Product", command=self.add_product).pack()  # Button to add products
        tk.Button(self.product_frame, text="Generate Invoice", command=self.generate_invoice).pack()  # Moved Generate Invoice button here

        # Invoice Frame UI elements
        self.invoice_display = tk.Text(self.invoice_frame, height=10, width=40)  # Text area to display the invoice
        self.invoice_display.pack()

        self.login_frame.pack()  # Show login frame initially

    # Function to handle user login
    def login(self):
        username = self.username_entry.get()  # Get the entered username
        password = self.password_entry.get()  # Get the entered password
        if username and password:
            self.current_user = User(username, password)  # Create a User object if both fields are filled
            self.login_frame.pack_forget()  # Hide the login frame
            self.product_frame.pack()  # Show the product frame
        else:
            messagebox.showerror("Error", "Please enter both username and password")  # Error if fields are empty

    # Function to add a product to the list
    def add_product(self):
        name = self.product_name_entry.get()  # Get the product name
        price = self.product_price_entry.get()  # Get the product price
        try:
            price = float(price)  # Try converting price to float
            if price < 0:
                raise ValueError  # Raise error if price is not positive
            self.products.append(Product(name, price))  # Add product to the list
            messagebox.showinfo("Success", "Product added!")  # Show success message
            self.product_name_entry.delete(0, tk.END)  # Clear the product name entry
            self.product_price_entry.delete(0, tk.END)  # Clear the product price entry
        except ValueError:
            messagebox.showerror("Error", "Invalid price. Please enter a positive number.")  # Error for invalid price

    # Function to generate the invoice
    def generate_invoice(self):
        if not self.products:
            messagebox.showerror("Error", "No products added yet")  # Error if no products are added
            return

        total = sum(product.price for product in self.products)  # Calculate total price
        invoice_text = f"Invoice for {self.current_user.username}\n"  # Start invoice text
        invoice_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"  # Add current date and time
        for product in self.products:
            invoice_text += f"{product.name}: ${product.price:.2f}\n"  # List each product and its price
        invoice_text += f"\nTotal: ${total:.2f}"  # Add total to invoice text

        self.invoice_display.delete(1.0, tk.END)  # Clear the invoice display area
        self.invoice_display.insert(tk.END, invoice_text)  # Insert the invoice text
        self.product_frame.pack_forget()  # Hide the product frame
        self.invoice_frame.pack()  # Show the invoice frame

        # Save invoice to a text file
        filename = f"invoice_{self.current_user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(invoice_text)  # Write invoice to the file
        messagebox.showinfo("Success", f"Invoice saved to {filename}")  # Show success message

    # Function to run the main loop of the application
    def run(self):
        self.root.mainloop()

# Entry point of the program
if __name__ == "__main__":
    app = InvoiceMaker()  # Create an instance of InvoiceMaker
    app.run()  # Run the application
