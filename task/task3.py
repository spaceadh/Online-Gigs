from dhCheck_Task3 import dhCheckCorrectness
import numpy as np
from scipy.stats import triang, lognorm, pareto
from scipy.optimize import linprog

def Task3(x, y, z, x_initial, c, x_bound, se_bound, ml_bound):
    # TODOreturn (weights_b, weights_d, x_add)
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

    print("************************************")
    print("************weight_add calculations*********")
    
    num_types = len(x_initial)

    # Formulate the linear programming problem
    X = np.column_stack((np.ones(len(x)), np.array(x)))  # Add a column of ones for the intercept
    c_lp = np.array(c)
    A_eq = np.ones((1, num_types))
    b_eq = np.array([se_bound])

    A_ub = np.vstack([X[:, 1:].T, -np.eye(num_types)])

    # Separate the upper bound for each type of security control and the remaining maintenance load
    x_bound_ub = np.array(x_bound)  # Ensure x_bound_ub is 1-D
    ml_bound_ub = ml_bound - np.dot(x_initial, x_bound)
    
    # Concatenate the upper bounds
    b_ub = np.concatenate((x_bound_ub, [ml_bound_ub]))

    # Solve the linear programming problem
    res = linprog(c_lp, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub)
    x_add = res.x

    return weights_b, weights_d, x_add

