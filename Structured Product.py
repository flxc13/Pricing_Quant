import numpy as np
from tqdm import tqdm

NOM = 100000
K0 = 0.9  # Strike percentage
KI = 0.86  # Knock-in level
AC = 1.02  # Auto-call level
CP = 0.0125  # Coupon per month
rf = 0.0495  # HKD interest rate
rd = 0.023  # CNY interest rate
sigma_fx = 0.075  # Volatility of CNYHKD
rho = 0.45  # Correlation of S1 and fx
S0 = 31  # Initial stock price
N = 180  # time step
sigma = 0.458  # Implied Volatility
rg = rf + rho * sigma * sigma_fx  # Calculate rg
print(rg)

Pc = S0 * AC  # Auto-call price
K = K0 * S0  # Strike price
Pk = S0 * KI  # Knock-in price
T = 1 / 2  # Expiry date
dt = T / N  # Time step size


def calculate_fair_price(paths):
    auto_call_count = 0
    payoff = np.zeros(paths)

    for j in tqdm(range(paths)):
        S = S0
        auto_call_condition_met = False
        auto_knock_in_condition_met = False
        Coupon = 0
        day = 0
        accrued = 0

        for i in range(0, 180):  # Simulate one payoff
            Z = np.random.normal()
            S += S * (rg * dt + sigma * Z * np.sqrt(dt))
            day += 1

            if day % 30 == 0:  # Pay coupon
                Coupon += np.exp(-rd * (day / 360)) * NOM * CP

            if S < Pk and not auto_knock_in_condition_met:  # Check for Knock-in event
                auto_knock_in_condition_met = True

            if i >= 29 and S >= Pc and not auto_call_condition_met:  # Check for auto call
                auto_call_condition_met = True
                auto_call_count += 1
                break
        SM = S

        if auto_call_condition_met and day % 30 != 0:
            accrued = np.exp(-rd * (day / 360)) * CP * NOM * ((day % 30)/30)
            payoff[j] = np.exp(-rd * (day/360)) * NOM + Coupon + accrued
        elif auto_knock_in_condition_met and SM >= K:
            payoff[j] = np.exp(-rd * (day/360)) * NOM + Coupon
        elif auto_knock_in_condition_met and SM < K:
            payoff[j] = np.exp(-rd * (day / 360)) * (SM / K) * NOM + Coupon
        else:
            payoff[j] = np.exp(-rd * (day / 360)) * NOM + Coupon

    fair_price = np.mean(payoff)
    return fair_price, auto_call_count


fair_price_10k, auto_call_count_10k = calculate_fair_price(10000)
print("Fair Price (10,000 Monte Carlo paths):", fair_price_10k)
print("Number of auto-calls (10,000 Monte Carlo paths):", auto_call_count_10k)
profit_margin = (NOM - fair_price_10k) / NOM * 100
print("Profit margin of the investment bank:", '%.5f' % profit_margin, "%")

fair_price_300k, auto_call_count_300k = calculate_fair_price(300000)
print("Fair Price (300,000 Monte Carlo paths):", fair_price_300k)
print("Number of auto-calls (300,000 Monte Carlo paths):", auto_call_count_300k)
profit_margin = (NOM - fair_price_300k) / NOM * 100
print("Profit margin of the investment bank:", '%.5f' % profit_margin, "%")
