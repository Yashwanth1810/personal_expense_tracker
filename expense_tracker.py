from expense import Expense
import calendar
import datetime


def main():
    print(f"Running the expense tracker🎯")
    expense_file_path='expenses.csv'

    try:
        budget=float(input("Enter the budget for this month in ₹: "))
    except ValueError:
        print("Enter the valid amount. Budget set to ₹2000")
        budget=2000

    # get user input for expense.
    expense=get_user_expense()
    #print(expense)


    # Write their expense to a file
    save_expense_to_file(expense, expense_file_path)
    #print("saving user expense:")

    # Read the file and summarize the expenses.
    summarize_expenses(expense_file_path, budget)

def get_user_expense():
    #print(f"🎯Getting user expense")
    #expense=get_user_expense()
    expense_name=input("Enter expense name: ")
    expense_amount=float(input("Enter expense amount: "))
    print(f'You\'ve enetered {expense_name}, {expense_amount}')
  
    expense_categories=["🍔 Food", "🏡 Home", "💼 Work", "🎉 Fun", "✨ Miscellaneous"]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f'  {i+1}.  {category_name}')

        value_range=f"[1 - {len(expense_categories)}]: "
        try:
            selected_index=int(input(f"Enter a category number {value_range}")) - 1
        except ValueError:
            print("Please enter a valid number!")
            continue

        if selected_index in range(len(expense_categories)):
            selected_category=expense_categories[selected_index]
            new_expense=Expense(name=expense_name,category= selected_category,amount=expense_amount)
            return new_expense
           
        else:
            print("Invalid input. Please Try again!")

    
    

def save_expense_to_file(expense:Expense, expense_file_path):
    print(f"🎯Saving user expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name}, {expense.amount}, {expense.category}\n")

def summarize_expenses(expense_file_path, budget):
    print(f"🎯Summarizing user expense")
    expenses: list[Expense]=[]
    with open(expense_file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category=line.strip().split(',')
            line_expense=Expense(
                name=expense_name, amount=float(expense_amount), category=expense_category
            )
            #print(line_expense)
            expenses.append(line_expense)
    
    amount_by_category={}
    for expense in expenses:
        key=expense.category
        if key in amount_by_category:
            amount_by_category[key]+= expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses by Category📈")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ₹{amount:.2f}")

    total_spent=sum([x.amount for x in expenses])
    print(f"📊 You\'ve spent ₹{total_spent:.2f} this month!")

    remaining_budget=budget-total_spent
    print(f"✅ Reamaining budget for this month: ₹{remaining_budget:.2f}")

    now=datetime.datetime.now()

    days_in_month=calendar.monthrange(now.year, now.month)[1]
    remaining_days=days_in_month-now.day
    print("Remaining days in the current month:", remaining_days)
    try:
        daily_budget=remaining_budget/remaining_days
        print(green(f"👉 Budget Per Day: ₹{daily_budget:.2f}"))
    except ZeroDivisionError:
        print(green(f"This is the last day of the month and the budget for today is: ₹{remaining_budget:.2f}"))

def green(text):
    return f"\033[92m{text}\033[0m"
    

if __name__ == "__main__":
    main()

