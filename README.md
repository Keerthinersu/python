import tkinter as tk
from tkinter import messagebox

# Sample in-memory accounts
accounts = {}  # Format: {account_number: {'pin': '1234', 'balance': 1000}}

# Main Application
class ATMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python ATM")
        self.geometry("400x300")
        self.resizable(False, False)
        self.current_user = None

        self.frames = {}

        for F in (StartPage, CreateAccountPage, LoginPage, MenuPage):
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = frame

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Start Page
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Welcome to Python ATM", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self, text="Create Account", width=20,
                  command=lambda: controller.show_frame("CreateAccountPage")).pack(pady=5)
        tk.Button(self, text="Login", width=20,
                  command=lambda: controller.show_frame("LoginPage")).pack(pady=5)

# Create Account Page
class CreateAccountPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Create Account", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(self, text="Account Number").pack()
        self.acc_entry = tk.Entry(self)
        self.acc_entry.pack()

        tk.Label(self, text="4-digit PIN").pack()
        self.pin_entry = tk.Entry(self, show='*')
        self.pin_entry.pack()

        tk.Button(self, text="Create", command=self.create_account).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage")).pack()

    def create_account(self):
        acc = self.acc_entry.get()
        pin = self.pin_entry.get()

        if acc in accounts:
            messagebox.showerror("Error", "Account already exists!")
        elif not pin.isdigit() or len(pin) != 4:
            messagebox.showerror("Error", "PIN must be 4 digits")
        else:
            accounts[acc] = {'pin': pin, 'balance': 0.0}
            messagebox.showinfo("Success", "Account created!")
            self.acc_entry.delete(0, 'end')
            self.pin_entry.delete(0, 'end')
            self.controller.show_frame("StartPage")

# Login Page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Login", font=("Helvetica", 14)).pack(pady=10)

        tk.Label(self, text="Account Number").pack()
        self.acc_entry = tk.Entry(self)
        self.acc_entry.pack()

        tk.Label(self, text="PIN").pack()
        self.pin_entry = tk.Entry(self, show='*')
        self.pin_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("StartPage")).pack()

    def login(self):
        acc = self.acc_entry.get()
        pin = self.pin_entry.get()

        if acc in accounts and accounts[acc]['pin'] == pin:
            self.controller.current_user = acc
            self.controller.show_frame("MenuPage")
        else:
            messagebox.showerror("Error", "Invalid credentials!")

# Menu Page (After Login)
class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="ATM Menu", font=("Helvetica", 14)).pack(pady=10)

        tk.Button(self, text="Check Balance", width=20, command=self.check_balance).pack(pady=5)
        tk.Button(self, text="Deposit", width=20, command=self.deposit).pack(pady=5)
        tk.Button(self, text="Withdraw", width=20, command=self.withdraw).pack(pady=5)
        tk.Button(self, text="Logout", width=20, command=self.logout).pack(pady=5)

    def check_balance(self):
        acc = self.controller.current_user
        balance = accounts[acc]['balance']
        messagebox.showinfo("Balance", f"Your balance is ₹{balance:.2f}")

    def deposit(self):
        amount = simple_input("Enter amount to deposit:")
        if amount is not None:
            accounts[self.controller.current_user]['balance'] += amount
            messagebox.showinfo("Success", f"₹{amount:.2f} deposited!")

    def withdraw(self):
        amount = simple_input("Enter amount to withdraw:")
        acc = self.controller.current_user
        if amount is not None:
            if amount <= accounts[acc]['balance']:
                accounts[acc]['balance'] -= amount
                messagebox.showinfo("Success", f"₹{amount:.2f} withdrawn!")
            else:
                messagebox.showerror("Error", "Insufficient balance")

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("StartPage")

# Helper function to take numeric input
def simple_input(prompt):
    def on_ok():
        try:
            val = float(entry.get())
            top.destroy()
            result.append(val)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number")

    result = []
    top = tk.Toplevel()
    top.title("Input")
    tk.Label(top, text=prompt).pack(pady=5)
    entry = tk.Entry(top)
    entry.pack(pady=5)
    tk.Button(top, text="OK", command=on_ok).pack()
    top.wait_window()
    return result[0] if result else None

# Run the app
if __name__ == "__main__":
    app = ATMApp()
    app.mainloop()

