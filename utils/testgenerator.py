# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 13:02:04 2026

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

#Distributes target_sum into num_parts subsums
#Makes sure that each subsum is not too small or too large
def distribute_sum_with_bounds(target_sum, num_parts, ub): 
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
    
    return result

m = 9 #Number of machines
c = 10 #Number of classes
n = 30 #Number of jobs
T = 1000 #Optimal makespan

jobs= [] #jobs[i] --> (processing time,class) for job i, i = 0, ..., n-1
  
#class_process_times[c'] --> total processing time for class c', c' = 0,...,c-1
class_process_times = distribute_sum_with_bounds(m*T, c, [T]*c)

#num_jobs_in_each_class[c'] --> number of jobs in class c', c' = 0,...,c-1
num_jobs_in_each_class = distribute_sum_with_bounds(n, c, class_process_times)


for i in range(c): 
    class_time = class_process_times[i]
    num_jobs_in_class = num_jobs_in_each_class[i]
    
    #job_process_times[j] --> processing time for j:th job in i:th class
    job_process_times = distribute_sum_with_bounds(class_time, num_jobs_in_class, [class_time]*num_jobs_in_class)
    for j in range(num_jobs_in_class):
        #In the test files, the class indexing starts on 1
        jobs.append((job_process_times[j], i+1))

np.random.shuffle(jobs)

print(m)
for job_time, job_class in jobs:
    print(job_time, job_class)  
