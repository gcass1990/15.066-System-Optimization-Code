#!/usr/bin/env python
# coding: utf-8




import gurobipy as gp

print("==============Sensitivity Analysis  =================")
# First, we define a variable that contains the optimization model
m = gp.Model("primal")

# Next, we define the three decision variables with their respective lower and upper bounds
x = m.addVar(lb = 0) # 0<= x
y = m.addVar(lb = 0) # 0<= y
z = m.addVar(lb=-gp.GRB.INFINITY) # z can be anything

# Then, we give bounds on x and y being at most 10, respectively 12
bound_x = m.addConstr(x<=10)
bound_y = m.addConstr(y<=12)

# Then, we add the other constraints
c1 = m.addConstr(3*x+y+5*z<=11) # This constraint is increased by 1!
c2 = m.addConstr(x+3*y<=12) # x + 3y<=12
c3 = m.addConstr(3*z>=6) # 3*z>=6

# Next, we set our objective: maximizing x+3y+2z
m.setObjective(x+3*y+2*z, gp.GRB.MAXIMIZE)

m.optimize()
print('Obj: %g' % m.objVal)
