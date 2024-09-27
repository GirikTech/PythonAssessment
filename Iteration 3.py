import tkinter as tk
from tkinter import messagebox, ttk, font
import json
from datetime import datetime

# Class to represent a user with username, password, role, and associated business
class User: 
    def __init__(self, username, password, role, business):
        self.username = username  
        self.password = password  
        self.role = role 
        self.business = business

# Class to represent a product with name, price, and the user who added it
class Product:
    def __init__(self, name, price, added_by):
        self.name = name 
        self.price = price 
        self.added_by = added_by 

# Main application class for InvoiceMaker
class InvoiceMaker:
    def __init__(self):
        # Initialise the root window and set title, size, and colors
        self.root = tk.Tk()
        self.root.title("Invoice Maker - Iteration 3")
        self.root.geometry("400x1000")
        self.bg_color = "#f0f0f0"  # Light gray background
        self.accent_color = "#4a90e2"  # Blue accent
        self.text_color = "#333333"  # Dark gray text
        self.root.configure(bg=self.bg_color)

        # Configure default font size and family for the application
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=16, family="Helvetica")
        self.root.option_add("*Font", default_font)

        # Create a custom style for ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use 'clam' theme as base
        self.style.configure('TFrame', background=self.bg_color) # Set frame background
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color) # Label style
        self.style.configure('TButton', background=self.accent_color, foreground='white') # Button style
        self.style.map('TButton', background=[('active', self.accent_color)]) # Button hover style
        self.style.configure('TEntry', fieldbackground='white', foreground=self.text_color) # Entry field style 
        self.style.configure('Treeview', background='white', fieldbackground='white', foreground=self.text_color) # Treeview style
        self.style.configure('Treeview.Heading', background=self.accent_color, foreground='white') # Treeview heading

        # Initialise user and data storage variables
        self.current_user = None
        self.users = self.load_data("3users.json")
        self.products = self.load_data("3products.json")
        self.purchase_history = self.load_data("3purchase_history.json")

        # Setup the user interface components
        self.setup_ui()

     # Load data from JSON files
    def load_data(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f) # Return loaded data
        except FileNotFoundError:
            return {} # Return empty dictionary if file is not found

     # Save data to JSON files
    def save_data(self, data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f) # Save data as JSON

    # Setup main UI layout and frames
    def setup_ui(self):
        # Notebook widget for tab navigation
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        # Creating different frames (tabs) for login, signup, products, invoices, and history
        self.login_frame = ttk.Frame(self.notebook, style='TFrame')
        self.signup_frame = ttk.Frame(self.notebook, style='TFrame')
        self.product_frame = ttk.Frame(self.notebook, style='TFrame')
        self.invoice_frame = ttk.Frame(self.notebook, style='TFrame')
        self.history_frame = ttk.Frame(self.notebook, style='TFrame')

        # Add login and signup frames to the notebook initially
        self.notebook.add(self.login_frame, text="Login")
        self.notebook.add(self.signup_frame, text="Sign Up")

        # Setup each frame's layout and widgets
        self.setup_login_frame()
        self.setup_signup_frame()
        self.setup_product_frame()
        self.setup_invoice_frame()
        self.setup_history_frame()

    # Login frame setup: username, password fields, and login button
    def setup_login_frame(self):
        ttk.Label(self.login_frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)
        ttk.Label(self.login_frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.pack(pady=5)
        ttk.Button(self.login_frame, text="Login", command=self.login).pack(pady=10)

    # Signup frame setup: username, password, role selection, and business input
    def setup_signup_frame(self):
        ttk.Label(self.signup_frame, text="Username:").pack(pady=5)
        self.new_username_entry = ttk.Entry(self.signup_frame)
        self.new_username_entry.pack(pady=5)
        ttk.Label(self.signup_frame, text="Password:").pack(pady=5)
        self.new_password_entry = ttk.Entry(self.signup_frame, show="*")
        self.new_password_entry.pack(pady=5)
        ttk.Label(self.signup_frame, text="Role:").pack(pady=5)
        self.role_var = tk.StringVar(value="employee")
        ttk.Radiobutton(self.signup_frame, text="Employee", variable=self.role_var, value="employee").pack()
        ttk.Radiobutton(self.signup_frame, text="Owner", variable=self.role_var, value="owner").pack()
        ttk.Label(self.signup_frame, text="Business:").pack(pady=5)
        self.business_entry = ttk.Entry(self.signup_frame)
        self.business_entry.pack(pady=5)
        ttk.Button(self.signup_frame, text="Sign Up", command=self.signup).pack(pady=10)

    # Product frame setup: form for adding products and a treeview to display them
    def setup_product_frame(self):
        ttk.Label(self.product_frame, text="Product Name:", style='TLabel').pack(pady=(20,5))
        self.product_name_entry = ttk.Entry(self.product_frame, width=40)
        self.product_name_entry.pack(pady=5)
        
        ttk.Label(self.product_frame, text="Product Price:", style='TLabel').pack(pady=(15,5))
        self.product_price_entry = ttk.Entry(self.product_frame, width=40)
        self.product_price_entry.pack(pady=5)
        
        # Button to add products and treeview to display them
        ttk.Button(self.product_frame, text="Add Product", command=self.add_product, style='TButton').pack(pady=20)
        
        # Treeview to display the list of products
        self.product_tree = ttk.Treeview(self.product_frame, columns=('Name', 'Price', 'Added By'), show='headings', style='Treeview')
        self.product_tree.heading('Name', text='Name')
        self.product_tree.heading('Price', text='Price')
        self.product_tree.heading('Added By', text='Added By')
        self.product_tree.pack(pady=20, fill='both', expand=True)
        
        # Buttons to generate invoices and view purchase history
        button_frame = ttk.Frame(self.product_frame, style='TFrame')
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Generate Invoice", command=self.show_invoice, style='TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="View Purchase History", command=self.show_history, style='TButton').pack(side='left', padx=10)
    
    # History frame setup to display past purchase history
    def setup_history_frame(self):
        self.history_tree = ttk.Treeview(self.history_frame, columns=('Date', 'Total'), show='headings')
        self.history_tree.heading('Date', text='Date')
        self.history_tree.heading('Total', text='Total')
        self.history_tree.pack(pady=10, expand=True, fill="both")
        ttk.Button(self.history_frame, text="Back to Products", command=self.back_to_products).pack(pady=10)

    def show_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        if self.current_user.business in self.purchase_history:
            for purchase in self.purchase_history[self.current_user.business]:
                self.history_tree.insert('', 'end', values=(purchase['date'], f"${purchase['total']:.2f}"))
        self.notebook.forget(self.product_frame)
        self.notebook.add(self.history_frame, text="Purchase History")
        self.notebook.select(self.history_frame)

    # Invoice frame setup for generating and displaying invoices
    def setup_invoice_frame(self):
        self.invoice_text = tk.Text(self.invoice_frame, height=15, width=50, bg=self.bg_color, fg="black")
        self.invoice_text.pack(pady=10)
        ttk.Button(self.invoice_frame, text="Save Invoice", command=self.save_invoice).pack(pady=10)
        ttk.Button(self.invoice_frame, text="Back to Products", command=self.back_to_products).pack(pady=10)

    # Function to handle user login
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Validate username and password
        if username in self.users and self.users[username]['password'] == password:
            user_data = self.users[username]
            self.current_user = User(username, password, user_data['role'], user_data['business'])
            self.notebook.forget(self.login_frame)
            self.notebook.forget(self.signup_frame)
            self.notebook.add(self.product_frame, text="Products")
            self.load_products()
            messagebox.showinfo("Success", f"Welcome, {username}!")
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    # Function to handle user signup
    def signup(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        role = self.role_var.get()
        business = self.business_entry.get()
        # Validate inputs and create new user
        if username and password and business:
            if username not in self.users:
                self.users[username] = {
                    'password': password,
                    'role': role,
                    'business': business
                }
                self.save_data(self.users, "users.json")
                messagebox.showinfo("Success", "Account created! You can now log in.")
                self.notebook.select(self.login_frame)
            else:
                messagebox.showerror("Error", "Username already exists")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    # Function to add products to the list
    def add_product(self):
        name = self.product_name_entry.get()
        price = self.product_price_entry.get()
        try:
            price = float(price)
            if price < 0:
                raise ValueError
            if self.current_user.business not in self.products:
                self.products[self.current_user.business] = []
            # Add product to the business's product list
            self.products[self.current_user.business].append({
                'name': name,
                'price': price,
                'added_by': self.current_user.username
            })
            self.save_data(self.products, "products.json")
            self.load_products()
            self.product_name_entry.delete(0, tk.END)
            self.product_price_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid price. Please enter a positive number.")

    # Function to load products into the treeview
    def load_products(self):
        self.product_tree.delete(*self.product_tree.get_children())
        if self.current_user.business in self.products:
            for product in self.products[self.current_user.business]:
                self.product_tree.insert('', 'end', values=(product['name'], f"${product['price']:.2f}", product['added_by']))
    
    # Function to show invoice for the current business
    def show_invoice(self):
        if self.current_user.business not in self.products or not self.products[self.current_user.business]:
            messagebox.showerror("Error", "No products added yet")
            return

        total = sum(product['price'] for product in self.products[self.current_user.business]) # Calculate total price
        invoice_text = f"Invoice for {self.current_user.business}\n" # Start invoice text
        invoice_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n" # Add current date and time
        for product in self.products[self.current_user.business]:
            invoice_text += f"{product['name']}: ${product['price']:.2f}\n" # List each product and its price
        invoice_text += f"\nTotal: ${total:.2f}" # Add total to invoice text

        self.invoice_text.delete(1.0, tk.END)
        self.invoice_text.insert(tk.END, invoice_text)
        self.notebook.forget(self.product_frame)
        self.notebook.add(self.invoice_frame, text="Invoice")
        self.notebook.select(self.invoice_frame)

    # Function to navigate back to the product frame
    def back_to_products(self):
        self.notebook.forget(self.notebook.select()) 
        self.notebook.add(self.product_frame, text="Products")
        self.notebook.select(self.product_frame) # Switch to the invoice frame

    # Function to save the generated invoice as a file and store purchase history
    def save_invoice(self):
        invoice_content = self.invoice_text.get(1.0, tk.END) # Get the content of the invoice
        filename = f"invoice_{self.current_user.business}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt" # Generate a unique filename
        with open(filename, 'w') as f:
            f.write(invoice_content) # Write the invoice content to the file
        
        # Save the invoice to the purchase history
        if self.current_user.business not in self.purchase_history:
            self.purchase_history[self.current_user.business] = []
        
        total = sum(product['price'] for product in self.products[self.current_user.business])
        self.purchase_history[self.current_user.business].append({
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total': total
        })
        self.save_data(self.purchase_history, "purchase_history.json")
        
        messagebox.showinfo("Success", f"Invoice saved to {filename}") # Show success message
     
    # Function to run the main loop of the application
    def run(self):
        self.root.mainloop()

# Entry point of the program
if __name__ == "__main__":
    app = InvoiceMaker() # Create an instance of the InvoiceMaker class
    app.run() # Run the application