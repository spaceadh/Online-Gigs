import numpy as np
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

# Define inputs
a = 10
b = 20
c = 15
point1 = 17
number_set = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
prob_set = [0.05, 0.1, 0.15, 0.2, 0.15, 0.1, 0.1, 0.05, 0.05, 0.05]
num = 10000
point2 = 200
mu = 0.5
sigma = 0.2
xm = 100
alpha = 2
point3 = 300
point4 = 400

# Call Task1 function
result = Task1(a, b, c, point1, number_set, prob_set, num, point2, mu, sigma, xm, alpha, point3, point4)

print("*******Task 1*******")
# Print results
print("Probability that AV is no greater than point1:", result[0])
print("Mean of AV:", result[1])
print("Median of AV:", result[2])
print("Mean of numbers of annual occurrences:", result[3])
print("Variance of numbers of annual occurrences:", result[4])
print("Probability that total impact is greater than point2:", result[5])
print("Probability that total impact is between point3 and point4:", result[6])
print("Annualized Loss Expectancy (ALE):", result[7])

def Task2(num, table, probs):
    # Extracting the table data
    X_values = [2, 3, 4, 5]
    Y_values = [6, 7, 8]
    occurrences = table
    
    # (1) Calculate the probability 𝐩𝐫𝐨𝐛𝟏 of 3 ≤ X ≤ 4 and the probability 𝐩𝐫𝐨𝐛𝟐 of X+Y ≤ 10
    prob1 = sum([occurrences[i][j] for i in range(1, 3) for j in range(len(Y_values))]) / num
    prob2 = sum([occurrences[i][j] for i in range(len(X_values)) for j in range(len(Y_values)) if X_values[i] + Y_values[j] <= 10]) / num
    
    # (2) Find the probability 𝐩𝐫𝐨𝐛𝟑 of Y=8 given that a case is tested positive
    prob_T_positive = sum([sum(occurrences[i]) for i in range(len(occurrences))]) / num
    prob_Y_8_given_T_positive = (occurrences[-1][0] + occurrences[-1][1]) / prob_T_positive
    
    return (prob1, prob2, prob_Y_8_given_T_positive)

# Define inputs
num = 100  # Example value, you should replace it with your actual data
table = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90],
    [100, 110, 120]
]
probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # Example values, replace them with your actual data

# Call Task2 function
result = Task2(num, table, probs)

# Print results
print("Probability of 3 ≤ X ≤ 4:", result[0])
print("Probability of X+Y ≤ 10:", result[1])
print("Probability of Y=8 given that a case is tested positive:", result[2])

# Features (x)
x = [
    [11, 12, 13, 14, 15],
    [21, 22, 23, 24, 25],
    [31, 32, 33, 34, 35],
    [41, 42, 43, 44, 45]
]

# Target variables (y and z)
y = [1, 2, 3, 4]   # Corresponding to the first 4 rows of x
z = [6, 7, 8, 9]   # Corresponding to the first 4 rows of x

x_initial = [1, 1, 1, 1]
c = [1, 1, 1, 1]
x_bound = [10, 10, 10, 10]
se_bound = 30
ml_bound = 50

def compute_weights(x, y, z):
    # Convert inputs to NumPy arrays
    X = np.column_stack((np.ones(len(x)), np.array(x)))  # Add a column of ones for the intercept
    
    # Print shapes for debugging
    print("Shape of X:", X.shape)
    print("Shape of y:", np.array(y).shape)
    
    # Perform linear regression for weights_b
    weights_b = np.linalg.lstsq(X, y, rcond=None)[0]
    print(weights_b)
    
    # Perform linear regression for weights_d
    weights_d = np.linalg.lstsq(X, z, rcond=None)[0]
    print(weights_d)
    
    return weights_b, weights_d

# Example inputs
x = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8]]
y = [10, 20, 30, 40]
z = [50, 60, 70, 80]
x_initial = [1, 2, 3, 4]
c = [100, 200, 300, 400]
x_bound = [5, 6, 7, 8]  # Corrected x_bound list
se_bound = 200
ml_bound = 300

# Example usage:
# weights_b, weights_d = compute_weights(x, y, z)

# print("Weights_b:", weights_b)
# print("Weights_d:", weights_d)

# print("Additional security controls:", x_add)