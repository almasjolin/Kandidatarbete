#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 10:45:52 2026

@author: almasjolin
"""
# main.py
import gurobipy as gp
from gurobipy import GRB

#MODELL
#n är antalet jobb
#p är en dict: [i] --> duration of i:th job, i = 0, ..., n-1
#m är antalet maskiner
#classes är en dict: [c] --> list of id:s of jobs in class c, c = 1, ..., number of classes
def solve_ilp(n,p,m,classes):   
    model = gp.Model("MSRS")
    
    M = sum(p.values())#satte som summar av alla processingtimes
    epsilon = 0.05

    #VARIABLER

    #Starttider
    t = model.addVars(range(n), lb=0, vtype=GRB.CONTINUOUS, name="t")


    #Makespan
    T = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="T")


    #Binära varibaler
    x = {}  # xj,j'
    y = {}  # yj,j'
    z = {}  # zj,j'

    for j in range(n):#sätter binära variablerna x,y,z på varje par av jobb
        for j_prime in range(n):
            x[j, j_prime] = model.addVar(vtype=GRB.BINARY, name=f"x_{j}_{j_prime}")
            y[j, j_prime] = model.addVar(vtype=GRB.BINARY, name=f"y_{j}_{j_prime}")
            z[j, j_prime] = model.addVar(vtype=GRB.BINARY, name=f"z_{j}_{j_prime}")


    #CONSTRAINTS

    #Objective function
    model.setObjective(T, GRB.MINIMIZE)


    #Makespan contraints
    # Övre gräns på T, som mest M
    model.addConstr(T <= M, name="T_upper_bound")

    # T måste vara minst lika stor som slutiden för varje jobb
    for j in range(n):
        model.addConstr(t[j] + p[j] <= T, name=f"makespan_{j}")


    #x-constraints (implicerar att x_jj'=1 omm t_j'<=t_j)

    for j in range(n):
        for j_prime in range(n):
            # t_j' <= t_j + (1 - x_j,j')*M kallas constraint1 
            model.addConstr(
                t[j_prime] <= t[j] + (1 - x[j, j_prime]) * M,
                name=f"x_constraint1_{j}_{j_prime}"
            )
            
            # t_j + epsilon <= t_j' + x_j,j'*M, kallas constraint2
            model.addConstr(
                t[j] + epsilon <= t[j_prime] + x[j, j_prime] * M,
                name=f"x_constraint2_{j}_{j_prime}"
            )

    #y-constraints (implicerar att y_jj' = 1 omm t_j<=t_j' + p_j')

    for j in range(n):
        for j_prime in range(n):
            # t_j + epsilon <= t_j' + p_j' + (1 - y_j,j')*M, kallas constraint1 
            model.addConstr(
                t[j] + epsilon <= t[j_prime] + p[j_prime] + (1 - y[j, j_prime]) * M,
                name=f"y_constraint1_{j}_{j_prime}"
            )
            
            # t_j' + p_j' <= t_j + y_j,j'*M , kallas constraint2
            model.addConstr(
                t[j_prime] + p[j_prime] <= t[j] + y[j, j_prime] * M,
                name=f"y_constraint2_{j}_{j_prime}"
            )



    #z-contraints

    for j in range(n):
        for j_prime in range(n):
            # z_j,j' <= y_j,j'
            model.addConstr(
                z[j, j_prime] <= y[j, j_prime],
                name=f"z_constraint1_{j}_{j_prime}"
            )
            
            # z_j,j' <= x_j,j'
            model.addConstr(
                z[j, j_prime] <= x[j, j_prime],
                name=f"z_constraint2_{j}_{j_prime}"
            )
            
            # x_j,j' + y_j,j' - 1 <= z_j,j'
            model.addConstr(
                x[j, j_prime] + y[j, j_prime] - 1 <= z[j, j_prime],
                name=f"z_constraint3_{j}_{j_prime}"
            )


    #Maskin-constraint
    #Högst m jobb kan köras samtidigt
    for j in range(n):
        model.addConstr(
            gp.quicksum(z[j, j_prime] for j_prime in range(n)) <= m,
            name=f"machine_limit_{j}")

    #Resurs-constraint
    # Jobb i samma klass kan inte överlappa
    for class_name, class_jobs in classes.items():#för varje par av nyckel och värde i classes
        for j in class_jobs:#för varje par av jobb i classen
            for j_prime in class_jobs:
                if j != j_prime:  # Olika jobb i samma klass
                    model.addConstr(z[j, j_prime] == 0,
                        name=f"resource_conflict_{j}_{j_prime}")

    
    model.setParam("TimeLimit", 1800)

    model.optimize()
    

    if model.status == GRB.TIME_LIMIT:
        print("Time limit reached")
    if model.SolCount > 0:
        print(f"Best solution found with gap: {model.MIPGap:.2%}")
        t_sol = {j: t[j].X for j in range(n)}
        return T.X, t_sol
    else:
        print("No feasible solution found")
        return None, None
    










