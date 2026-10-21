"""Analyze expenses from a CSV file using Python's standard library.
Run: python expense_csv_analyzer.py expenses.csv

CSV columns required: date,category,amount,description
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path


def analyze(path):
    totals = defaultdict(float)
    count = 0
    grand_total = 0.0

    with Path(path).open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        required = {"date", "category", "amount", "description"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError("CSV must contain: date, category, amount, description")

        for row in reader:
            try:
                amount = float(row["amount"])
            except (TypeError, ValueError):
                print(f'Skipping invalid amount in row: {row}')
                continue
            category = (row["category"] or "Uncategorized").strip()
            totals[category] += amount
            grand_total += amount
            count += 1

    print(f"Transactions analyzed: {count}")
    print(f"Total spending: {grand_total:.2f}")
    print("\\nSpending by category:")
    for category, total in sorted(totals.items(), key=lambda item: item[1], reverse=True):
        print(f"  {category}: {total:.2f}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python expense_csv_analyzer.py expenses.csv")
        raise SystemExit(1)
    try:
        analyze(sys.argv[1])
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
