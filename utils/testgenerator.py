# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 13:02:04 2026

@author: idagu
"""
import random
import numpy as np

def generate_class_processing_times(m,c,T): 
    target_sum = m*T
    class_processing_times = [1]*c
    remaining = target_sum - c
    
    indices = list(range(c))
    while remaining > 0:
         random.shuffle(indices) # För att sprida ut värdena rättvist
         for i in indices:
             if remaining <= 0: break
             
             current_val = class_processing_times[i]
             if current_val < T:
                 # Lägg till så mycket som möjligt, men max upp till T
                 can_add = min(remaining, T - current_val)
                 # Vi tar en slumpmässig del av det vi 'kan' lägga till för bättre varians
                 add = random.randint(1, can_add)
                 class_processing_times[i] += add
                 remaining -= add
                 
    return class_processing_times

def generate_number_of_jobs(n,c, class_processing_times): 
    target_sum = n
    num_jobs_in_each_class = [1]*c
    remaining = target_sum - c
    
    indices = list(range(c))
    while remaining > 0: 
        random.shuffle(indices)
        for i in indices: 
            if remaining <= 0: break
            
            current_val = num_jobs_in_each_class[i]
            upper_bound = class_processing_times[i]
            if current_val < upper_bound:
                can_add = min(remaining, upper_bound-current_val)
                add = random.randint(1,can_add)
                num_jobs_in_each_class[i] += add
                remaining -= add
                
    return num_jobs_in_each_class

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

m = 5
c = 8
n = 15

T = random.randint(np.ceil(m/n), 100) #kan ändra övre gränsen sen
print("Makespan: ", T)
jobs= []
  
class_processing_times = generate_class_processing_times(m, c, T)
num_jobs_in_each_class = generate_number_of_jobs(n, c, class_processing_times)

#slumpar processing time för varje jobb
for i in range(c): 
    cuts_for_processingtimes = sorted(random.sample(range(1,class_processing_times[i]),num_jobs_in_each_class[i]-1))
    prev = 0
    for cut in cuts_for_processingtimes: 
        jobs.append((cut-prev,i))
        prev=cut
    jobs.append((class_processing_times[i]-prev,i))
    
p = {}
classes = {k: [] for k in range(c)}
for j,(time,class_) in enumerate(jobs): 
    p[j] = time
    classes[class_].append(j)

print(m)
for job_time, job_class in jobs:
    print(job_time, job_class)


    
    
    
    
    
    
    