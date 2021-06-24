#https://ocw.mit.edu/courses/sloan-school-of-management/15-053-optimization-methods-in-management-science-spring-2013/tutorials/MIT15_053S13_tut01.pdf

import gurobipy as gp
m = gp.Model("MachineProducts ")

#Decision variables
#How much of product to make on each machine
P = m.addVar(lb=0,name="P") #
Q = m.addVar(lb=0,name="Q") #
R = m.addVar(lb=0,name="R") #

#Constraints
m.addConstr(20*P+10*Q+10*R <= 2400) #Machine A limits
m.addConstr(12*P+28*Q+16*R <= 2400) #Machine B Limits
m.addConstr(15*P+6*Q+16*R <= 2400) #Machine C limits
m.addConstr(10*P+15*Q<= 2400) #Machine D limits
m.addConstr(P<=100)
m.addConstr(Q<=40)
m.addConstr(R<=60)
Profit = 45*P+Q*60+50*R-6000

# Product 1 must be produced on both machines X and Y but products 2, 3 and 4 can be produced on either machine.
#etc

#Objective
#Minimize total time spent on tasks  (Connie  only)  Minimize sum
m.setObjective(Profit,gp.GRB.MAXIMIZE)

m.optimize() #solve it

var_store = m.getVars()
print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)

#Confirmed accuracy here
#https://www.mikenicely.com/can/