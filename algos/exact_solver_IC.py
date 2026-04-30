# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:03:22 2026

@author: rebec
"""

import sys
import time
from ILP_IC import ilp_ic
from machine_assignment import machine_assignment

## Read input ##
job_class = {} # [i] --> class of i:th job, i = 0, ..., n-1
job_time = {} # [i] --> duration of i:th job, i = 0, ..., n-1
class2ids = {} # [c] --> list of id:s of jobs in class c, c = 1, ..., number of classes

data = sys.stdin.readlines()
m = int(data[0]) # Number of machines
n = 0 # Number of jobs
for id, line in enumerate(data[1:]):
    line = line.strip()
    if line == "":
        break
    t, c = [int(i) for i in line.split()]
    job_time[id] = t
    job_class[id] = c
    n += 1

    if c not in class2ids.keys():
        class2ids[c] = []
    
    class2ids[c].append(id)

classes = list(class2ids.keys())

start_time = time.perf_counter()

# Lower bound for optimal solution
T = max(
    1/m * sum(job_time),
    max(
        [sum([job_time[x] for x in class2ids[c]]) for c in classes]
    ),
    sum(sorted(job_time,reverse=True)[m-1:m+1])
)

print(f"Lower bound for optimal solution: T = {T}")

makespan, t_solution = ilp_ic(n, job_time, m, class2ids)
sigma = machine_assignment(t_solution, m, job_time)

end_time = time.perf_counter()
execution_time = end_time-start_time
print(f"Running time: {execution_time:.4f} seconds")

fraction = makespan / T

print(f"Makespan: {makespan}")
print(f"Fraction: {fraction:.3f}")
print(f"Percentage over: {(fraction-1)*100:.2f}%")
# Save data to file
if "--write" in sys.argv:
    with open("temp.txt", "w") as f:
        f.write(f"{n} {m}\n")  # First line: n and m
        for i in range(n):
            f.write(f"{t_solution[i]} {sigma[i]} {job_time[i]} {job_class[i]}\n")
    f.close()