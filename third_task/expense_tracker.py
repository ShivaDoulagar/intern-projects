import json
from datetime import datetime


class ExpenseTracker:
    def __init__(self, data_file="expenses.json"):
        self.data_file = data_file
        self.expenses = self.load_data()

    def load_data(self):
        """Load expense data from file."""
        try:
            with open(self.data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def save_data(self):
        """Save expense data to file."""
        with open(self.data_file, "w") as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, amount, category, description=""):
        """Add a new expense entry."""
        try:
            amount = float(amount)
            date = datetime.now().strftime("%Y-%m-%d")
            if date not in self.expenses:
                self.expenses[date] = []
            self.expenses[date].append({
                "amount": amount,
                "category": category,
                "description": description
            })
            self.save_data()
            print("Expense added successfully!")
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")

    def view_summary(self, month=None):
        """View summary of expenses by category and month."""
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        summary = {}
        for date, records in self.expenses.items():
            record_month = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m")
            if month and record_month != month:
                continue
            for record in records:
                category = record["category"]
                summary[category] = summary.get(category, 0) + record["amount"]

        if summary:
            print(f"\nExpense Summary ({month if month else 'All Time'}):")
            for category, total in summary.items():
                print(f"{category}: ${total:.2f}")
        else:
            print("No expenses found for the given month.")

    def list_expenses(self):
        """List all recorded expenses."""
        if not self.expenses:
            print("No expenses recorded yet.")
            return
        print("\nAll Expenses:")
        for date, records in self.expenses.items():
            print(f"Date: {date}")
            for record in records:
                print(f"  - {record['category']}: ${record['amount']} ({record['description']})")

    def run(self):
        """Run the Expense Tracker."""
        while True:
            print("\nExpense Tracker Menu")
            print("1. Add Expense")
            print("2. View Monthly Summary")
            print("3. List All Expenses")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                amount = input("Enter amount: ")
                category = input("Enter category: ")
                description = input("Enter description (optional): ")
                self.add_expense(amount, category, description)
            elif choice == "2":
                month = input("Enter month (YYYY-MM) or press Enter for all-time summary: ")
                self.view_summary(month)
            elif choice == "3":
                self.list_expenses()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
