# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 20:31:33 2026

@author: rebec
"""

from ILP import solve_ilp
from maskintilldelning import maskintilldelning

# ---testinstans---

jobs = [1,2,3,4]
p = {1:2, 2:3, 3:1, 4:4}
m = 2
machines = [1,2]
classes = {
    "A": [1,3],
    "B": [2],
    "C": [4]
}

# ---kör ILP---

T, t_solution = solve_ilp(jobs, p, m, classes)

print("Makespan:", T)
print("Starttider:", t_solution)

# ---maskintilldelning---

sigma = maskintilldelning(t_solution, machines, p)

print("Maskintilldelning:", sigma)
