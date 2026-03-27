# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:44:14 2026

@author: idagu
"""
import random
import numpy as np

#Generates a random Poisson-distributed integer with average mu in the range [lb, ub]
def truncated_poisson(mu, lb, ub):
    while True:
       value = np.random.poisson(mu)
       
       if lb <= value <= ub:
           return value

#Distributes target_sum into num_parts subsums by creating break points
#Makes sure that each subsum is not too large by using upper bound ub
def create_breaks_with_bounds(target_sum, num_parts, ub): 
    result = [1]*num_parts
    remaining = target_sum - sum(result)
    indices = list(range(num_parts))
    average_val = target_sum/num_parts
    
    while remaining > 0: 
        random.shuffle(indices)
        
        for i in indices: 
            upper_bound = ub[i]
            
            if remaining <= 0: break
        
            current_val = result[i]
            left_until_average = average_val - current_val
            
            #We only add if it is allowed and we are not above average
            if current_val < upper_bound and left_until_average > 0: 
                can_add = min(remaining,upper_bound-current_val)
                
                if can_add < left_until_average: 
                    add = can_add
                    
                else: 
                    add = truncated_poisson(left_until_average, 1, can_add)
                result[i] += add
                remaining -= add
    
    tot = result[0]           
    for i in range(1, len(result)):
        tot += result[i]
        result[i] = tot
    
    return result

m = 4 #Number of machines
c = 6 #Number of classes
n = 18 #Number of jobs
T = 1000 #Optimal makespan

total_time = m*T

#Create the processing times for the jobs by creating break points
#Make sure the jobs finishes exactly at T

machine_breaks = [i * T for i in range(1, m)]

class_breaks = create_breaks_with_bounds(total_time, c, [T]*c)

all_breaks = sorted(list(set(machine_breaks + class_breaks)))

#Fewer jobs than break points (can happen only if n < m + c)
if n < len(all_breaks): 
    
    #Replace class break points with machine break points
    for i in range(len(all_breaks)-n):
        class_breaks[i] = 1000*(i+1)
        
    all_breaks = sorted(list(set(machine_breaks + class_breaks)))
        
else: 
    #Create the remaining break points
    internal_breaks = random.sample(range(1, total_time), n - m - c)
    
    all_breaks = sorted(list(set(all_breaks + internal_breaks)))
    
    #If duplicates
    while len(all_breaks) < n: 
        new_break = random.randint(1, total_time - 1)
        if new_break not in all_breaks:
            all_breaks.append(new_break)
            all_breaks.sort()

jobs = []

last_time = 0
last_class = 1
for b in all_breaks: 
    job_time = b - last_time
    jobs.append((job_time, last_class))
    last_time = b
    
    if b in class_breaks: 
        last_class += 1

np.random.shuffle(jobs)

print(m)
for job_time, job_class in jobs:
    print(job_time, job_class)     