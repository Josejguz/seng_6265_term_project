# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 18:23:29 2024

@author: apgra
"""

class Budget:
    def __init__(self, name):
        
        #Initializes name of budget

        self.name = name

        # Initialize empty lists for income and expenses
        
        self.incomes = []
        self.expenses = []

    def add_income(self, source, amount):
       
        # Adds income source and amount to the income list.
        if not source:
            raise ValueError("Income source must be provided.")
        if amount is None:
            raise ValueError("Amount cannot be empty.")
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number.")
        if amount > 0:
            self.incomes.append({'source': source, 'amount': amount})
            print(f"Income of {amount} from {source} added.")
        else:
            print("Income amount must be positive.")

    def add_expense(self, category, amount):
       
        # Adds an expense description and amount to the expenses list.
        if not category:
            raise ValueError("Expense category must be provided.")
        if amount is None:
            raise ValueError("Amount cannot be empty.")
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a number.")
        if amount > 0:
            self.expenses.append({'category': category, 'amount': amount})
            print(f"Expense of {amount} for {category} added.")
        else:
            print("Expense amount must be positive.")

    def remove_income(self, source, amount):
        for income in self.incomes:
            if income['source'] == source and income['amount'] == amount:
                self.incomes.remove(income)
                print(f"Income of {amount} from {source} removed.")
                return

    def remove_expense(self, category, amount):
        for expense in self.expenses:
            if expense['category'] == category and expense['amount'] == amount:
                self.expenses.remove(expense)
                print(f"Expense of {amount} for {category} removed.")

    def calculate_total_income(self):
        return sum([income['amount'] for income in self.incomes])
    
    def calculate_total_expenses(self):
        return sum([expense['amount'] for expense in self.expenses])

    def calculate_savings(self):
        
       # Calculates total savings by subtracting total expenses from total income.
               
        total_income = self.calculate_total_income()
        total_expenses = self.calculate_total_expenses()
        savings = total_income - total_expenses
        return savings
    
    def generate_report(self):

        # Generates a report with the budget name, total income, total expenses, savings, income list, and expenses list.
        report = {
            'budget_name': self.name,
            'total_income': self.calculate_total_income(),
            'total_expenses': self.calculate_total_expenses(),
            'savings': self.calculate_savings(),
            'incomes': self.incomes,
            'expenses': self.expenses
        }
        return report
    
    def save_budget(self, db, username):
        user_budget = db.budgets.find_one({"username": username})
        budget_data = {
            "name": self.name,
            "incomes": self.incomes,
            "expenses": self.expenses
        }
        if user_budget:
            db.budgets.update_one({"username": username}, {"$set": {self.name: budget_data}})
        else:
            db.budgets.insert_one({"username": username, self.name: budget_data})
        return True

    @staticmethod
    def load_budget(db, username, budget_name):
        user_budget = db.budgets.find_one({"username": username})
        if user_budget and budget_name in user_budget:
            budget_data = user_budget[budget_name]
            budget = Budget(budget_data['name'])
            budget.incomes = budget_data['incomes']
            budget.expenses = budget_data['expenses']
            return budget
        return None