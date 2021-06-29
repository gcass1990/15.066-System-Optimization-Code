#!/usr/bin/env python
# coding: utf-8

# ## HW1 - LP Formulations
# 
# In this first homework assignment we will work on 5 different LP forumulations in Gurobi. For each of them, a skeleton python code is provided, and you are tasked with filling in some additional bits and pieces. As a little help, the output of each cell is what it should be if you fill in the right code in each cell (where it is currently missing).

# In[1]:


import gurobipy as gp


# ### Problem 1
# 
# Problem 1 in this assignment is a "classical first linear programming problem": a diet optimization problem. We are given different types of food, that each come with a (financial) cost and with nutritional information (amount of calories, protein, fat, and sodium). In addition, we are told in what limits our nutritional intake should be for each of the nutrients (e.g., at least 91g of protein).
# 
# Below, I will walk you through the optimization problem that aims to minimize the financial cost of the food items we consume whilst guaranteeing that we are within the limits of calories,protein, fat, and sodium.

# In[2]:


# This first cell just defines the different nutrients, the healthy limits 
# of each nutrient, and the cost/nutrients of each food item.

categories, minNutrition, maxNutrition = gp.multidict({
    'calories': [1800, 2200],
    'protein':  [91, gp.GRB.INFINITY],
    'fat':      [0, 65],
    'sodium':   [0, 1779]})

foods, cost = gp.multidict({
    'hamburger': 2.49,
    'chicken':   2.89,
    'hot dog':   1.50,
    'fries':     1.89,
    'macaroni':  2.09,
    'pizza':     1.99,
    'salad':     2.49,
    'milk':      0.89,
    'ice cream': 1.59})

# Nutrition values for the foods #Dictionary
nutritionValues = {
    ('hamburger', 'calories'): 410,
    ('hamburger', 'protein'):  24,
    ('hamburger', 'fat'):      26,
    ('hamburger', 'sodium'):   730,
    ('chicken',   'calories'): 420,
    ('chicken',   'protein'):  32,
    ('chicken',   'fat'):      10,
    ('chicken',   'sodium'):   1190,
    ('hot dog',   'calories'): 560,
    ('hot dog',   'protein'):  20,
    ('hot dog',   'fat'):      32,
    ('hot dog',   'sodium'):   1800,
    ('fries',     'calories'): 380,
    ('fries',     'protein'):  4,
    ('fries',     'fat'):      19,
    ('fries',     'sodium'):   270,
    ('macaroni',  'calories'): 320,
    ('macaroni',  'protein'):  12,
    ('macaroni',  'fat'):      10,
    ('macaroni',  'sodium'):   930,
    ('pizza',     'calories'): 320,
    ('pizza',     'protein'):  15,
    ('pizza',     'fat'):      12,
    ('pizza',     'sodium'):   820,
    ('salad',     'calories'): 320,
    ('salad',     'protein'):  31,
    ('salad',     'fat'):      12,
    ('salad',     'sodium'):   1230,
    ('milk',      'calories'): 100,
    ('milk',      'protein'):  8,
    ('milk',      'fat'):      2.5,
    ('milk',      'sodium'):   125,
    ('ice cream', 'calories'): 330,
    ('ice cream', 'protein'):  8,
    ('ice cream', 'fat'):      10,
    ('ice cream', 'sodium'):   180}


# In[3]:


nutritionValues[('milk','fat')]


# We use this data below when we define our optimization problem.

# In[5]:


# First, we define a variable that contains the optimization model
m = gp.Model("diet1")

# Second, we add decision variables to the model that capture for each 
# food item the quantity bought
buy = {}
for f in foods:
    buy[f] = m.addVar(name=f)

# Third, we set our objective: minimizing the cost of the food
m.setObjective(sum(buy[f]*cost[f] for f in foods), gp.GRB.MINIMIZE)

