# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 14:58:31 2026

@author: idagu
"""
#t är en dict: [i] --> start time of i:th job, i = 0, ..., n-1
#m är antalet maskiner
#p är en dict: [i] --> duration of i:th job, i = 0, ..., n-1

def maskintilldelning(t, m, p):
    #Maskintilldelningsschemat
    sigma = {}
    
    #Totalbelastning på varje maskin
    p_m = {i: 0 for i in range(m)}
    
    #Sortera jobben efter starttid
    t_sorted = dict(sorted(t.items(), key=lambda item: item[1]))
    
    for j in t_sorted.keys():
        i = min(p_m, key=p_m.get) #maskinen med minst totalbelastning
        p_m[i] += p[j] #lägger till jobb till maskinen
        sigma[j] = i
    
    return (sigma)
        
        