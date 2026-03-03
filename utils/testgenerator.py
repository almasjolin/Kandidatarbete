# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 13:02:04 2026

@author: idagu
"""
import random
import numpy as np


#Generates a random Poisson-distributed integer in the range [lb, ub]
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
                
# def generate_class_processing_times(m,c,T): 
#     target_sum = m*T
#     average_time = m*T/c
#     class_processing_times = [1]*c
#     remaining = target_sum - c
    
#     indices = list(range(c))
#     while remaining > 0:
#          random.shuffle(indices) # För att sprida ut värdena rättvist
#          for i in indices:
#              if remaining <= 0: break
             
#              current_val = class_processing_times[i]
#              if current_val < T:
#                  # Lägg till så mycket som möjligt, men max upp till T
#                  can_add = min(remaining, T - current_val)
#                  if can_add < average_time: 
#                      class_processing_times[i] += can_add
#                      remaining -=can_add
#                  # Vi tar en slumpmässig del av det vi 'kan' lägga till för bättre varians
#                  else: 
#                      add = truncated_poisson(average_time, can_add)
#                      class_processing_times[i] += add
#                      remaining -= add
                 
#     return class_processing_times

# def generate_number_of_jobs(n,c, class_processing_times): 
#     target_sum = n
#     average_num = n/c
#     num_jobs_in_each_class = [1]*c
#     remaining = target_sum - c
    
#     indices = list(range(c))
#     while remaining > 0: 
#         random.shuffle(indices)
#         for i in indices: 
#             if remaining <= 0: break
            
#             current_val = num_jobs_in_each_class[i]
#             upper_bound = class_processing_times[i]
#             if current_val < upper_bound:
#                 can_add = min(remaining, upper_bound-current_val)
#                 if can_add < average_num: 
#                     num_jobs_in_each_class[i]+= can_add
#                     remaining -=can_add
#                 else: 
#                     add = truncated_poisson(average_num, upper_bound)
#                     num_jobs_in_each_class[i] += add
#                     remaining -= add
                
#     return num_jobs_in_each_class

# def testgenerator(m, c, n): 
#     T = random.randint(np.ceil(m/n), 100) #kan ändra övre gränsen sen
#     print("Makespan: ", T)
#     jobs= []
    
#     class_processing_times = generate_class_processing_times(m, c, T)
#     num_jobs_in_each_class = generate_number_of_jobs(n, c, class_processing_times)
    
#     #slumpar processing time för varje jobb
#     for i in range(c): 
#         cuts_for_processingtimes = sorted(random.sample(range(1,class_processing_times[i]),num_jobs_in_each_class[i]-1))
#         prev = 0
#         for cut in cuts_for_processingtimes: 
#             jobs.append((cut-prev,i))
#             prev=cut
#         jobs.append((class_processing_times[i]-prev,i))
        
#     p = {}
#     classes = {k: [] for k in range(c)}
#     for j,(time,class_) in enumerate(jobs): 
#         p[j] = time
#         classes[class_].append(j)
#     print(n,p,m,classes)
#     return n,p,m,classes

m = 5 #Number of machines
c = 7 #Number of classes
n = 15 #Number of jobs
T = 100 #Optimal makespan

jobs= [] #jobs[i] --> (processing time,class) for job i, i = 0, ..., n-1
  
#class_process_times[c'] --> total processing time for class c'. c' = 0,...,c-1
class_process_times = distribute_sum_with_bounds(m*T, c, [T]*c)

#num_jobs_in_each_class[c'] --> number of jobs in class c', c' = 0,...,c-1
num_jobs_in_each_class = distribute_sum_with_bounds(n, c, class_process_times)

#slumpar processing time för varje jobb
# for i in range(c): 
#     cuts_for_processingtimes = sorted(random.sample(range(1,class_processing_times[i]),num_jobs_in_each_class[i]-1))
#     prev = 0
#     for cut in cuts_for_processingtimes: 
#         jobs.append((cut-prev,i+1))
#         prev=cut
#     jobs.append((class_processing_times[i]-prev,i+1))

for i in range(c): 
    class_time = class_process_times[i]
    num_jobs_in_class = num_jobs_in_each_class[i]
    job_process_times = distribute_sum_with_bounds(class_time, num_jobs_in_class, [class_time]*num_jobs_in_class)
    for j in range(num_jobs_in_class):
        jobs.append((job_process_times[j], i+1)) #In the test files, the class indexing starts on 1

np.random.shuffle(jobs)

print(m)
for job_time, job_class in jobs:
    print(job_time, job_class)


    
    
    
    
    
    
    