# Fourth, we set constraints that enforce for each nutrition category
# (calories, protein, fat, sodium) that we be in the feasible range
for c in categories:
    m.addRange(sum(nutritionValues[f, c] * buy[f] for f in foods), 
               # this sum captures the amount of each nutrient
               minNutrition[c], # this is the lower bound (from the data)
               maxNutrition[c], # this is the upper bound (from the data)
               c) # this is the name for the constraint 
        # a name is not required but it is a good habit to 
        # give each variable/constraint a unique name
        
# We could have written the constraints also by writing
# m.addConstr(sum(nutritionValues[f, c] * buy[f] for f in foods) >= minNutrition[c])
# and
# m.addConstr(sum(nutritionValues[f, c] * buy[f] for f in foods) <= maxNutrition[c])
# We will see situations below in which this notation is easier to write.


# That's it. Probably that was not that hard, right? 
# 
# Now we can tell Gurobi to find us an optimal solution. When Gurobi solves, it gives us a lot of information that we may not care about (at least, not right now). So before solving, we define a function that ends up printing the interesting bits of the optimal solution for us.

# In[10]:


def printSolution(m):
    if m.status == gp.GRB.OPTIMAL:
        buyx = m.getAttr('x', buy)
        print('Cost: %g' %(sum(cost[f] * buyx[f] for f in foods)))
        print('\nNutrients:')
        for c in categories:
            print('%s %g'%(c, sum(buyx[f]*nutritionValues[f,c] for f in foods)))
        print('\nBuy:')
        for f in foods:
            if buy[f].x > 0.0001:
                print('%s %g' % (f, buyx[f]))
        
    else:
        print('No solution')


# In[11]:


# Now we solve, and get a bunch of info we don't necessarily understand
# If we want to stop gurobi from printing that info wee can add 
# m.setParam( 'OutputFlag', False ) to the code to stop Gurobi from printing
m.optimize()


# In[12]:


# Now we print the interesting aspects of our solution:
printSolution(m)


# I hope everything above has made sense. If not, feel free to reach out to any of the teaching staff for gurobi questions or to Valerie for python questions (or cc all of us). 
# 
# #### A) 
# Below, we will try to set up a slightly different optimization problem. Now, rather than aiming to minimize cost, we try to build muscle, i.e., we need to maximize our protein intake. The cell below has most of the protein maximization model written out (same as above), with only the objective missing. Add the new objective to the optimization problem and have gurobi solve it.

# In[15]:


# First, we define a variable that contains the optimization model
m = gp.Model("diet2")

# Second, we add decision variables to the model that capture for each 
# food item the quantity bought
buy = {}
for f in foods:
    buy[f] = m.addVar(name=f)

# Third, we set our objective: maximizing the amount of protein in our diet.
#Cass key changes: change from cost to protein, change from minimize to maximize 
#nutritionValues[('milk','fat')]
m.setObjective(sum(buy[f]*nutritionValues[(f,'protein')] for f in foods), gp.GRB.MAXIMIZE) 
                                          
# Fourth, we set constraints that enforce for each nutrition category 
# (calories, protein, fat, sodium) that we be in the feasible range
for c in categories: # 
    m.addRange(sum(nutritionValues[f, c] * buy[f] for f in foods), # again: amount of each nutrient
               minNutrition[c], # again: lower bound (from the data)
               maxNutrition[c], # again: upper bound (from the data)
               c) # name for constraint
m.optimize()
printSolution(m)


# #### B) 
# Similar to part (A), we still want to maximize our protein intake. However, we now have an added budget constraint: our cost can be at most 12.5. Write out and solve this new optimization problem (you should be able to copy-paste the cell from question A, and add just one line with the new budget constraint).

# In[17]:


# First, we define a variable that contains the optimization model
m = gp.Model("diet3")

# Second, we add decision variables to the model that capture for each 
# food item the quantity bought
buy = {}
for f in foods:
    buy[f] = m.addVar(name=f)

# Third, we set our objective as in part A: maximizing the amount of protein in our diet.
m.setObjective(sum(buy[f]*nutritionValues[(f,'protein')] for f in foods), gp.GRB.MAXIMIZE) 

