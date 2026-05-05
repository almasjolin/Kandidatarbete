# Algorithms for scheduling with many shared resources - Implementation and analysis of an exact algorithm

This repository contains code for the bachelor's thesis project "Algorithms for scheduling with many shared resources - Implementation and analysis of an exact algorithm" at the University of Gothenburg, 2026. 

The project aims to analyze and compare different algorithms for the many shared resources scheduling (MSRS) problem. 

## Project structure

To make it easy to navigate, the project is structured as follows: 

* `/algos/` - Code for the different algorithms for solving the MSRS-problem.
* `/results/` - Here the data is saved when running an algorithm.
* `/tests/` - The testfiles used for evaluating the algorithms. 
* `/utils/` - Code for the test generator and visualization of schedules. 

## Algorithms

The `/algos/` directory contains both our own exact solver for the MSRS problem, as well as approximation algorithms and heuristics used for performance comparison.

### Our implementation: The exact solver

Our main contribution is an exact solver based on an integer linear programming (ILP) formulation, together with a machine assignment. We have developed five different versions of the ILP model: one standard and four optimized. 

* **Machine assignment:**  `algos/machine_assignment.py` - This generates the machine assignment. 
* **ILP versions:**
  * `algos/ILP_STD.py` - The standard, unoptimized ILP formulation.
  * `algos/ILP_LB.py` - Includes a lower bound of the makespan. 
  * `algos/ILP_WS.py` - Uses start values from an approximation algorithm together with a lower bound. **(Note: Requires running an approximation algorithm first).**
  * `algos/ILP_IC.py` - Uses indicator constraints instead of big-M formulations.
  * `algos/ILP_CMB.py` - Combines all previous optimizations. **(Note: Requires running an approximation algorithm first).**
* **Exact solvers:**  `algos/exact_solver_X.py` - Complete program for solving the MSRS problem, using `algos/ILP_X.py` together with `algos/machine_assignment.py`.  

### Approximation algorithms and heuristics
To evaluate the performance of our exact solver, we compare it againts approximation algorithms and heuristics.
The code for these algorithms was not implemented by us. It is sourced from the "bachelor-thesis-project-MSRS" repository and can be found here: https://github.com/ollelapidus/bachelor-thesis-project-MSRS. 

* **Included algorithms:** 
    * `algo-gen/simulated-annealing.cpp`
    * `algos/simulated-annealing-algo.cpp`
    * `algos/3_over_2.py`
    * `algos/3_over_2_with_downshift.py`
    * `algos/3_over_2_with_enqueue.py`
    * `algos/5_over_3.py`
    * `algos/5_over_3_with_downshift.py`
    * `algos/5_over_3_with_enqueue.py`
    * `algos/enqueue.py`
    * `algos/greedy.py`

## Prerequisites

You need to install [Gurobi](https://www.gurobi.com) to run the exact solvers.

## Usage

To run an algorithm or generate a testfile, use the provided bash scripts. The test data is saved in the txt-file `tests/test.txt`, and the result data from the exact solvers is saved in the csv-file `progress_data.csv`. 

**Standard execution:**
```bash
# Generate a test file
./generate.sh

# Run and visualize an algorithm (e.g., the standard exact solver)
./visualize.sh algos/exact_solver_STD.py tests/your_testfile.txt

```

**Run exact solver with start values:**
```bash
#First, run an approximation algorithm whose solution you want as start values (e.g., the 3/2-approximation)
./visualize.sh algos/3_over_2.py tests/your_testfile.txt

#Then, run the exact solver (the warm start or combined solver)
./visualize.sh algos/exact_solver_WS.py tests/your_testfile.txt