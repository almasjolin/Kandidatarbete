#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 10:45:52 2026

@author: almasjolin
"""
# main.py
import gurobipy as gp
from gurobipy import GRB
import csv

#MODEL
#n is the number of jobs
#p is a dictionary: p[i] --> duration of i:th job, i = 0, ..., n-1
#m is the number of machines
#classes is a dictionary: classes[c] --> list of id:s of jobs in class c, c = 1, ...,K
def ilp_std(n,p,m,classes):   
    model = gp.Model("MSRS")
    
    M = sum(p.values())

    epsilon = 0.1

    #VARIABLES

    #Start times
    t = model.addVars(range(n), lb=0, vtype=GRB.CONTINUOUS, name="t")


    #Makespan
    T = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name="T")


    #Binary variables
    x = {}  # xj,j'
    y = {}  # yj,j'
    z = {}  # zj,j'

    for j in range(n):#defines the binary variables x,y,z for each pair of jobs
        for j_prime in range(n):
            x[j, j_prime] = model.addVar(vtype=GRB.BINARY, name=f"x_{j}_{j_prime}")
            y[j, j_prime] = model.addVar(vtype=GRB.BINARY, name=f"y_{j}_{j_prime}")
            z[j, j_prime] = model.addVar(vtype=GRB.BINARY, name=f"z_{j}_{j_prime}")


    #CONSTRAINTS

    #Objective function
    model.setObjective(T, GRB.MINIMIZE)


    #Makespan contraints
    # T <= M
    model.addConstr(T <= M, name="T_upper_bound")

    # T must be at least as large as the end time of each job
    for j in range(n):
        model.addConstr(t[j] + p[j] <= T, name=f"makespan_{j}")


    #x-constraints (implies that x_jj'=1 iff t_j'<=t_j)

    for j in range(n):
        for j_prime in range(n):
            # t_j' <= t_j + (1 - x_j,j')*M is called constraint1 
            model.addConstr(
                t[j_prime] <= t[j] + (1 - x[j, j_prime]) * M,
                name=f"x_constraint1_{j}_{j_prime}"
            )
            
            # t_j + epsilon <= t_j' + x_j,j'*M is called constraint2
            model.addConstr(
                t[j] + epsilon <= t[j_prime] + x[j, j_prime] * M,
                name=f"x_constraint2_{j}_{j_prime}"
            )

    #y-constraints (implies that y_jj' = 1 iff t_j<=t_j' + p_j')

    for j in range(n):
        for j_prime in range(n):
            # t_j + epsilon <= t_j' + p_j' + (1 - y_j,j')*M is called constraint1 
            model.addConstr(
                t[j] + epsilon <= t[j_prime] + p[j_prime] + (1 - y[j, j_prime]) * M,
                name=f"y_constraint1_{j}_{j_prime}"
            )
            
            # t_j' + p_j' <= t_j + y_j,j'*M is called constraint2
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


    #Machine constraints
    #At most m jobs can run in parallel
    for j in range(n):
        model.addConstr(
            gp.quicksum(z[j, j_prime] for j_prime in range(n)) <= m,
            name=f"machine_limit_{j}")

    #Resource constraints
    # Jobs in the same class cannot overlap
    for class_name, class_jobs in classes.items():
        for j in class_jobs:
            for j_prime in class_jobs:
                if j != j_prime:  # Different jobs in the same class
                    model.addConstr(z[j, j_prime] == 0,
                        name=f"resource_conflict_{j}_{j_prime}")

    
    #Will break if it runs for more than 10 min
    model.setParam("TimeLimit", 600)

    #DATA COLLECTION
    
    progress_data = []
    
    last_log_time = -5

    def callback(model, where): 
        nonlocal last_log_time
        
        if where == GRB.Callback.MIPSOL or where == GRB.Callback.MIP:
            
            if where == GRB.Callback.MIPSOL: 
                best_objective = model.cbGet(GRB.Callback.MIPSOL_OBJBST)
                best_bound = model.cbGet(GRB.Callback.MIPSOL_OBJBND)
                
            else: 
                best_objective = model.cbGet(GRB.Callback.MIP_OBJBST)
                best_bound = model.cbGet(GRB.Callback.MIP_OBJBND)
    
            run_time = model.cbGet(GRB.Callback.RUNTIME)
            
            #Save data every 5 seconds or when new solutions or lower bounds are found
            if best_objective < 10**15 and \
                (run_time - last_log_time >= 5 or \
                not progress_data or \
                best_objective != progress_data[-1]['Incumbent'] or \
                best_bound != progress_data[-1]['BestBound']):
    
                progress_data.append({
                    'Incumbent': best_objective, 
                    'BestBound': best_bound, 
                    'Time': run_time
                })
    
    
                last_log_time = run_time
            
            
    model.optimize(callback)
    
    fields = ['Time', 'Incumbent', 'BestBound']
    
    with open('progress_data.csv', 'w', newline= '') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        writer.writeheader()
        
        writer.writerows(progress_data)
    

    if model.status == GRB.TIME_LIMIT:
        print("Time limit reached")
    if model.SolCount > 0:
        print(f"Best solution found with gap: {model.MIPGap:.2%}")
        t_sol = {j: t[j].X for j in range(n)}
        return T.X, t_sol
    else:
        print("No feasible solution found")
        return None, None
    










