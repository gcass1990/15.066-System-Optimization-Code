#!/usr/bin/env python
# coding: utf-8




import gurobipy as gp

print("==============Primal =================")
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
c1 = m.addConstr(3*x+y+5*z<=10) # 3x + y + 5z<=10
c2 = m.addConstr(x+3*y<=12) # x + 3y<=12
c3 = m.addConstr(3*z>=6) # 3*z>=6

# Next, we set our objective: maximizing x+3y+2z
m.setObjective(x+3*y+2*z, gp.GRB.MAXIMIZE)

m.optimize()
print('Obj: %g' % m.objVal)
print(c1.pi, c2.pi, c3.pi)
print("====================DUAL=====================")
# Then we print the solution values for each variable
print(x.x,y.x,z.x)
print(c1.pi,c2.pi,c3.pi)

m2 = gp.Model("dual")
a = m2.addVar(lb = 0)
b = m2.addVar(lb = 0)
c = m2.addVar(lb=0)
d = m2.addVar(lb=0)
e= m2.addVar(lb=0)

#Constriants
c11 = m2.addConstr(a+3*c+d >= 1)
c12 = m2.addConstr(b+c+3*d >= 3)
c13 = m2.addConstr(5*c - e >= 2)

#Objective
m2.setObjective(10*a+10*b+10*c+12*d-2*e, gp.GRB.MINIMIZE)
#Run Analysis
m2.optimize()
print(a.x,b.x,c.x,d.x,e.x)
print(c11.pi,c12.pi,c13.pi)

print('Obj: %g' % m2.objVal)
