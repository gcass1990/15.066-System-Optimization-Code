import gurobipy as gp
m = gp.Model("firstLP")
x = m.addVar(lb=0,ub=15,name="x") #decision variable constraint
y = m.addVar(lb = -gp.GRB.INFINITY,ub=gp.GRB.INFINITY,name="y") #decision variable constraint
m.addConstr(x+3*y<= 10) #constraints with interacting variables
m.addConstr(2*x+y >= 0) #constraints with interacting variables
m.setObjective(x+y,gp.GRB.MINIMIZE) #Objective function
m.optimize() #solve it

var_store = m.getVars()
print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)
