import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Define the DEAP creator and toolbox
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()

# Define problem-specific parameters
num_jobs = 3
num_machines = 3

# Register the individual and population
toolbox.register("individual", tools.initIterate, creator.Individual, lambda: np.random.permutation(num_jobs * num_machines))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the objective function (total completion time)
def objective(individual):
    completion_times = np.zeros(num_jobs, dtype=int)

    for i in range(num_jobs * num_machines):
        job = individual[i] // num_machines
        machine = individual[i] % num_machines

        if machine == 0:
            start_time = 0
        else:
            if i > 0:
                prev_job = individual[i - 1] // num_machines
                start_time = max(completion_times[job], completion_times[prev_job])
            else:
                start_time = 0

        processing_time = np.random.randint(1, 10)  # Replace this with your actual processing time function
        completion_times[job] = start_time + processing_time


    return np.max(completion_times),

toolbox.register("evaluate", objective)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selBest)

# Local search method (exchange two randomly selected jobs)

def local_search(individual):
    idx1, idx2 = np.random.choice(len(individual), 2, replace=False)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual,

toolbox.register("local_search", local_search)

# Main DEAP differential evolution algorithm with iteration tracking
def differential_evolution_with_iteration(pop_size, max_iterations):
    population = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(1)
    iteration_data = []

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)

    for iteration in range(max_iterations):
        algorithms.varAnd(population, toolbox, cxpb=0.7, mutpb=0.2)

        fitnesses = toolbox.map(toolbox.evaluate, population)
        for ind, fit in zip(population, fitnesses):
            ind.fitness.values = fit

        hof.update(population)

        iteration_data.append(np.min([ind.fitness.values[0] for ind in population]))

    # Plot iteration curve
    plt.plot(range(1, max_iterations + 1), iteration_data, marker='o')
    plt.xlabel('Iteration')
    plt.ylabel('Best Fitness')
    plt.title('Iteration Curve')
    plt.show()

    return hof[0]

# Plot Gantt chart
def plot_gantt_chart(individual):
    completion_times = np.zeros(num_jobs, dtype=int)
    gantt_data = []

    for i in range(num_jobs * num_machines):
        job = individual[i] // num_machines
        machine = individual[i] % num_machines

        if machine == 0:
            start_time = 0
        else:
            start_time = max(completion_times[job], completion_times[individual[i - 1]])

        processing_time = np.random.randint(1, 10)  # Replace this with your actual processing time function
        completion_times[job] = start_time + processing_time

        gantt_data.append((job, machine, start_time, start_time + processing_time))

    gantt_data.sort(key=lambda x: (x[0], x[2]))  # Sort by job and start time

    fig, ax = plt.subplots()
    for entry in gantt_data:
        ax.broken_barh([(entry[2], entry[3] - entry[2])], (entry[0], 1), facecolors=('tab:blue'))

    ax.set_yticks(range(num_jobs))
    ax.set_yticklabels([f'Job {i}' for i in range(num_jobs)])
    ax.set_xlabel('Time')
    ax.set_title('Gantt Chart')
    plt.show()

# Main function
def main():
    pop_size = 10
    max_iterations = 50

    best_solution = differential_evolution_with_iteration(pop_size, max_iterations)

    print("Best Solution:")
    print(best_solution)

    # Plot Gantt chart
    plot_gantt_chart(best_solution)

if __name__ == "__main__":
    main()