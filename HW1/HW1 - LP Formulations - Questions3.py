#!/usr/bin/env python
# coding: utf-8

# ## HW1 - LP Formulations
#
# In this first homework assignment we will work on 5 different LP forumulations in Gurobi. For each of them, a skeleton python code is provided, and you are tasked with filling in some additional bits and pieces. As a little help, the output of each cell is what it should be if you fill in the right code in each cell (where it is currently missing).

# In[1]:


import gurobipy as gp

# #### Problem 3
#
# In this question we need to decide on a production schedule for a factory. The factory is tasked with producing 3 different goods, and it has 3 different machines; each machine can be tasked to work on any of the goods, but machines are faster at producing some goods than they are at others. Our goal is to minimize the time until all our orders are fulfilled.
#
# In the cell below we provide you with the data for the problem:

# In[12]:


# we have products 'p1', 'p2', 'p3', and we need to
# produce (respectively) 100, 200, 400 units of each
product_demand = {'p1': 100, 'p2': 200, 'p3': 400}
machines = ['m1', 'm2', 'm3']
# we have three machines, 'm1', 'm2', and 'm3' and
# the number of products of each type that can be produced
# by each of the machines is given in the dictionary below
machine_speed = {('m1','p1'):2, ('m1','p2'):1, ('m1','p3'):3,
                 ('m2','p1'):2, ('m2','p2'):2, ('m2','p3'):4.5,
                 ('m3','p1'):2, ('m3','p2'):3, ('m3','p3'):4}
# e.g., machine 'm1' can produce 2 units of type 'p1' but only
# 1 unit of type 'p2' per hour


# Hint: In setting up your optimization problem it will be useful to define 10 different variables: 9 for each pair of machine and product ("how many hours does machine i spend on product j?"), and 1 for the objective ("what is the maximum time any of the machines is working?"), which we refer to as makespan.

# In[13]:


m = gp.Model("production_schedule")

time_spent = {}
# First add a decision variable capturing the time each machine spends on each product
for machine,p in machine_speed:
    dv_name = machine+"-"+p #create a name
    print(dv_name)
    time_spent[(machine,p)] =  m.addVar(name=dv_name)
print(len(time_spent))

# Next, add constraints to ensure we spend enough time (by respective machines) on 
# each product so that enough units of each products are completed
for p in product_demand:
    #quantity = time_spent * production rate
    quantity = 0 #initialize the quantity
    for machine in machines:
        quantity = quantity+ machine_speed[(machine,p)]*time_spent[(machine, p)] #update the quantity term
    m.addConstr(quantity == product_demand[p]) #greater than

makespan = m.addVar(lb=0)   # makespan will be the objective, the maximum time any
                            # machine works in total. Notice that lb is the lower bound
                            # on a variable, so we do not allow the makespan to be negative

# Add a constraint that the makespan variable is no less than the time each 
# machine spends individually
for machine in ['m1', 'm2', 'm3']:
    machinetime = 0 #Initialize the variable
    for p in product_demand:
        machinetime = machinetime + time_spent[(machine, p)] #update the term
    print(machine,machinetime)
    m.addConstr(makespan >= machinetime) #NO LESS THAN
     
        
# Finally, set the objective to be the minimization of the makespan. 
m.setObjective(makespan,gp.GRB.MINIMIZE)

# Since we have only constrained the makespan to be bounded below by the time spent by any 
# of 'm1', 'm2', 'm3' (and nothing else), and since the objective should minimize the 
# makespan, the optimal  solution will have the makespan be equal to the maximum of 
# time spent by any of the machines. Specifically, there is no reason (constraint) 
# forcing the makespan variable to be any larger than the maximum total time spent, 
# and the minimization objective is "pushing" it down until one of the inequalities 
# holds with equality.


m.optimize()

for x in time_spent:
    if time_spent[x].x>0:
        print("""Machine %s works on product %s for %g hours, producing %g units"""%(x[0],
                                            x[1], time_spent[x].x,
                                            machine_speed[x]*time_spent[x].x))