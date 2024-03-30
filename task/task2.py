# from dhCheck_Task2 import dhCheckCorrectness
import numpy as np
from scipy.stats import triang, lognorm, pareto
from scipy.optimize import linprog

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
    prob3 = (occurrences[-1][0] + occurrences[-1][1]) / prob_T_positive
    
    return prob1, prob2, prob3

num = 200
probs = [0.5,0.3,0.6,0.2,0.4,0.6]
table = [[14, 16, 20, 15], [17, 21, 20, 16], [12, 18, 15, 17]]
(prob1, prob2, prob3) = Task2(num, table, probs)
print(prob1,prob2,prob3)
# num = 100  # Example value, you should replace it with your actual data
# table = [
#     [10, 20, 30],
#     [40, 50, 60],
#     [70, 80, 90],
#     [100, 110, 120]
# ]
# probs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]     

# # Call Task2 function
# result = Task2(num, table, probs)
# prob1, prob2, prob3 = Task2(num, table, probs)
# print(result)
# print("Probability 1: ",prob1)
# print("Probability 2: ",prob2)
# print("Probability 3: ",prob3)
