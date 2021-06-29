#!/usr/bin/env python
# coding: utf-8

# ## HW1 - LP Formulations
# 
# In this first homework assignment we will work on 5 different LP forumulations in Gurobi. For each of them, a skeleton python code is provided, and you are tasked with filling in some additional bits and pieces. As a little help, the output of each cell is what it should be if you fill in the right code in each cell (where it is currently missing).

# In[1]:


import gurobipy as gp

# #### Problem 2
# 
# Consider the following problem Amazon may face (let's not kid ourselves: the variation Amazon faces is 100x more complex; but this is a simplified version): they have 4 different suppliers that each have some amount of inventory of a particular SKU. They also have 9 different orders for that SKU with individual fulfillment centers asking for one shipment of that SKU. Given the costs of shipping from each supplier to each fulfillment center, decide which supplier should ship to which fulfillment center, such that the resulting shipping costs are minimized.
# 
# (PS: yes, we're assuming that sending items fractionally will be allowed, at a fractional cost, for the purpose of this question! Though, it turns out, that that won't be an issue!)

# In[10]:


# Define supplier inventories
supplier_inventories = {'w1': 4, 'w2': 3, 'w3': 2, 'w4':3}
# the dictionary below holds the cost of shipping from each supplier to each center.
# We assume that the shipment costs are linear in the amount shipped,
supplier_center_cost = {'w1': [3, 5, 6, 2, 4, 6, 3, 6, 4],
                           'w2': [6, 5, 8, 3, 5, 6, 3, 5, 2],
                           'w3': [3, 5, 3, 2, 4, 7, 3, 6, 4],
                           'w4': [1, 4, 1, 4, 1, 8, 5, 1, 3]}
# e.g., the cost of one shipment from supplier 'w1' to the first center is 3
print(supplier_center_cost['w1'][0])

# whereas the cost of half a shipment from supplier 'w3' to the final center is 1/2*4=2
print(supplier_center_cost['w3'][8])

m = gp.Model("shipping")
shipments = {}

# Define decision variables to indicate for each supplier/center how much is shipped
for w in supplier_inventories:
    for center in range(9):
        wc = w+str(center) #name of the variable
        shipments[w,center] = m.addVar(name=wc)
print(len(shipments))
print(shipments)

total_cost = 0
# Next, we set our objective: minimizing the cost of all shipments
for item in shipments:
    w = item[0]
    center = item[1]
    specific_cost = supplier_center_cost[w][center]
    unit_cost = specific_cost*shipments[w,center]
    total_cost = total_cost + unit_cost
print(total_cost)

m.setObjective(total_cost,gp.GRB.MINIMIZE)

# Set a constraint that the amount of inventory shipped from a given supplier is at most its inventory
for w in supplier_inventories:
    sup_sum = sum(shipments[w,center] for center in range (9))
    print(sup_sum)
    m.addConstr(sup_sum <= supplier_inventories[w])  # Individual Inventory capacity


# Set a constraint that each center receives one shipment of inventory
for center in range(9):
    cent_sum = sum(shipments[w,center] for w in  supplier_inventories)
    m.addConstr(cent_sum == 1)

print("=============")
m.optimize()


# Below we print for each center the supplier from which the shipment ias made

# In[11]:


for center in range(9):
    for w in supplier_inventories:
        if shipments[w,center].x>0: print(w, center, supplier_center_cost[w][center])


