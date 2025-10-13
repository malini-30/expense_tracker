# 💰 Personal Expense Tracker (Python Console)

A simple Python console application to record daily expenses, categorize
them, and generate monthly spending summaries --- stored in a CSV file
for persistence.

------------------------------------------------------------------------

## 🚀 Features

-   **Add Expenses**: Date, category, description, and amount\
-   **View Expenses**: All, by category, or by month/year (tabular
    format with `tabulate`)\
-   **Summary Report**: Monthly totals, category breakdowns, highest &
    lowest spending\
-   **Data Storage**: Persistent `.csv` file + automatic backups\
-   **Utilities**:
    -   Quick Food Entry 🍕
    -   Export tax-related expenses 📊
    -   Money-saving tips 💡
    -   Backup before exit 💾

------------------------------------------------------------------------

## 🛠 Tech Stack

-   **Python Standard Library**: `csv`, `datetime`, `os`\
-   **Optional**: [`tabulate`](https://pypi.org/project/tabulate/) for
    pretty terminal tables

------------------------------------------------------------------------

## 📂 File Structure

    expense_tracker.py   # Main script
    expenses.csv         # Auto-generated data file
    backups/             # Auto-generated backups

------------------------------------------------------------------------

## ▶️ Usage

1.  Install optional dependency:

    ``` bash
    pip install tabulate
    ```

2.  Run the program:

    ``` bash
    python python expense_tracker.py
    ```

3.  Use the menu to add, view, and report expenses.

------------------------------------------------------------------------

## 📊 Sample Output

**Main Menu**

    ==================================================
            💰 My Personal Expense Tracker 💰
    ==================================================
    1. Add New Expense
    2. View Expenses
    3. Generate Monthly Report
    4. 🍕 Quick Food Entry
    5. 📊 Export Tax Expenses
    6. 💡 My Spending Tips
    7. 💾 Create Backup
    8. Exit

**Monthly Report Example**

    📊 Monthly Report for 08-2023
    +---------------------+---------+-------------+--------------+--------+
    | Category            | Amount  | Percentage  | Budget Goal  | Status |
    +---------------------+---------+-------------+--------------+--------+
    | 🍕 Food & Dining    | $450.00 | 45.0%       | $400         | ❌     |
    | 📄 Bills & Utilities| $300.00 | 30.0%       | $500         | ✅     |
    | 🛒 Shopping         | $200.00 | 20.0%       | $300         | ✅     |
    | 🚗 Transport        | $50.00  | 5.0%        | $200         | ✅     |
    +---------------------+---------+-------------+--------------+--------+

    💵 Total Spending: $1000.00
    📈 Highest Spending: 🍕 Food & Dining ($450.00)
    📉 Lowest Spending: 🚗 Transport ($50.00)

------------------------------------------------------------------------

## 📌 Notes

-   Data is stored locally in `expenses.csv`.\
-   Backups are auto-saved in the `backups/` directory on exit.\
-   Supports custom categories and budget goals.

------------------------------------------------------------------------

## 📜 License

MIT License © 2025
------------------------------------------------------------------------
## 📩 Contact

- 👨‍💻 *Developer:* V Devi Malini
- 📧 *Email:* 23jr1a4494@gmail.com
- 🌐 *GitHub:*
https://github.com/malini-30

