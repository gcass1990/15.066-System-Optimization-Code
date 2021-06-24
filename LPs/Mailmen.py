import gurobipy as gp
m = gp.Model("Wedding Planning")

#Decision variables -> time each worker spends on each task. Number of each task each worker completes
X1 = m.addVar(lb=0,name="X1")
X2 = m.addVar(lb=0,name="X2")
X3 = m.addVar(lb=0,name="X3")
X4 = m.addVar(lb=0,name="X4")
X5 = m.addVar(lb=0,name="X5")
X6 = m.addVar(lb=0,name="X6")
X7 = m.addVar(lb=0,name="X7")
z = X1+X2+X3+X4+X5+X6+X7

#Constraints
#Cant do negative work. All work must be completed
m.addConstr(X1+X2+X3+X4+X5 >= 17 ) #Monday
m.addConstr(X2+X3+X4+X5+X6 >= 13 ) #T
m.addConstr(X3+X4+X5+X6+X7>= 15 ) #W
m.addConstr(X1+X4+X5+X6+X7>= 19 ) #Th
m.addConstr(X1+X2+X5+X6+X7>= 14 ) #F
m.addConstr(X1+X2+X3+X6+X7>= 16 ) #Sat
m.addConstr(X1+X2+X3+X4+X7>= 11 ) #Sun


#Objective
#Minimize total time spent on tasks  (Connie  only)  Minimize sum
m.setObjective(z,gp.GRB.MINIMIZE)

m.optimize() #solve it

var_store = m.getVars()
print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)
