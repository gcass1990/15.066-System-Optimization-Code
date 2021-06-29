#!/usr/bin/env python
# coding: utf-8

# ## HW1 - LP Formulations
# 
# In this first homework assignment we will work on 5 different LP forumulations in Gurobi. For each of them, a skeleton python code is provided, and you are tasked with filling in some additional bits and pieces. As a little help, the output of each cell is what it should be if you fill in the right code in each cell (where it is currently missing).

# In[1]:


import gurobipy as gp



# #### Problem 4
# 
# The next question is based on a problem I (DF) myself consulted on. The industry partner I worked with operates a large online platform with millions of transactions every day. In order to process all the payments, the company partners with 2 different financial providers. In a nutshell, the providers have different cost structures for processing each payment. The goal of this optimization problem is to decide which payments to send to which provider.
# 
# - Provider A charges a proportional fee that is 2\% of the cost of the transaction, and requires the average payment routed to them to have a transaction value of at least 8\$
# - Provider B charges a fixed fee of \$.20 per payment
# 
# Below is a skeleton of a linear program that decides for each transaction which provider to send it to. Fill in the objective and the constraint (for provider A).

# In[14]:


# The list below has all transactions for one day.
Transactions = [5, 10, 14, 20, 6, 12, 16, 10, 8, 9, 12, 15]
num_transactions = len(Transactions)


# In[18]:


# First, we define a variable that contains the optimization model
m = gp.Model("transactions")

# Second, we add decision variables that capture for each 
# transaction which provider we send it to. A good way of doing this is
# by creating a variable that is either 0 or 1, where 0 indicates it is being 
# sent to A and 1 indicates it is being sent to B.
provider = {}
for k in range(num_transactions):
    provider[k] = m.addVar(lb=0,ub=1,name=str(k))
print(provider)

# Third, you need to add a constraint that ensures that the average value 
# of transactions sent to provider A is at least $8. This is tricky!
numA = sum(provider[k] for k in provider)
sumA = sum(provider[k]*Transactions[k] for k in provider)
AvgA = 8
#print(numA)
#print(sumA)
m.addConstr(sumA >= AvgA*numA)


# Last, define the objective. This is also not so easy:
# You want a term for each provider that contributes
# .02*transactions[k]  and .2 if provider[k]=1
b_pay = 0.20*(num_transactions-numA)
a_pay = sum(0.02*provider[k]*Transactions[k] for k in provider)
final_pay = b_pay+a_pay

m.setObjective(final_pay,gp.GRB.MINIMIZE)
m.optimize()

print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)
