from dhCheck_Task1 import dhCheckCorrectness
import numpy as np
import copy
from scipy.stats import triang, lognorm, pareto
from scipy.optimize import linprog


def Task1(a, b, c, point1, number_set, prob_set, num, point2, mu, sigma, xm, alpha, point3, point4):
    # (1) (i) Find the probability 𝐩𝐫𝐨𝐛𝟏 that the AV is no greater than 𝐩𝐨𝐢𝐧𝐭𝟏
    dist_AV = triang(c=(c - a) / (b - a), loc=a, scale=b - a)
    prob1 = dist_AV.cdf(point1)
    
    # (1) (ii) Find the mean MEAN_t and median MEDIAN_t of the AV
    MEAN_t = dist_AV.mean()
    MEDIAN_t = dist_AV.median()
    
    # (2) Calculate the mean MEAN_d and variance VARIANCE_d of the numbers of annual occurrences
    MEAN_d = np.dot(number_set, prob_set)
    VARIANCE_d = np.dot((number_set - MEAN_d)**2, prob_set)
    
    # (3) Monte Carlo simulation for total impact
    np.random.seed(0)  # for reproducibility
    num_samples = 100000  # number of Monte Carlo samples
    impact_A = lognorm.rvs(s=sigma, scale=np.exp(mu), size=num_samples)
    impact_B = pareto.rvs(b=alpha, scale=xm, size=num_samples)
    total_impact = impact_A + impact_B
    
    # (3) (i) Randomly sample num points for the total impact
    sampled_points = np.random.choice(total_impact, num)
    
    # (3) (ii) Derive the probability prob2 that the total impact is greater than point2
    prob2 = np.mean(total_impact > point2)
    
    # (3) (iii) Derive the probability prob3 that the total impact is between point3 and point4
    prob3 = np.mean((point3 < total_impact) & (total_impact < point4))
    
    # (4) Calculate the value of the ALE
    EF = prob2  # Using prob2 as EF
    SLE = MEAN_t * EF
    ARO = MEAN_d
    ALE = ARO * SLE
    
    return prob1, MEAN_t, MEDIAN_t, MEAN_d, VARIANCE_d, prob2, prob3, ALE

# # Define inputs
# a = 10
# b = 20
# c = 15
# point1 = 17
# number_set = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# prob_set = [0.05, 0.1, 0.15, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05]
# num = 10000
# point2 = 200
# mu = 0.5
# sigma = 0.2
# xm = 100
# alpha = 2
# point3 = 300
# point4 = 400

# # Call Task1 function
# result = Task1(a, b, c, point1, number_set, prob_set, num, point2, mu, sigma, xm, alpha, point3, point4)

# print("*******Task 1*******")
# # Print results
# print("Probability that AV is no greater than point1:", result[0])
# print("Mean of AV:", result[1])
# print("Median of AV:", result[2])
# print("Mean of numbers of annual occurrences:", result[3])
# print("Variance of numbers of annual occurrences:", result[4])
# print("Probability that total impact is greater than point2:", result[5])
# print("Probability that total impact is between point3 and point4:", result[6])
# print("Annualized Loss Expectancy (ALE):", result[7])