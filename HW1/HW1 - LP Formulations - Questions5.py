#!/usr/bin/env python
# coding: utf-8

# ## HW1 - LP Formulations
# 
# In this first homework assignment we will work on 5 different LP forumulations in Gurobi. For each of them, a skeleton python code is provided, and you are tasked with filling in some additional bits and pieces. As a little help, the output of each cell is what it should be if you fill in the right code in each cell (where it is currently missing).

# In[1]:


import gurobipy as gp


# #### Problem 5
# 
# In this problem we try to find the optimal schedule of workers to different shifts in a store. Suppose our store is open 24/7, and the number of workers needed to staff the store is given below.

# In[20]:


staff_required = {0: 8, 1: 8, 2: 9, 3: 8, 4: 8, 5: 9, 
                  6: 10, 7: 12, 8: 12, 9: 12, 10: 10, 
                  11: 10, 12: 12, 13: 12, 14: 10, 15: 10,
                  16: 9, 17: 10, 18: 12, 19: 12, 20: 12,
                  21: 10, 22: 9, 23: 8}


# A worker scheduled to show up at a given time, stays for 4h. Find the number of workers to show up at each hour of the day that minimizes the total number of workers that need are needed over the course of the day while fulfilling the staff needs above.
# 
# Hint: the python function \% may be useful in coding up the constraints!

# In[21]:


# First, we define a variable that contains the optimization model
m = gp.Model("transactions")

# Second, let's create one variable for each hour in which a shift can start
starts = {}
for k in range(24):
    start=k
    stop=k+4
    if stop >23:
        stop = stop -24
    varname = "x"+str(start)+"-"+str(stop)
    print(varname)
    starts[k] = m.addVar(name=varname)
# Third, define the objective: the total number of workers needed
numworkers =  sum(starts[k] for k in starts) #
m.setObjective(numworkers,gp.GRB.MINIMIZE)

# Fourth, add a constraint for each hour that ensures that sufficiently
# many workers are scheduled to work at that hour.
for k in range(24):
    k2 =k -1 #started the last hour
    k3 = k-2 #started two hours ago
    k4 = k-3 #started three hours ago
    if k2 <0:
        k2 = k2+24
    if k3 <0:
        k3 =k3+24
    if k4 <0:
        k4 = k4 +24
    num_on_duty = starts[k] + starts[k2] +starts[k3] + starts[k4] #num_on_duty
    m.addConstr(num_on_duty >= staff_required[k]) # number on duty must be greater than that required

#optimize
m.optimize()


# In[22]:


for k in range(len(starts)): print(k, starts[k].x, staff_required[k])
