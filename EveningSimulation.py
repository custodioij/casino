import Casino as Ca
from matplotlib import pyplot as plt

sim_results = []
for i in range(1000):
    monte_carlo = Ca.Casino()
    sim_results.append(monte_carlo.simulate_evening(super_silent=True))
    print(i)

fig1 = plt.figure()
plt.hist(sim_results)
fig1.suptitle(r'Distribution of the profit of the casino')

plt.show()
