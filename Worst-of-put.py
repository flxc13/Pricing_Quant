import numpy as np
from tqdm import tqdm

# The required stock prices from the data
S10 = 31.00  # Starting price of S1
S20 = 29.10  # Starting price of S2
sigma1 = 0.21805  # Volatility of S1
sigma2 = 0.412894  # Volatility of S2
rho12 = 0.440247  # Correlation coefficient
r = 0.0495  # Interest rate (4.95% p.a.)
N1, N2 = 180, 2  # Number of time steps


def average_worst_of_put_option(S10, S20, sigma1, sigma2, rho12, r, N, paths):
    T = 1.0  # Maturity time in years
    dt = T / N  # Time step size
    payoff = np.zeros(paths)

    for i in tqdm(range(paths)):  # Simulated a payoff
        S1 = S10
        S2 = S20
        for j in range(N):
            Z1 = np.random.normal()  # Generate a random normal distributed number
            Z2 = rho12 * Z1 + np.sqrt(1 - rho12 ** 2) * np.random.normal()  # Generate a random correlated number

            S1 = S1 * np.exp((r - 0.5 * sigma1 ** 2) * dt + sigma1 * np.sqrt(dt) * Z1)  # New stock price
            S2 = S2 * np.exp((r - 0.5 * sigma2 ** 2) * dt + sigma2 * np.sqrt(dt) * Z2)
            if j == (N / 2 - 1):  # Record S11 and S21
                S11 = S1
                S21 = S2
            if j == (N - 1):  # Record S12 and S22
                S12 = S1
                S22 = S2
        B1 = min(S11 / S10, S21 / S20)
        B2 = min(S12 / S10, S22 / S20)
        A = (B1 + B2) / 2
        payoff[i] = np.maximum(1 - A, 0.0)

    option_price = np.exp(-r * T) * np.mean(payoff)
    return option_price


print("running")
# Calculate option prices
option_price_1 = average_worst_of_put_option(S10, S20, sigma1, sigma2, rho12, r, N1, 10000)
print("Option Price ia) (10000 paths):", option_price_1)
# option_price_2 = average_worst_of_put_option(S10, S20, sigma1, sigma2, rho12, r, N1, 300000)
# print("Option Price ib) (300000 paths):", option_price_2)
option_price_3 = average_worst_of_put_option(S10, S20, sigma1, sigma2, rho12, r, N2, 10000)
print("Option Price iia) (10000 paths):", option_price_3)
# option_price_4 = average_worst_of_put_option(S10, S20, sigma1, sigma2, rho12, r, N2, 300000)
# print("Option Price iib) (300000 paths):", option_price_4)
