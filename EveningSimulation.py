import Casino as Ca
from matplotlib import pyplot as plt
import pandas as pn
import numpy as np
from scipy.stats import gaussian_kde
"""
Questions to awnser:
1) Evolution of cashflow over 1000 simulations.

2) Profit of Craps and Roulette tables

3) Tips (barmen) per night agains commissions (croupiers).
    It is much better to be a barman

4) Profit of an evening, for many values of expected_return (including statistics and distribution).

4)
# print("VaR(5%) = " + str(np.percentile(daily_profit, 5)))

# pandas.to_latex()
"""
# First define a simulations function


def simulate_casino(n_sim=30, capacity=100, expected_return='default', n_barmen=4, reset=False):
    """Runs a Monte Carlo simulation on the Monte Carlo casino, and returns the results in a pandas data frame"""
    profit = []
    tips = []
    commission = []
    cash = []
    roulette_profit = []
    craps_profit = []
    monte_carlo = Ca.Casino()
    for i in range(n_sim):
        profit.append(monte_carlo.simulate_evening(capacity=capacity, expected_return=expected_return,
                                                   n_barmen=n_barmen, super_silent=True))
        tips.append(float(sum([x.tips for x in monte_carlo.barmen])))
        commission.append(float(sum([x.commission for x in monte_carlo.croupiers])))
        cash.append(monte_carlo.cash)
        craps_profit.append(sum([x.profit for x in monte_carlo.c_tables]))
        roulette_profit.append(sum([x.profit for x in monte_carlo.r_tables]))
        if reset:
            monte_carlo = Ca.Casino()
        print(i + 1)
    sim_results_df = pn.DataFrame({'profit': profit, 'cash': cash, 'tips': tips, 'tips per barman': [x/4 for x in tips],
                                   'commission': commission, 'commission per croupier': [x/20 for x in commission],
                                   'craps profit': craps_profit, 'roulette profit': roulette_profit})
    return sim_results_df

# 1) Evolution of cashflow over 1000 simulations:

sim_results = simulate_casino(n_sim=1000)

loss_x = [x for x in sim_results['profit'] if x < 0]
loss_y = [list(y)[0] for y in enumerate(sim_results['profit'])if y[1] < 0]

plt.figure()
plt.subplot(211)
plt.plot(sim_results['cash'])
plt.title('Evolution of the casino\'s cashflow')
plt.axhline(color='r')
plt.subplot(212)
plt.plot(sim_results['profit'], color='b')
plt.scatter(loss_y, loss_x, color='r')
plt.axhline(color='r')
plt.title('Evolution of the casino\'s daily profit')
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
plt.savefig('profit_and_cashflow.png')

# 2) Profit of Craps and Roulette tables

craps_daily = [sim_results['craps profit'][i] - sim_results['craps profit'][i-1]
               for i in range(1, sim_results.shape[0])]
roulette_daily = [sim_results['roulette profit'][i] - sim_results['roulette profit'][i-1]
                  for i in range(1, sim_results.shape[0])]
craps_dens = gaussian_kde(craps_daily)
roulette_dens = gaussian_kde(roulette_daily)
xs = np.linspace(-50000, 50000)
plt.figure()
plt.plot(xs, craps_dens(xs), label="Craps", color="b")
plt.plot(xs, roulette_dens(xs), label="Roulette", color="g")
plt.axvline(color='r')
plt.title('Profit per table (gaussian density estimation)')
plt.legend()
plt.savefig('craps_and_roulette_dens.png')  # Density estimation plot

plt.figure()
plt.hist(craps_daily, bins=25, label="Craps", color="b", alpha=0.5)
plt.hist(roulette_daily, bins=25, label="Roulette", color="g", alpha=0.5)
plt.axvline(color='r')
plt.title('Profit per table (histogram)')
plt.legend()
plt.savefig('craps_and_roulette.png')

# 3) Tips (barmen) per night against commissions (croupiers)

plt.figure()
plt.subplot(211)
plt.hist(sim_results['tips per barman'])
plt.title('Distribution of tips earned by the barman')
plt.subplot(212)
plt.hist(sim_results['commission per croupier'])
plt.title('Distribution of commissions earned by the croupiers')
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
plt.savefig('tips_and_comissions.png', dpi=200)

# 4) Profit of an evening, for many values of expected_return (including statistics and distribution).

ER = [0.5, 0.9, 1, 1.2, 1.5, 2]  # Expected value of betting

sim_results = [simulate_casino(n_sim=200, expected_return=value, reset=True) for value in ER]

fig = plt.figure(figsize=(11, 11))
for i in range(len(ER)):
    fig.add_subplot(230+i+1)
    plt.hist(sim_results[i-1]['profit'], range=[-100000, 50000], bins=25,  label=str(ER[i]))
    plt.title('Daily profit for expected return = ' + str(ER[i]))
plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25, wspace=0.35)
plt.savefig('profit_by_ER.png')

# 5) Simulation statistics
