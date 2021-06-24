import gurobipy as gp
m = gp.Model("Knapsack ")

#Decision variables
#How much of item Xi to place in knapsack
X1 = m.addVar(lb=0,name="X1") #1
X2 = m.addVar(lb=0,name="X2") #2
X3 = m.addVar(lb=0,name="X3") #3
X4 = m.addVar(lb=0,name="X4") #4
X5 = m.addVar(lb=0,name="X5") #5
X6 = m.addVar(lb=0,name="X6") #6
X7 = m.addVar(lb=0,name="X7") #7
Profit = 7*X1+12*X2+4*X3+6*X4+10*X5+8*X6+5*X7

#Constraints
m.addConstr(2*X1+3*X2+4*X3+1*X4+2*X5+5*X6+1*X7 <= 25)

#Objective
#Minimize total time spent on tasks  (Connie  only)  Minimize sum
m.setObjective(Profit,gp.GRB.MAXIMIZE)

m.optimize() #solve it

var_store = m.getVars()
print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)
