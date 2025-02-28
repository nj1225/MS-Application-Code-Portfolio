import json
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            initial_budget REAL
        )
    """)
    conn.commit()
    conn.close()

# Function to add an expense
def add_expense(description, amount):
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (description, amount) VALUES (?, ?)", (description, amount))
    conn.commit()
    conn.close()
    print(f"Added expense: {description}, Amount: {amount}")

# Function to get total expenses
def get_total_expenses():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0  # Return 0 if no expenses exist
    conn.close()
    return total

# Function to get all expenses
def get_expenses():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT description, amount FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return [{"description": desc, "amount": amt} for desc, amt in expenses]

# Function to set initial budget
def set_initial_budget(amount):
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budget")  # Clear previous budget entry
    cursor.execute("INSERT INTO budget (initial_budget) VALUES (?)", (amount,))
    conn.commit()
    conn.close()

# Function to get initial budget
def get_initial_budget():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT initial_budget FROM budget ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

# Function to get remaining balance
def get_balance():
    budget = get_initial_budget()
    return budget - get_total_expenses()

# Function to show budget details
def show_budget_details():
    budget = get_initial_budget()
    expenses = get_expenses()
    
    print(f"\nTotal Budget: {budget}")
    print("Expenses:")
    for expense in expenses:
        print(f"- {expense['description']}: {expense['amount']}")
    print(f"Total Spent: {get_total_expenses()}")
    print(f"Remaining Budget: {get_balance()}")

# Main function
def main():
    setup_database()
    print("Welcome to the Budget App")

    if get_initial_budget() == 0:
        initial_budget = float(input("Please enter your initial budget: "))
        set_initial_budget(initial_budget)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Add an expense")
        print("2. Show budget details")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            description = input("Enter expense description: ")
            amount = float(input("Enter expense amount: "))
            add_expense(description, amount)
        elif choice == "2":
            show_budget_details()
        elif choice == "3":
            print("Exiting Budget App. Goodbye!")
            break
        else:
            print("Invalid choice, please choose again.")

if __name__ == "__main__":
    main()
