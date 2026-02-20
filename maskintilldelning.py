# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 14:58:31 2026

@author: idagu
"""

jobs = [] #tom lista med jobb
p = {} #tom diconary med processing times, p[j]= pj
machines = [] #tom lista med maskiner
classes = {} #dictionary som mappar klasser till jobb

def maskintilldelning(t: dict[int,float], machines: list[int], p: dict[int, float]) -> tuple[dict[int,int]]:
    #Maskintilldelningsschemat
    sigma = {}
    
    p_m = {i: 0 for i in machines}
    
   # p_m = {} #tom dictionary med maskinernas nuvarande totalbelastning
    #Initiera totalbelastningen på varje maskin till 0
    #for i in machines: 
     #   p_m.add(i,0)
    
    #Sortera jobben efter starttid
    t_sorted = dict(sorted(t.items(), key=lambda item: item[1]))
    
    for j in t_sorted.keys():
        i = min(p_m, key=p_m.get) #maskinen med minst totalbelastning
        p_m[i] += p[j] #lägger till jobb till maskinen
        sigma[j] = i
    
    return (sigma)
        
        