# Fourth, we set constraints that enforce for each nutrition category
# (calories, protein, fat, sodium) that we be in the feasible range
for c in categories: # 
    m.addRange(sum(nutritionValues[f, c] * buy[f] for f in foods), # again: amount of each nutrient
               minNutrition[c], # this is the lower bound (from the data)
               maxNutrition[c], # this is the upper bound (from the data)
               c) # this is the name for the constraint

# Finally, you need to add a constraint that bounds the cost of items bought by 12.5
for f in foods: # 
    m.addRange(sum(nutritionValues[f, c] * buy[f] for f in foods), # again: amount of each nutrient
               minNutrition[c], # this is the lower bound (from the data)
               maxNutrition[c], # this is the upper bound (from the data)
               c) # this is the name for the constraint

    
m.optimize()
printSolution(m)


# #### C)
# 
# Explain in words why the protein we get is lower in question B than it was in question A. Can you identify the budget we need to consume the maximum amount of protein? (either implement this, or just explain how you would do it)

# Answer C):
# 
# .
# 
# .
# 
# .

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
# whereas the cost of half a shipment from supplier 'w3' to the final center is 1/2*4=2
m = gp.Model("shipping")
shipments = {}

# Define decision variables to indicate for each supplier/center how much is shipped
for w in supplier_inventories:
    for center in range(9):
        shipments[w,center] = 
        
# Next, we set our objective: minimizing the cost of all shipments


# Set a constraint that the amount of inventory shipped from a given supplier is at most its inventory
for w in supplier_inventories:

# Set a constraint that each center receives one shipment of inventory
for center in range(9):

    
m.optimize()


# Below we print for each center the supplier from which the shipment ias made

# In[11]:


for center in range(9):
    for w in supplier_inventories:
        if shipments[w,center].x>0: print(w, center, supplier_center_cost[w][center])


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
    time_spent[(machine,p)] =  
# Next, add constraints to ensure we spend enough time (by respective machines) on 
# each product so that enough units of each products are completed
for p in product_demand:
     
    
makespan = m.addVar(lb=0)   # makespan will be the objective, the maximum time any
                            # machine works in total. Notice that lb is the lower bound
                            # on a variable, so we do not allow the makespan to be negative

# Add a constraint that the makespan variable is no less than the time each 
# machine spends individually
for machine in ['m1', 'm2', 'm3']:
     
        
# Finally, set the objective to be the minimization of the makespan. 

# Since we have only constrained the makespan to be bounded below by the time spent by any 
# of 'm1', 'm2', 'm3' (and nothing else), and since the objective should minimize the 
# makespan, the optimal  solution will have the makespan be equal to the maximum of 
# time spent by any of the machines. Specifically, there is no reason (constraint) 
# forcing the makespan variable to be any larger than the maximum total time spent, 
# and the minimization objective is "pushing" it down until one of the inequalities 
# holds with equality.


m.optimize()

print("The optimal schedule is:")
for x in time_spent:
    if time_spent[x].x>0:
        print("""Machine %s works on product %s for %g hours, producing %g units"""%(x[0], 
                                            x[1], time_spent[x].x, 
                                            machine_speed[x]*time_spent[x].x))


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
    provider[k] = m.addVar(lb=0,ub=1)
    
# Third, you need to add a constraint that ensures that the average value 
# of transactions sent to provider A is at least $8. This is tricky!


# Last, define the objective. This is also not so easy:
# You want a term for each provider that contributes 
# .02*transactions[k] if provider[k]=0 and .2 if provider[k]=1



m.optimize()


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

# Third, define the objective: the total number of workers needed

    
# Fourth, add a constraint for each hour that ensures that sufficiently
# many workers are scheduled to work at that hour.
for k in range(24):

m.optimize()


# In[22]:


for k in range(len(starts)): print(k, starts[k].x, staff_required[k])

