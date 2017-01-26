"""Definitions for classes Employees and Customeres, their subclasses and methods"""
import random
from random import randint


# Employee classes
class Employee(object):
    def __init__(self, wage=200):
        self.tota_wage = wage


class Croupier(Employee):
    def __init__(self, wage=200, commission=0):
        super(Croupier, self).__init__(wage)
        self.commission = commission


class Barman(Employee):
    def __init__(self, wage=200, sales=0, tips=0):
        super(Barman, self).__init__(wage)
        self.sales = sales
        self.tips = tips


# Customer class
class Customer(object):
    initial_lower_bound = 0
    initial_upper_bound = 0

    def __init__(self, bet=None, budget=0, drinks=0, tips=0, gain=0, barman: Barman=None):
        self.bet = bet
        self.gain = gain  # Final profit
        self.budget = budget
        self.drinks = drinks  # Total expenditure on drinks
        self.tips = tips  # Total tips given
        self.barman = barman
        self.initial_budget = budget

    def set_initial_budget(self):
        """Randomly sets the initial budget according to subclasses' range.
        Does not account for Bachelor's promotion.
        """
        self.budget = randint(self.initial_lower_bound, self.initial_upper_bound)
        self.initial_budget = self.budget

    def give_tip(self):
        """Give tips to the assigned barman and deduce tips from the budget"""
        if self.budget >= 20:
            tip = randint(0, 20)
            self.barman.tips += tip  # Barman receives the tip
            self.tips += tip
            self.budget -= tip

    def buy_drinks(self):
        """Buys a drink or two if they have enough money, and tip the barman"""
        if self.budget >= 60:
            drink_value = random.choice([20, 40])  # They buy either 1 or 2 drinks
            self.drinks += drink_value
            self.barman.sales += drink_value
            self.budget -= drink_value
            self.give_tip()
            return drink_value
        else:
            self.drinks += 0
            return 0

    def realize_gains(self):
        """Takes the money home"""
        self.gain = self.budget - self.initial_budget


# Customer's subclasses:
class Returning(Customer):
    initial_lower_bound = 100
    initial_upper_bound = 300

    def place_bet(self, min_bet):
        """Places the bet according to subclasses' behavior"""
        if self.budget >= min_bet:
            self.bet = min_bet
            self.budget -= min_bet
        else:
            self.bet = 0


class OneTime (Customer):
    initial_lower_bound = 200
    initial_upper_bound = 300

    def place_bet(self, _):
        """Places the bet according to subclasses' behavior"""
        betting = randint(0, round(self.budget/3))
        self.bet = betting
        self.budget -= betting


class Bachelor(Customer):
    initial_lower_bound = 200
    initial_upper_bound = 500

    def place_bet(self, _):
        """Places the bet according to subclasses' behavior"""
        betting = randint(0, round(self.budget))
        self.bet = betting
        self.budget -= betting
