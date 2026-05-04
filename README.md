#Algorithms for scheduling with many shared resources - Implementation and analysis of an exact algorithm

This repository contains code for the bachelor's thesis project "Algorithms for scheduling with many shared resources - Implementation and analysis of an exact algorithm" at the University of Gothenburg, 2026. 

The project aims to analyze and compare different algorithms for the many shared resources scheduling (MSRS) problem. 

## Project structure

To make it easy to navigate, the project is structured as follows: 

* `/algos/` - Code for the different algorithms for solving the MSRS-problem.
* `/results/` - Here the data is saved when running an algorithm.
* `/tests/` - The testfiles.
* `/utils/` - Code for the testgenerator and visualization of schedules. 

## Algorithms

The `/algos/` directory contains both our own exact solver for the MSRS problem, as well as approximation algorithms and heuristics used for performance evaluation and comparison.

### Our implementation: The exact solver

Our main contribution is an exact solver based on an integer linear programming (ILP) formulation, together with a machine assignment. We have developed five different versions of the ILP model, one standard and four optimized. 

* **Machine Assignment:** * `algos/machine_assignment.py` - This generates the machine assignment. 
* **ILP Versions:**
  * `algos/ILP_STD.py` - The standard, unoptimized ILP formulation.
  * `algos/ILP_LB.py` - Includes a lower bound of the makespan. 
  * `algos/ILP_WS.py` - Uses start values from an approximation algorithm together with a lower bound. **(Note: Requires running an approximation algorithm first).**
  * `algos/ILP_IC.py` - Uses indicator constraints instead of big-M formulations.
  * `algos/ILP_CMB.py` - Combines all previous optimizations. **(Note: Requires running an approximation algorithm first).**
* **Exact Solvers:** * `algos/exact_solver_X.py` - Complete program for solving the MSRS problem, using `algos/ILP_X.py` together with `algos/machine_assignment.py`.  

### Approximation algorithms and heuristics
To evaluate the performance of our exact solver, we compare it againts approximation algorithms and heuristics.
The code for these algorithms was not implemented by us. It is sourced from "bachelor-thesis-project-MSRS" and can be found here: https://github.com/ollelapidus/bachelor-thesis-project-MSRS. 

* **Included algorithms:** *
* `algo-gen/simulated-annealing.cpp`
* `algos/simulated-annealing-algo.cpp`
* `algos/3_over_2.py`
* `algos/3_over_2_with_downshift.py`
* `algos/3_over_2_with_enqueue.py`
* `algos/5_over_3.py`
* `algos/5_over_3_with_downshift.py`
* `algos/5_over_3_with_enqueue.py`
* `algos/enqueue.py`

## Prerequisites

You need to install [Gurobi](https://www.gurobi.com) to run the exact solvers.

## Usage

To run an algorithm or generate a testfile, use the provided bash scripts. 

**Standard Execution:**
```bash
# Generate a test file
./generate.sh

# Run and visualize an algorithm (e.g., the standard exact solver)
./visualize.sh algos/exact_solver_STD.py tests/test_a/test_a1.txt