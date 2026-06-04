import mysql.connector
from datetime import datetime
import getpass

# Ask for password (nothing shows while typing)
mysql_password = getpass.getpass("Enter MySQL password: ")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=mysql_password,
    database="expense_tracker"
)
cursor = db.cursor()

def add_expense():
    print("\n--- Add New Expense ---")
    
    try:
        amount = float(input("Amount (R): "))
        description = input("Description: ")
        expense_date = input("Date (DD-MM-YYYY) or press Enter for today: ")
        
        if not expense_date:
            expense_date = datetime.now().strftime("%d-%m-%Y")
        
        date_for_mysql = datetime.strptime(expense_date, "%d-%m-%Y").strftime("%Y-%m-%d")
        
        cursor.execute("SELECT id, name FROM categories ORDER BY id")
        rows = cursor.fetchall()
        print("\nCategories:")
        for row in rows:
            print(f"  {row[0]}. {row[1]}")
        
        cat_id = int(input("Select category number: "))
        
        query = "INSERT INTO expenses (amount, description, category_id, expense_date) VALUES (%s, %s, %s, %s)"
        values = (amount, description, cat_id, date_for_mysql)
        cursor.execute(query, values)
        db.commit()
        
        print(f"\n[SUCCESS] Expense added successfully! (ID: {cursor.lastrowid})")
        
    except ValueError:
        print("[ERROR] Invalid input.")
    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()

def view_expenses():
    print("\n--- All Expenses ---")
    
    query = """
    SELECT e.id, e.amount, e.description, c.name, e.expense_date
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    ORDER BY e.expense_date DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    if not rows:
        print("No expenses found.")
        return
    
    for row in rows:
        date_obj = datetime.strptime(str(row[4]), "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d-%m-%Y")
        print(f"ID: {row[0]} | Amount: R{row[1]} | Description: {row[2]} | Category: {row[3]} | Date: {formatted_date}")
    
    total = sum(row[1] for row in rows)
    print(f"\nTotal Expenses: R{total:.2f}")

def monthly_summary():
    print("\n--- Monthly Summary ---")
    
    date_str = input("Enter date (DD-MM-YYYY) to view summary for that month: ")
    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
    year = date_obj.strftime("%Y")
    month = date_obj.strftime("%m")
    
    query = """
    SELECT c.name, SUM(e.amount) as total
    FROM expenses e
    JOIN categories c ON e.category_id = c.id
    WHERE YEAR(e.expense_date) = %s AND MONTH(e.expense_date) = %s
    GROUP BY c.name
    ORDER BY total DESC
    """
    cursor.execute(query, (year, month))
    rows = cursor.fetchall()
    
    if not rows:
        print(f"No expenses for {date_str}.")
        return
    
    for row in rows:
        print(f"{row[0]}: R{row[1]}")
    
    grand_total = sum(row[1] for row in rows)
    print(f"\nTotal for {date_str}: R{grand_total:.2f}")

def delete_expense():
    print("\n--- Delete Expense ---")
    expense_id = input("Enter expense ID to delete: ")
    
    cursor.execute("SELECT id, description FROM expenses WHERE id = %s", (expense_id,))
    expense = cursor.fetchone()
    
    if not expense:
        print("[ERROR] Expense not found.")
        return
    
    print(f"Found: ID {expense[0]} - {expense[1]}")
    confirm = input(f"Delete this expense? (y/n): ").lower()
    
    if confirm == 'y':
        cursor.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
        db.commit()
        print("[SUCCESS] Expense deleted!")
    else:
        print("Cancelled.")

def main():
    while True:
        print("\n================================")
        print("      EXPENSE TRACKER")
        print("================================")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Monthly summary")
        print("4. Delete expense")
        print("5. Exit")
        
        choice = input("\nChoose an option (1-5): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            monthly_summary()
        elif choice == '4':
            delete_expense()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()