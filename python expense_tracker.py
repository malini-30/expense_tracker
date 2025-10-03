import csv
import os
from datetime import datetime
from pathlib import Path
from tabulate import tabulate

# ---- basic settings (I can tweak these whenever I feel like it) ----
DATA_FILE = "my_expenses.csv"
BACKUP_FOLDER = Path("safety_copies")
MY_BUDGET = 2000  # bi-weekly budget in dollars
CURRENCY = "USD"

# My categories (don’t judge the pizza one)
CATEGORIES = [
    "🍕 Food & Dining",
    "🚗 Transport",
    "🎮 Fun & Games",
    "📄 Bills & Utilities",
    "🛒 Shopping",
    "🤷 Miscellaneous"
]

# Spending goals (kinda rough estimates, but works)
CATEGORY_LIMITS = {
    "🍕 Food & Dining": 400,
    "🚗 Transport": 200,
    "🎮 Fun & Games": 100,
    "📄 Bills & Utilities": 500,
    "🛒 Shopping": 300,
    "🤷 Miscellaneous": 200
}

# make sure we have a file to write into
def setup_files():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "Description", "Amount"])
        print("Created new expense file!")

    if not BACKUP_FOLDER.exists():
        BACKUP_FOLDER.mkdir()
        print("Backup folder ready.")

# quick backup just in case I mess up
def make_backup():
    if not os.path.exists(DATA_FILE):
        print("Nothing to backup yet.")
        return
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_{stamp}.csv"
    with open(DATA_FILE, "r", encoding="utf-8") as src:
        with open(BACKUP_FOLDER / filename, "w", encoding="utf-8") as dst:
            dst.write(src.read())
    print(f"Backup saved as {filename}")

# user money input (forces valid number)
def ask_money(msg="Amount $: "):
    while True:
        val = input(msg).strip().replace("$", "")
        try:
            amt = float(val)
            if amt > 0:
                return amt
            else:
                print("No negatives or zeros please 🙃")
        except ValueError:
            print("That’s not a number, try again!")

# add expense
def add_expense():
    today = datetime.now().strftime("%Y-%m-%d")
    date = input(f"Date (YYYY-MM-DD) [default {today}]: ").strip() or today
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except:
        print("Format wrong, using today’s date.")
        date = today

    print("\nPick a category:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"{i}. {c}")

    cat = None
    while not cat:
        try:
            choice = int(input("Category #: "))
            if 1 <= choice <= len(CATEGORIES):
                cat = CATEGORIES[choice - 1]
            else:
                print("Number out of range.")
        except:
            print("Enter a number please.")

    desc = input("What for? ").strip() or "No description"
    amt = ask_money()

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date, cat, desc, amt])

    print(f"Added: {cat} - {desc} - ${amt:.2f}")
    if cat in ["🍕 Food & Dining", "🛒 Shopping"]:
        print("⚠ Careful, this is one of your overspending zones!")

# view all or filtered
def view_expenses():
    if not os.path.exists(DATA_FILE):
        print("No data yet.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))

    if not reader:
        print("No expenses recorded.")
        return

    print("\nView options:")
    print("1. All")
    print("2. By category")
    print("3. By month-year")
    print("4. Category stats")
    choice = input("Choice: ").strip()

    expenses = reader
    if choice == "2":
        for i, c in enumerate(CATEGORIES, 1):
            print(f"{i}. {c}")
        try:
            sel = int(input("Which? "))
            if 1 <= sel <= len(CATEGORIES):
                cat = CATEGORIES[sel - 1]
                expenses = [e for e in reader if e["Category"] == cat]
        except:
            pass
    elif choice == "3":
        period = input("Enter MM-YYYY: ").strip()
        try:
            month, year = period.split("-")
            expenses = [e for e in reader if e["Date"].split("-")[1] == month.zfill(2) and e["Date"].split("-")[0] == year]
        except:
            print("Bad format, showing all.")

    elif choice == "4":
        show_stats(reader)
        return

    if not expenses:
        print("Nothing found.")
        return

    rows = [[e["Date"], e["Category"], e["Description"], f"${float(e['Amount']):.2f}"] for e in expenses]
    print(tabulate(rows, headers=["Date", "Category", "Description", "Amount"], tablefmt="grid"))

# stats
def show_stats(data):
    totals = {}
    grand = 0
    for e in data:
        amt = float(e["Amount"])
        c = e["Category"]
        totals[c] = totals.get(c, 0) + amt
        grand += amt

    rows = []
    for c, total in totals.items():
        percent = (total / grand * 100) if grand else 0
        avg = total / sum(1 for e in data if e["Category"] == c)
        rows.append([c, f"${total:.2f}", f"${avg:.2f}", f"{percent:.1f}%"])

    print("\nCategory Breakdown")
    print(tabulate(rows, headers=["Category", "Total", "Avg/Entry", "% of Total"], tablefmt="grid"))
    print(f"Overall total = ${grand:.2f}")

# monthly report
def monthly_report():
    if not os.path.exists(DATA_FILE):
        print("No data yet.")
        return
    monthyear = input("Enter month-year (MM-YYYY): ").strip()
    try:
        datetime.strptime(monthyear, "%m-%Y")
    except:
        print("Bad format.")
        return
    m, y = monthyear.split("-")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = [e for e in csv.DictReader(f) if e["Date"].split("-")[1] == m.zfill(2) and e["Date"].split("-")[0] == y]

    if not data:
        print("Nothing in that period.")
        return

    totals = {}
    total_all = 0
    for e in data:
        amt = float(e["Amount"])
        totals[e["Category"]] = totals.get(e["Category"], 0) + amt
        total_all += amt

    rows = []
    for c, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        goal = CATEGORY_LIMITS.get(c, 150)
        ok = "✅" if total <= goal else "❌"
        rows.append([c, f"${total:.2f}", f"{(total/total_all)*100:.1f}%", f"${goal}", ok])

    print("\nMonthly Report", monthyear)
    print(tabulate(rows, headers=["Category", "Spent", "%", "Goal", "OK?"], tablefmt="grid"))
    print(f"Total spent = ${total_all:.2f}")

# just quick add food shortcut
def quick_food():
    desc = input("Food details: ") or "Food"
    amt = ask_money()
    today = datetime.now().strftime("%Y-%m-%d")
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([today, "🍕 Food & Dining", desc, amt])
    print("Added quick food expense.")

# exit
def quit_program():
    make_backup()
    print("Bye 👋 (your data is safe)")
    return True

# menu loop
def menu():
    while True:
        print("\n==== Expense Tracker ====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Monthly Report")
        print("4. Quick Food Entry")
        print("5. Backup Now")
        print("6. Quit")
        choice = input("Choice: ").strip()
        if choice == "1": add_expense()
        elif choice == "2": view_expenses()
        elif choice == "3": monthly_report()
        elif choice == "4": quick_food()
        elif choice == "5": make_backup()
        elif choice == "6":
            if quit_program(): break
        else:
            print("Not an option.")

if __name__ == "__main__":
    setup_files()
    menu()
