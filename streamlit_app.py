import streamlit as st
import calendar
import datetime
import os

# Define Expense class
class Expense:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ₹{self.amount:.2f}>"

# Save expense to file
def save_expense_to_file(expense, file_path):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

# Summarize expenses from file
def summarize_expenses(file_path, budget):
    expenses = []

    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            name, amount, category = line.strip().split(",")
            expenses.append(Expense(name, category, float(amount)))

    # Category-wise total
    category_totals = {}
    for exp in expenses:
        category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount

    st.subheader("📊 Expenses by Category")
    for category, total in category_totals.items():
        st.write(f"**{category}**: ₹{total:.2f}")

    total_spent = sum(exp.amount for exp in expenses)
    st.success(f"💸 Total Spent: ₹{total_spent:.2f}")
    remaining = budget - total_spent
    st.info(f"✅ Remaining Budget: ₹{remaining:.2f}")

    today = datetime.datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_remaining = days_in_month - today.day
    st.info(f"📅 Remaining days in the month: **{days_remaining}**")

    if days_remaining > 0:
        daily_budget = remaining / days_remaining
        st.info(f"📅 Budget per Day: ₹{daily_budget:.2f}")
    else:
        st.warning(f"📅 Last day of the month. Today's budget: ₹{remaining:.2f}")

# Main Streamlit App
def main():
    st.title("💰 Expense Tracker")
    file_path = "expenses.csv"

    budget = st.number_input("Enter your monthly budget (₹)", min_value=0.0, value=2000.0, step=100.0)

    st.header("➕ Add a New Expense")
    name = st.text_input("Expense Name")
    amount = st.number_input("Expense Amount (₹)", min_value=0.0, step=10.0)
    category = st.selectbox("Category", ["🍔 Food", "🏡 Home", "💼 Work", "🎉 Fun", "✨ Miscellaneous"])

    if st.button("Save Expense"):
        if name and amount > 0:
            expense = Expense(name, category, amount)
            save_expense_to_file(expense, file_path)
            st.success(f"✅ Saved: {expense}")
        else:
            st.error("❌ Please enter a valid name and amount!")

    st.header("📈 Monthly Summary")
    summarize_expenses(file_path, budget)

if __name__ == "__main__":
    main()
