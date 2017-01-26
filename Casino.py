"""Defines class Casino, and all methods needed to simulate an evening.
The simulate_evening() method, applied to an object of class Casino with default values for its attributes should be
    enough for a single complete simulation.
"""
import Tables
import People
import random


class Casino(object):
    """Class for the casino, joining all the others and running the simulations."""
    def __init__(self, r_tables=None, c_tables=None, croupiers=None, barmen=None, customers=None, cash=50000,
                 promotion=200):
        self.r_tables = r_tables  # List of roulette tables
        self.c_tables = c_tables  # List of craps tables
        self.croupiers = croupiers
        self.barmen = barmen
        self.customers = customers
        self.cash = cash  # Starting cash of the casino
        self.promotion = promotion  # Promotion given to bachelors

    def buy_tables(self, n_roulette=10, n_craps=10):
        """Creates the tables and randomly sets their minimum bets"""
        self.r_tables = [Tables.Roulette(0, [], []) for _ in range(n_roulette)]
        [x.set_minimum() for x in self.r_tables]
        self.c_tables = [Tables.Craps(0, [], []) for _ in range(n_craps)]
        [x.set_minimum() for x in self.c_tables]

    def hire_employees(self, n_barmen=4):
        """Creates barmen and only as many croupiers as needed"""
        n_croupier = len(self.r_tables) + len(self.c_tables)
        self.croupiers = [People.Croupier(200) for _ in range(n_croupier)]
        self.barmen = [People.Barman(200) for _ in range(n_barmen)]

    def assign_croupiers(self):
        """Assign each croupier to a table, needs the same number of the croupiers and tables"""
        for x, y in zip(self.r_tables + self.c_tables, self.croupiers):
            x.croupier = y

    def open_doors(self, capacity=100, per_returning=.5, per_bachelors=.2):
        """Creates customers in approximately the right proportions and sets their initial budgets"""
        n_returning = round(capacity * per_returning)
        n_bachelors = round(capacity * per_bachelors)
        n_one_time = capacity - n_returning - n_bachelors
        returners = [People.Returning() for _ in range(n_returning)]
        one_timers = [People.OneTime() for _ in range(n_one_time)]
        bachelors = [People.Bachelor() for _ in range(n_bachelors)]
        c_list = list(returners + one_timers + bachelors)
        [x.set_initial_budget() for x in c_list]
        print("Customers bought " + str(sum([x.budget for x in c_list])) +
              " in chips.")
        for x in bachelors:
            x.budget += self.promotion
            self.cash -= self.promotion
        self.customers = c_list

    def get_a_drink(self):
        """Assign to every customer a barman randomly, and they buy drinks.
        All customers get a drink."""
        which_barmen = [random.randint(1, len(self.barmen)) for _ in self.customers]
        for x in range(len(self.customers)):
            self.customers[x].barman = self.barmen[which_barmen[x]-1]  # Customers find a barmen
        drinks = [x.buy_drinks() for x in self.customers]  # Customers buy one or two drinks
        self.cash += sum(drinks)  # Profit for the casino
        print("Sales of drinks ammounted to " + str(sum(drinks)))

    def fill_tables(self):
        """Assigns every customer to a table randomly"""
        which_table = [random.randint(1, len(self.c_tables + self.r_tables)) for _ in self.customers]
        for x in range(len(self.customers)-1):
            (self.c_tables + self.r_tables)[which_table[x]-1].customers.append(self.customers[x])

    def clear_tables(self):
        """Clears the customer list o every table"""
        for x in (self.r_tables + self.c_tables):
            x.customers = []

    def play_round(self, silent=False):
        """Plays a round on every table"""
        self.fill_tables()
        values_won = [x.simulate_round(silent=silent) for x in (self.r_tables + self.c_tables)]
        self.clear_tables()
        values_won = [item for sublist in values_won for item in sublist]  # Flattens the list of lists
        count = sum([1 for x in values_won if x])
        if count > 0:
            print(str(count) + " players won a total of " + str(sum(values_won)) + " in this round")
        else:
            print("No player won in this round")

    def simulate_evening(self, n_roulette=10, n_craps=10, n_barmen=4, capacity=100, per_returning=.5, per_bachelors=.2,
                         n_drinks=5, n_rounds=3, silent=True):
        """Simulates a complete evening at the casino, from the setup to the results."""
        # Setup
        initial_cash = self.cash
        self.buy_tables(n_roulette, n_craps)
        self.hire_employees(n_barmen)
        self.assign_croupiers()
        self.open_doors(capacity, per_returning, per_bachelors)
        # Play games and buy drinks a set amount of times
        while n_drinks > 0 or n_rounds > 0:
            if n_drinks > 0:
                self.get_a_drink()
                n_drinks -= 1
            if n_rounds > 0:
                self.play_round(silent=silent)
                n_rounds -= 1
        # Collect profits from the tables
        for x in (self.r_tables + self.c_tables):
            self.cash += x.profit
        # Analyze results
        print("Customers changed " + str(sum([x.budget for x in self.customers])) +
              " in chips for cash")
        print("Profit of " + str(self.cash - initial_cash) + " tonight")


print(Casino.__doc__)
monte_carlo = Casino()
monte_carlo.simulate_evening()

print(monte_carlo.customers[0].initial_budget)
print(monte_carlo.customers[99].initial_budget)
print(monte_carlo.customers[99].initial_upper_bound)
