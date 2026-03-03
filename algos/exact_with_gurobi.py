# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 15:09:01 2026

@author: idagu
"""

import sys
from ILP import solve_ilp
from maskintilldelning import maskintilldelning

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

T = max(
    1/m * sum(job_time.values()),
    max(
        [sum([job_time[x] for x in class2ids[c]]) for c in classes]
    ),
    sum(sorted(job_time.values())[m-1:m+1])
)

print(f"Lower bound for optimal solution: T = {T}")

makespan, t_solution = solve_ilp(n, job_time, m, class2ids)
sigma = maskintilldelning(t_solution, m, job_time)

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