import Tables
from random import randint
import random
from matplotlib import pyplot as plt

# This is used to fix the random number generator so we can test the output
random.seed(3456)

# Simulates the Roulette twice

amounts1 = [10, 85, 120, 65, 150, 122]
bets1 = [10, 24, 36, 0, 11, 24]
table1 = Tables.Roulette(100)
print(table1.simulate_game(amounts1, bets1))
print(table1.simulate_game(amounts1, bets1))

# Simulates the Craps twice

amounts2 = [10, 85, 120, 65, 150, 122]
bets2 = [10, 12, 6, 2, 11, 5]
table2 = Tables.Craps(100)
print(table2.simulate_game(amounts2, bets2))
print(table2.simulate_game(amounts2, bets2))

# Create n_sim = 1000 simulations of the craps game:

result_profit = []
result_value_won = []
dices = []
casino_share = []
n_sim = 1000
for i in range(n_sim):
    amounts3 = [randint(100, 500) for j in range(10)]
    bets3 = [randint(2, 12) for k in range(10)]
    result = table2.simulate_game(amounts3, bets3)
    result_value_won.append(result[0])
    result_profit.append(result[1])
    dices.append(table2.dices())
    casino_share.append(result[1]/sum(amounts3))

# Plotting some important results

fig1 = plt.figure()
plt.hist(dices)
fig1.suptitle(r'Rolls of the two dices')

fig2 = plt.figure()
plt.hist([item for sublist in result_value_won for item in sublist])
fig2.suptitle(r'Prizes won by the players')

fig3 = plt.figure()
plt.hist(casino_share)
fig3.suptitle(r'Share kept by the casino')

plt.show()

# Printing the average share kept by the casino

avg_share = sum(casino_share)/len(casino_share)
print(avg_share)

"""This shows that, on average, the casino keeps 10% of the bets and distributes 90% as prizes."""
