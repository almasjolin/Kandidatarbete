# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 14:58:31 2026

@author: idagu
"""

jobs = [] #tom lista med jobb
p = {} #tom diconary med processing times, p[j]= pj
machines = []
classes = {} #dictionary som mappar jobb till dess klass/resurs

def maskintilldelning(t: dict[int,float]) -> tuple[dict[int,int], dict[int,float]]:
    #Maskintilldelningsschemat
    sigma = {}
    
    p_m = {} #tom dictionary med maskinernas nuvarande totalbelastning
    #Initiera totalbelastningen på varje maskin till 0
    for i in machines: 
        p_m.add(i,0)
    
    #Sortera jobben efter starttid
    t_sorted = dict(sorted(t.items(), key=lambda item: item[1]))
    
    for j in t_sorted.keys():
        i = min(p_m, key=p_m.get) #maskinen med minst totalbelastning
        sigma.add(j,i)
    
    return (sigma,t)
        
        