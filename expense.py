"""def get_initial_budget():
    #budget=float(input("Enter your budget: "))
    while True:
        try:
            #budget=float(input("Enter your budget: "))
            if budget<0:
                print("Budget cannot be negative!")
                continue
            return budget
        except ValueError:
            print("Invalid input. Please enter a valid number.")

get_initial_budget()

if __name__=="__main__":
    total_budget=get_initial_budget()
    print(f"Your total budget is ₹{total_budget}")"""

class Expense:
    def __init__(self, name, category, amount) -> None:
        self.name=name
        self.category=category
        self.amount=amount

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, {self.amount:.2f}>"