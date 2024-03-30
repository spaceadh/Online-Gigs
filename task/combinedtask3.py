import numpy as np
from scipy.optimize import linprog

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

# def compute_x_add(x, x_initial, c, x_bound, se_bound, ml_bound):
#     num_types = len(x_initial)

#     # Formulate the linear programming problem
#     X = np.column_stack((np.ones(len(x)), np.array(x)))  # Add a column of ones for the intercept
#     c_lp = np.array(c)
#     A_eq = np.ones((1, num_types))
#     b_eq = np.array([se_bound])

#     A_ub = np.vstack([X[:, 1:].T, -np.eye(num_types)])
#     # b_ub = np.concatenate([(ml_bound - np.array(z)), x_bound])
#     b_ub = np.concatenate([(ml_bound - np.array(z)), x_bound]).flatten()

#     print("Shape of X:", X.shape)
#     print("Shape of A_eq:", A_eq.shape)
#     print("Shape of b_eq:", b_eq.shape)
#     print("Shape of A_ub:", A_ub.shape)
#     print("Shape of b_ub:", b_ub.shape)
#     print("Values of b_ub:", b_ub)

#     # Solve the linear programming problem
#     res = linprog(c_lp, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub)
#     x_add = res.x

#     return x_add


# def compute_x_add_alternative(x, x_initial, c, x_bound, se_bound, ml_bound):
#     num_types = len(x_initial)

#     # Formulate the linear programming problem
#     X = np.column_stack((np.ones(len(x)), np.array(x)))  # Add a column of ones for the intercept
#     c_lp = np.array(c)
#     A_eq = np.ones((1, num_types))
#     b_eq = np.array([se_bound])

#     A_ub = np.vstack([X[:, 1:].T, -np.eye(num_types)])
#     b_ub = np.concatenate([(ml_bound - np.array(z)), x_bound])

#     # Solve the linear programming problem
#     res = linprog(c_lp, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub, method='highs')
#     x_add = res.x

#     return x_add

# def compute_x_add(x, x_initial, c, x_bound, se_bound, ml_bound):
#     num_types = len(x_initial)

#     # Formulate the linear programming problem
#     X = np.column_stack((np.ones(len(x)), np.array(x)))  # Add a column of ones for the intercept
#     c_lp = np.array(c)
#     print(c)
#     A_eq = np.ones((1, num_types))
#     b_eq = np.array([se_bound])

#     A_ub = np.vstack([X[:, 1:].T, -np.eye(num_types)])
#     # A_ub = np.concatenate([(ml_bound - np.array(z)), x_bound])
#     print(A_ub)
#     # Separate the upper bound for each type of security control and the remaining maintenance load
#     x_bound_ub = x_bound
#     ml_bound_ub = ml_bound - np.dot(x_initial, x_bound)
    
#     # Concatenate the upper bounds
#     b_ub = np.concatenate((x_bound_ub, [ml_bound_ub]))

#     # b_ub = np.concatenate([(ml_bound - np.array(z)), x_bound])
#     print(b_ub)

#     # Solve the linear programming problem
#     res = linprog(c_lp, A_eq=A_eq, b_eq=b_eq, A_ub=A_ub, b_ub=b_ub)
#     x_add = res.x

#     return x_add

def compute_x_add(x, x_initial, c, x_bound, se_bound, ml_bound):
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

    return x_add

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

# Example usage:
# weights_b, weights_d = compute_weights(x, y, z)

# print("Weights_b:", weights_b)
# print("Weights_d:", weights_d)
x_add = compute_x_add(x, x_initial, c, x_bound, se_bound, ml_bound)
print("Number of additional security controls (x_add):", x_add)
