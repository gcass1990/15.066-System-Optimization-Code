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

print("======================Part A===============")
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

print("===================Part B===========")
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
m.addRange(sum(cost[f] * buy[f] for f in foods), 0,12.5)
    
m.optimize()
printSolution(m)


# #### C)
# 
# Explain in words why the protein we get is lower in question B than it was in question A. Can you identify the budget we need to consume the maximum amount of protein? (either implement this, or just explain how you would do it)

# Answer C):
# 
# .
# 
