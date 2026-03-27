# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 14:58:31 2026

@author: idagu
"""
#t is a dictionary: t[i] --> start time of i:th job, i = 0, ..., n-1
#m is the number of machines
#p is a dictionary: p[i] --> duration of i:th job, i = 0, ..., n-1

def machine_assignment(t, m, p):
    #Machine assignment schedule
    sigma = {}
    
    #Total load on each machine
    C = {i: 0 for i in range(m)}
    
    #Sort the jobs based on start times
    t_sorted = dict(sorted(t.items(), key=lambda item: item[1]))
    
    for j in t_sorted.keys():
        i = min(C, key=C.get) #The machines with least total load
        C[i] += p[j] #Add the job to the machine
        sigma[j] = i
    
    return (sigma)
        
        