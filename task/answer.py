import numpy as np
from scipy.stats import triang, lognorm, pareto

def calculate_probability_av(a, b, c, point1):
    dist = triang(c=(c - a) / (b - a), loc=a, scale=b - a)
    prob1 = dist.cdf(point1)
    return prob1

def calculate_mean_median_av(a, b, c):
    dist = triang(c=(c - a) / (b - a), loc=a, scale=b - a)
    MEAN_t = dist.mean()
    MEDIAN_t = dist.median()
    return MEAN_t, MEDIAN_t

def calculate_mean_variance_occurrences(number_set, prob_set):
    MEAN_d = np.sum(np.array(number_set) * np.array(prob_set))
    VARIANCE_d = np.sum(np.array(number_set) ** 2 * np.array(prob_set)) - MEAN_d ** 2
    return MEAN_d, VARIANCE_d

def monte_carlo_simulation(mu, sigma, xm, alpha, num, point2, point3, point4):
    impact_A = lognorm(sigma, scale=np.exp(mu))
    impact_B = pareto(alpha, scale=xm)
    
    total_impact_samples = impact_A.rvs(num) + impact_B.rvs(num)
    
    prob2 = np.sum(total_impact_samples > point2) / num
    prob3 = np.sum((point3 < total_impact_samples) & (total_impact_samples < point4)) / num
    
    return prob2, prob3

def calculate_ALE(MEAN_t, MEAN_d, prob2):
    EF = prob2
    SLE = MEAN_t * EF
    ARO = MEAN_d
    ALE = ARO * SLE
    return ALE

def Task1(a, b, c, point1, number_set, prob_set, num, point2, mu, sigma, xm, alpha, point3, point4):
    prob1 = calculate_probability_av(a, b, c, point1)
    MEAN_t, MEDIAN_t = calculate_mean_median_av(a, b, c)
    MEAN_d, VARIANCE_d = calculate_mean_variance_occurrences(number_set, prob_set)
    prob2, prob3 = monte_carlo_simulation(mu, sigma, xm, alpha, num, point2, point3, point4)
    ALE = calculate_ALE(MEAN_t, MEAN_d, prob2)
    
    return prob1, MEAN_t, MEDIAN_t, MEAN_d, VARIANCE_d, prob2, prob3, ALE

# Example usage:
a, b, c = 10, 50, 30
point1 = 20
number_set = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
prob_set = [0.1, 0.2, 0.15, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0.05]
num = 10000
point2 = 100
mu, sigma = 0.5, 0.1
xm, alpha = 50, 2
point3, point4 = 150, 200

result = Task1(a, b, c, point1, number_set, prob_set, num, point2, mu, sigma, xm, alpha, point3, point4)
print(result)