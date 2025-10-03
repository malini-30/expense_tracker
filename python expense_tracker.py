import csv
from datetime import datetime
from os import path
from tabulate import tabulate
import os
from pathlib import Path

# Constants here..
EXPENSE_FILE = "expenses.csv"
BACKUP_DIR = Path(__file__).parent / "backups" 

#  FIXME:My personalized spending categories with emojis - these match my actual spending habits mentioned here..
CATEGORIES = {
    "FOOD": "🍕 Food & Dining",
    "TRANSP": "🚗 Transport", 
    "FUN": "🎮 Fun & Games",
    "BILLS": "📄 Bills & Utilities",
    "SHOP": "🛒 Shopping",
    "MISC": "🤷 Other Stuff"
}

#TODO:Personal configuration section - settings that work for ME
class PersonalConfig:
    # I get paid bi-weekly, so my budget is based on that
    DEFAULT_BUDGET = 2000
    CURRENCY = "USD"
    
    # FIXME:These are my problem categories where I tend to overspend it 
    WATCHLIST_CATEGORIES = ["🍕 Food & Dining", "🛒 Shopping"]
    
    # TODO:My preferred date format here
    DATE_FORMAT = "%Y-%m-%d"  # Tried others but this works best for sorting techinic
    
    @staticmethod
    def get_category_goal(category):
        """My personal spending goals by category"""
        goals = {
            "🍕 Food & Dining": 400,
            "🚗 Transport": 200,
            "🎮 Fun & Games": 100,
            "📄 Bills & Utilities": 500,
            "🛒 Shopping": 300,
            "🤷 Other Stuff": 200
        }
        return goals.get(category, 150)  # Default for any new categories section.

def init_file():
    """Create the CSV file with headers if it doesn't exist"""
    # FIXME:Also create backups directory while we're at it
    if not path.exists(BACKUP_DIR):
        BACKUP_DIR.mkdir(parents=True,exist_ok=True)
        print(f"Created {BACKUP_DIR} directory for backups")
    
    if not path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount"])
        print("Created new expense file! Ready to start tracking. 💪")

def get_money_input(prompt):
    """My own function to get money amount. Keeps asking until it gets a valid positive number."""
    #  TODO:Tried using regex at first but it was overkill for this simple case
    # TODO:This approach handles most common cases without being too complex
    while True:
        money_str = input(prompt).strip().lstrip('$') # Handles if user types '$'
        
        #  TODO:HERE Originally had issues with negative numbers, added this check
        if money_str.startswith('-'):
            print("Nice try! Expenses can't be negative though. 😉")
            continue
            
        try:
            money_val = float(money_str)
            if money_val > 0:
                return money_val
            else:
                print("C'mon, amount has to be positive!")
        except ValueError:
            # TODO:Found that empty strings were causing troubles, added this specific check
            if not money_str:
                print("You didn't enter anything! Try again.")
            else:
                print(f"'{money_str}' doesn't look like a money amount. Please try again.")

def create_backup():
    """After losing my expense data last month, I never skip backups anymore"""
    if not os.path.exists(EXPENSE_FILE):
        print("No expense file found to backup")
        return
    
    # Create backup filename with date and time
    current_time = datetime.now()
    time_string = current_time.strftime("%Y%m%d_%H%M%S")
    backup_filename = f"expenses_backup_{time_string}.csv"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    # Just copy the file contents straight across
    original_file = open(EXPENSE_FILE, 'r', encoding='utf-8')
    backup_file = open(backup_path, 'w', encoding='utf-8')
    
    backup_file.write(original_file.read())
    
    original_file.close()
    backup_file.close()
    
    print(f"Backup saved: {backup_path}")
    
    #  TODO: Simple file copy - could use shutil but this works fine
    with open(EXPENSE_FILE, 'r', encoding='utf-8') as source:
        with open(backup_file, 'w', encoding='utf-8') as target:
            target.write(source.read())
    
    print(f"✓ Backup created: {backup_file}")

