import copy
import numpy as np
from scipy.stats import triang, lognorm, pareto

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

def hill_climbing_task1(a, b, c, point1, number_set, prob_set, num, point2, mu, sigma, xm, alpha, point3, point4, max_iterations=1000):
    best_solution = (a, b, c, point1, number_set, prob_set, num, point2, mu, sigma, xm, alpha, point3, point4)
    best_output = Task1(*best_solution)
    best_objective = best_output[-1]  # ALE as the objective function
    
    for iteration in range(max_iterations):
        current_solution = copy.deepcopy(best_solution)
        current_output = Task1(*current_solution)
        current_objective = current_output[-1]
        
        # Generate neighbors by making small changes to the current solution
        neighbor = perturb_solution(current_solution)
        neighbor_output = Task1(*neighbor)
        neighbor_objective = neighbor_output[-1]
        
        # If the neighbor has a better objective value, update the current solution
        if neighbor_objective > current_objective:
            current_solution = neighbor
            current_output = neighbor_output
            current_objective = neighbor_objective
            
            # Update the best solution if needed
            if current_objective > best_objective:
                best_solution = current_solution
                best_output = current_output
                best_objective = current_objective
    
    return best_output

def perturb_solution(solution):
    # Example perturbation: Randomly adjust one parameter (you can customize this based on your problem)
    index_to_perturb = np.random.choice(len(solution))
    perturbed_solution = list(solution)
    perturbed_solution[index_to_perturb] += np.random.uniform(-1, 1)
    return tuple(perturbed_solution)

# Example usage:
# Define initial solution
initial_solution = (a, b, c, point1, number_set, prob_set, num, point2, mu, sigma, xm, alpha, point3, point4)

# Run hill climbing
best_output = hill_climbing_task1(*initial_solution)

# Print the best solution and its output
print("Best Output:", best_output)