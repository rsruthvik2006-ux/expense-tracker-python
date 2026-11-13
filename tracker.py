"""
Personal Expense Tracker
An object-oriented CLI application for logging expenses, saving data to CSV,
and generating category summaries and report statistics.
"""

import csv
import os
from datetime import datetime


class Expense:
    """Represents an individual financial expense item."""

    def __init__(self, amount: float, category: str, description: str, date_str: str = None):
        self.amount = float(amount)
        self.category = category.strip().capitalize()
        self.description = description.strip()
        self.date = date_str if date_str else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        """Converts expense attributes to dictionary for CSV storage."""
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
        }


class ExpenseTracker:
    """Manages collection of expenses and handles file storage & reporting."""

    def __init__(self, filepath="expenses.csv"):
        self.filepath = filepath
        self.expenses = []
        self.load_from_csv()

    def add_expense(self, expense: Expense):
        """Adds an expense object and saves it to local storage."""
        self.expenses.append(expense)
        self._save_to_csv()

    def get_total_spent((self) -> float:
        """Calculates total spend across all logged expenses."""
        return sum(exp.amount for exp in self.expenses)

    def get_summary_by_category(self) -> dict:
        """Aggregates spending amounts organized by expense category."""
        summary = {}
        for exp in self.expenses:
            summary[exp.category] = summary.get(exp.category, 0.0) + exp.amount
        return summary

    def _save_to_csv(self):
        """Writes current list of expenses to a CSV file."""
        fieldnames = ["date", "category", "amount", "description"]
        with open(self.filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for exp in self.expenses:
                writer.writerow(exp.to_dict())

    def load_from_csv(self):
        """Loads expenses from CSV file if it exists."""
        if not os.path.exists(self.filepath):
            return

        with open(self.filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            self.expenses = [
                Expense(row["amount"], row["category"], row["description"], row["date"])
                for row in reader
            ]


def main():
    tracker = ExpenseTracker("sample_expenses.csv")

    # Adding sample data to simulate real usage
    sample_data = [
        Expense(4.50, "Food", "Morning Coffee"),
        Expense(14.20, "Food", "Lunch Combo"),
        Expense(55.00, "Transport", "Gas Station"),
        Expense(120.00, "Utilities", "Electricity Bill"),
        Expense(15.99, "Entertainment", "Streaming Subscription"),
    ]

    print("--- Personal Expense Tracker & Analytics ---")
    print("Logging sample expenses...")

    for exp in sample_data:
        tracker.add_expense(exp)

    # Output statistics and reports
    total = tracker.get_total_spent()
    by_category = tracker.get_summary_by_category()

    print("\n-------------------------------------------")
    print(f"Total Logged Spending: ${total:.2f}")
    print("-------------------------------------------")
    print("Breakdown by Category:")
    for category, amount in by_category.items():
        percentage = (amount / total) * 100 if total > 0 else 0
        print(f"  - {category:<15}: ${amount:>7.2f} ({percentage:>5.1f}%)")
    print("-------------------------------------------")
    print("Data saved successfully to 'sample_expenses.csv'.")


if __name__ == "__main__":
    main()