def add_the_expense():
    """Add a new expense to the tracker"""
    print("\n--- Add New Expense ---")
    
    # TODO:Get expense details 
    today = datetime.now().strftime('%Y-%m-%d')
    date_input = input(f'Date (YYYY-MM-DD) [Today: {today}]: ') or today
    
    #TODO:Validate date format - I kept entering wrong formats before
    try:
        datetime.strptime(date_input, '%Y-%m-%d')
    except ValueError:
        print("⚠️  Date format should be YYYY-MM-DD. Using today's date.")
        date_input = today
    
    print("\nWhere did you spend money?")
    category_list = list(CATEGORIES.values())
    for i, category in enumerate(category_list, 1):
        print(f"{i}. {category}")
    
    while True:
        try:
            cat_choice = input("Select category (number): ").strip()
            if not cat_choice:
                print("You need to pick a category!")
                continue
                
            cat_choice = int(cat_choice)
            if 1 <= cat_choice <= len(category_list):
                category = category_list[cat_choice - 1]
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
    
    description = input('Description (what was it for?): ').strip() or "No description"
    
    # TODO:below Use our custom money input function MENTIONED
    amount = get_money_input("Amount: $")
    
    # Save to CSV here 
    with open(EXPENSE_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([date_input, category, description, amount])
    
    print("\n✓ Expense added successfully!")
    
    # TODO:Checking if this is a category I'm watching   ..
    if category in PersonalConfig.WATCHLIST_CATEGORIES:
        print(f"💡 Remember: You're trying to spend less on {category}!")

def detect_overspending(category_totals, monthly_budget=1000):
    """I always blow my budget on eating out - this keeps me honest"""
    food_total = category_totals.get("🍕 Food & Dining", 0)
    
    # Figure out what percentage of my budget I've already burned through
    spent_so_far = (food_total / monthly_budget) * 100
    
    if spent_so_far > 80:
        print(f"🚨 HEADS UP: You've dropped ${food_total:.2f} on food already!")
        print(f"   That's {spent_so_far:.1f}% of your ${monthly_budget} monthly limit!")
        
        if spent_so_far > 100:
            print("   💀 Yikes - you're over budget!")
        
        return True
    
    return False
    if budget_percentage > 80:
        print(f"🚨 WARNING: You've spent ${food_spending:.2f} on food!")
        print(f"   That's {budget_percentage:.1f}% of your ${monthly_budget} budget!")
        if budget_percentage > 100:
            print("   💀 You've exceeded your budget!")
        return True
    return False

def calc_category_stats(expenses):
    """Calculate statistics for categories - evolved this function a few times"""
    # Version 1: Simple totals MENTION
    # Version 2: Added averages and counts here ..
    # Version 3: Added percentage calculations below..
    
    category_data = {}
    total_all = 0
    
    for expense in expenses:
        category = expense['Category']
        amount = float(expense['Amount'])
        total_all += amount
        
        if category not in category_data:
            #TODO:  below Initializing with all the stats I might want here..
            category_data[category] = {
                'total': 0,
                'count': 0,
                'average': 0,
                'transactions': []
            }
        
        category_data[category]['total'] += amount
        category_data[category]['count'] += 1
        category_data[category]['transactions'].append(amount)
    
    # TODO: Below Calculate averages and percentages in a separate loop (not most efficient but clearer explain)
    for category in category_data:
        data = category_data[category]
        data['average'] = data['total'] / data['count'] if data['count'] > 0 else 0
        data['percentage'] = (data['total'] / total_all) * 100 if total_all > 0 else 0
    
    return category_data, total_all

def view_expenses():
    """View all expenses with filtering options"""
    try:
        # FIXME:Was having the encoding issues on the  Windows, AND also added utf-8 explicitly
        with open(EXPENSE_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
    except FileNotFoundError:
        print("No expenses recorded yet. Start by adding one!")
        return
    
    # the Old way: if len(expenses) == 0
    # TODO:New way: more pythonic according to StackOverflow here 
    if not expenses:
        print("No expenses recorded yet. Start by adding one!")
        return
    
    # TODO:Previous menu was about to getting crowded, simplified options here..
    print("\n--- View Expenses ---")
    print("1. View all expenses")
    print("2. Filter by category") 
    print("3. Filter by month/year")
    print("4. Show category statistics")
    
    choice = input("What do you want to see? (1-4): ")
    
    filtered_expenses = expenses
    category_list = list(CATEGORIES.values())
    
    if choice == '2':
        print("\nCategories:")
        for i, category in enumerate(category_list, 1):
            print(f"{i}. {category}")
        
        cat_choice = input("Select category (number) or press Enter for all: ")
        if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(category_list):
            selected_category = category_list[int(cat_choice) - 1]
            
            # TODO:Tried using filter() and lambda but  herefound this more readable format below
            #  TODO:here filtered_expenses = list(filter(lambda x: x['Category'] == selected_category, expenses))
            filtered_expenses = []
            for exp in expenses:
                if exp['Category'] == selected_category:
                    filtered_expenses.append(exp)
    
    elif choice == '3':
        month_year = input("Enter month and year (MM-YYYY) or press Enter for all: ")
        if month_year:
            try:
                month, year = month_year.split('-')
                filtered_expenses = [
                    e for e in expenses 
                    if e['Date'].split('-')[1] == month.zfill(2) 
                    and e['Date'].split('-')[0] == year
                ]
            except:
                print("Invalid format. Use MM-YYYY (e.g., 08-2023)")
                return
    
    elif choice == '4':
        #  FIXME:below Shown my enhanced statistics mention..
        category_stats, total = calc_category_stats(expenses)
        
        print(f"\n📈 Spending Statistics (All Time)")
        print("=" * 50)
        
        stats_data = []
        for category, stats in category_stats.items():
            stats_data.append([
                category,
                f"${stats['total']:.2f}",
                stats['count'],
                f"${stats['average']:.2f}",
                f"{stats['percentage']:.1f}%"
            ])
        
        headers = ["Category", "Total", "Transactions", "Avg/Transaction", "Percentage"]
        print(tabulate(stats_data, headers=headers, tablefmt="simple"))
        print(f"\nOverall Total: ${total:.2f}")
        return
    
    if not filtered_expenses:
        print("No expenses match your criteria.")
        return
    
    # TODO:Convert amounts to float for proper sorting here 
    for expense in filtered_expenses:
        expense['Amount'] = float(expense['Amount'])
    
    # TODO: Figure out a better way  later to sort 
    filtered_expenses.sort(key=lambda x: datetime.strptime(x['Date'], '%Y-%m-%d'), reverse=True)
    
    #  TODO:Prepare data for tabulate below
    table_data = []
    total = 0
    for expense in filtered_expenses:
        table_data.append([
            expense['Date'],
            expense['Category'],
            expense['Description'],
            f"${expense['Amount']:.2f}"
        ])
        total += expense['Amount']
    
    headers = ["Date", "Category", "Description", "Amount"]
    # NOTE:  below  we Found this tabulate library on StackOverflow, works great!
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"\n💰 Total: ${total:.2f}")

def generating_the_report():
    """Generate monthly spending summary"""
    try:
        with open(EXPENSE_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            expenses = list(reader)
    except FileNotFoundError:
        print("No expenses recorded yet. Start by adding one!")
        return
    
    if not expenses:
        print("No expenses recorded yet. Start by adding one!")
        return
    
    print("\n--- Monthly Spending Report ---")
    
    # Get month/year input from the user below 
    while True:
        month_year = input("Enter month and year (MM-YYYY): ")
        try:
            month, year = month_year.split('-')
            datetime.strptime(month_year, '%m-%Y')  # Validate format here
            break
        except:
            print("Invalid format. Use MM-YYYY (e.g., 08-2023)")
    
    # below Filter  shows expenses for the selected month/year
    monthly_expenses = [
        e for e in expenses 
        if e['Date'].split('-')[1] == month.zfill(2) 
        and e['Date'].split('-')[0] == year
    ]
    
    if not monthly_expenses:
        print(f"No expenses recorded for {month_year}.")
        return
    
    # Calculate totals and category breakdown..
    cat_totals = {}  # Using slightly less descriptive name here 
    total = 0
    
    for expense in monthly_expenses:
        amount = float(expense['Amount'])
        category = expense['Category']
        total += amount
        cat_totals[category] = cat_totals.get(category, 0) + amount
    
    # TODO:Sort the categories by spending (highest first)
    sorted_categories = sorted(cat_totals.items(), key=lambda x: x[1], reverse=True)
    
    #   TODO: Prepare report data
    report_data = []
    for category, amount in sorted_categories:
        percentage = (amount / total) * 100
        budget_goal = PersonalConfig.get_category_goal(category)
        status = "✅" if amount <= budget_goal else "❌"
        
        report_data.append([
            category,
            f"${amount:.2f}",
            f"{percentage:.1f}%",
            f"${budget_goal}",
            status
        ])
    
    #   TODO:Below Print report
    print(f"\n📊 Monthly Report for {month_year}")
    print(tabulate(report_data, headers=["Category", "Amount", "Percentage", "Budget Goal", "Status"], tablefmt="grid"))
    print(f"\n💵 Total Spending: ${total:.2f}")
    print(f"📈 Highest Spending: {sorted_categories[0][0]} (${sorted_categories[0][1]:.2f})")
    if len(sorted_categories) > 1:
        print(f"📉 Lowest Spending: {sorted_categories[-1][0]} (${sorted_categories[-1][1]:.2f})")
    
    #  FIXME:My personal overspending check here..
    overspent = detect_overspending(cat_totals)
    if overspent:
        print("\n💡 Tip: Try meal prepping to save on food costs!")

def quickly_add_food_expense():
    """I eat out a lot, so I made a shortcut for food expenses"""
    print("\n🍕 Quick Food Expense")
    description = input("What did you eat? ").strip() or "Food"
    amount = get_money_input("Amount: $")
    
    today = datetime.now().strftime('%Y-%m-%d')
    with open(EXPENSE_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([today, "🍕 Food & Dining", description, amount])
    
    print("✓ Quick food expense added!")
    
    #  TODO:MY Personal reminder since I  HAVE overspend on food
    if amount > 20:
        print("💡 That's a bit pricey! Maybe cook at home next time?")

def export_for_the_taxes():
    """I need this for my tax deductions - business expenses"""
    try:
        with open(EXPENSE_FILE, 'r', encoding='utf-8') as file:
            expenses = list(csv.DictReader(file))
    except FileNotFoundError:
        print("No expenses to export!")
        return
    
    # FIXME:Filter for  the potential business expenses  ( specific categories)
    business_categories = ["🚗 Transport", "📄 Bills & Utilities"]
    business_expenses = [e for e in expenses if e['Category'] in business_categories]
    
    if business_expenses:
        tax_file = f"tax_expenses_{datetime.now().strftime('%Y%m%d')}.csv"
        with open(tax_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Description", "Amount", "Tax Purpose"])
            for expense in business_expenses:
                writer.writerow([expense['Date'], expense['Category'], 
                               expense['Description'], expense['Amount'], "Business"])
        print(f"✓ Tax expenses exported to {tax_file}")
        print("💡 Remember to keep receipts for tax time!")
    else:
        print("No business-related expenses found.")

def show_spending_tips():
    """Personal tips I've collected for saving money"""
    print("\n💡 My Personal Spending Tips")
    print("=" * 40)
    tips = [
        "🍕 Food: Meal prep on Sundays saves me $50+/week",
        "🚗 Transport: Carpool twice a week = $40/month savings", 
        "🛒 Shopping: 24-hour rule - wait a day before buying",
        "📄 Bills: Negotiated internet bill down by $15/month",
        "🎮 Fun: Library free events instead of expensive outings",
        "💡 General: Use cash for discretionary spending"
    ]
    
    for tip in tips:
        print(f"• {tip}")

def exit_program():
    """Better safe than sorry - always backup before quitting"""
    create_backup()  # Can't afford to lose my expense data again
    
    print("\nThat's all for now! Catch you later! 👋")
    print("(Don't worry, I made a backup of your data)")
    
    return True

def main_menu():
    """Display the main menu - customized for my workflow"""
    print("\n" + "="*50)
    print("        💰 My Personal Expense Tracker 💰")
    print("="*50)
    print("   (Customized for my spending habits)")
    
    menu_actions = {
        '1': add_the_expense,
        '2': view_expenses,
        '3': generating_the_report,
        '4': quickly_add_food_expense,  # it is My personal shortcut
        '5': export_for_the_taxes,        # it is My tax utility
        '6': show_spending_tips,      # it is My personal advice
        '7': create_backup,           #  it is My backup utility
        '8': exit_program
    }
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Add New Expense")
        print("2. View Expenses") 
        print("3. Generate Monthly Report")
        print("4. 🍕 Quick Food Entry (I use this a lot!)")
        print("5. 📊 Export Tax Expenses") 
        print("6. 💡 My Spending Tips")
        print("7. 💾 Create Backup")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        action = menu_actions.get(choice)
        if action:
            should_exit = action()
            if should_exit:
                break
        else:
            print("Hmm, that option doesn't exist. Try 1-8.")

if __name__ == "__main__":
    # My personal startup routine mentioned...
    init_file()
    
    # TODO: Checking if we  restore from backup (feature I'm thinking about)
    if not path.exists(EXPENSE_FILE) and path.exists(BACKUP_DIR):
        print("💡 Note: Found backup directory. Restore feature coming soon!")
    
    main_menu()