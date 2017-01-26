
##########################
import random
from random import randint
###########################


class Employees(object):
    def nothing(self):
        return print("Placeholder")
    # def __init__(self, fixed_wage=200):
    #     self.total_wage = fixed_wage


class Croupier(Employees):
    def __init__(self, fixed_wage=200, commission=0):
        self.total_wage = fixed_wage
        self.commission = commission

        # def total_wage(self, fixed_wage=200, profit=0):
        #     self.total_wage = fixed_wage
        #     self.total_wage += profit * 0.005
        #     return self.total_wage

###########################


class Barman(Employees):
    def __init__(self, fixed_wage=200, sales=0, tips=0):
        self.total_wage = fixed_wage
        self.sales = sales
        self.tips = tips

    def adjusted_wage(self, tips):
        self.total_wage += tips

    # def drinks_served(self, drinks):
    #     self.drinks += drinks
    #
    # def tips_received(self, tips):
    #     self.tips += tips

#############################
#############################
#############################


class Customers(object):
    def __init__(self, bet=None, current_budget=0, drinks=0, tips=0, gain=0, barman=Barman()):
        self.bet = bet
        self.gain = gain
        self.current_budget = current_budget
        self.drinks = drinks
        self.tips = tips
        self.barman = barman

    # def current_budget(self, bet, gain):
    #     self.current_budget -= bet
    #     self.current_budget += gain

    def give_tip(self):
        if self.current_budget >= 20:
            tip = randint(0, 20)
            self.barman.tips += tip  # Barman receives the tip
            self.tips += tip
            self.current_budget -= tip

    def buy_drinks(self):
        if self.current_budget >= 60:
            drink_value = random.choice([20, 40])  # They buy either 1 or 2 drinks
            self.drinks += drink_value
            self.barman.sales += drink_value
            self.current_budget -= drink_value
            self.give_tip()
            return drink_value
        else:
            self.drinks += 0
            return 0

###########################


class Returning(Customers):
    def initial_budget(self):
        self.current_budget = randint(100, 300)

    def place_bet(self, min_bet):
        if self.current_budget >= min_bet:
            self.bet = min_bet
            self.current_budget -= min_bet
        else:
            self.bet = 0

############################


class OneTime (Customers):
    def initial_budget(self):
        self.current_budget = randint(200, 300)

    def place_bet(self, min_bet):
        betting = randint(0, round(self.current_budget/3))
        self.bet = betting
        self.current_budget -= betting

    ############################


class Bachelor(Customers):
    def initial_budget(self):
        self.current_budget = randint(200, 500)

    def total_budget(self, promotion):
        self.current_budget += promotion

    def place_bet(self, min_bet):
        betting = randint(0, round(self.current_budget))
        self.bet = betting
        self.current_budget -= betting
