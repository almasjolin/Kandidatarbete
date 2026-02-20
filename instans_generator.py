# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 18:53:20 2026

@author: rebec
"""

import random
import numpy as np


def generate_instance():

    m = random.randint(10, 30) # slumpar antal maskiner
    T = random.randint(5, 100) # den totala tidsaxeln
    p_bar = random.randint(5, T) # styr jobblängd/ medelvärde för jobblängd

    alpha = {(i, t): -1 for i in range(m) for t in range(T)} # skapar en dictionary som representerar schemat
    C = {t: set() for t in range(T)} # för varje tidpunkt lagrar vi vilka klasser som är aktiva
    R = {(i, t) for i in range(m) for t in range(T)} # unassigned slots/(maskin, tid)-par
    J = []   # lista av (processing time, klass)

    def mex(S): # tar en mängd S av aktiva klasser vid givet tidsintervall och returnerar minsta positiva heltal som inte finns i S
        x = 1
        while x in S:
            x += 1
        return x

    while R: # så länge det finns lediga tidsrutor fortsätter vi

        (i, t) = random.choice(list(R)) # nytt jobb på slumpmässig plats
        l_prime = np.random.poisson(p_bar - 1) + 1 # slumpmässig jobblängd
        l = min(l_prime, T - t) # begränsar längden

        for k in range(t, t + l): # kontrollerar om platsen är ledig. Om inte kortar vi ner längden
            if alpha[(i, k)] != -1:
                l = k - t
                break

        if l == 0: # om ingen ledig tid kvar i sloten -> gå till nästa slumpade slot
            R.remove((i, t))
            continue

        active_classes = set() # hitta klass
        for r in range(t, t + l):
            active_classes |= C[r]

        c = mex(active_classes)

        J.append((l, c)) # skapar ett nytt jobb

        for k in range(t, t + l): # uppdaterar scshemat
            alpha[(i, k)] = c
            C[k].add(c)

        for k in range(t, t + l): # tar bort upptagen slot
            R.discard((i, k))


    jobs = list(range(len(J)))
    p = {}
    classes = {}

    for j, (length, c) in enumerate(J):
        p[j] = length
        if c not in classes:
            classes[c] = []
        classes[c].append(j)

    return jobs, p, m, classes

print(generate_instance())