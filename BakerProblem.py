import gurobipy as gp

a = gp.Model("Cake Selling ")
#BUtter = $5 profit, 90 lbs max, 6 minutes per pound to make , 3 minutes per pound of labor
#Sponge = $5, 60 lbs max, 4.5 minutes per pound to make, 6 minutes per pounds of sponge dou

#Decision variables
#Production quantities
S = a.addVar(lb=0,ub = 90, name="S") #decision variable constraint
B = a.addVar(lb= 0,ub = 60, name="B") #decision variable constraint

#Constriants
#Mixing
a.addConstr(6*B+4.5*S <= 465) #amount of mixer time available
#Labor
a.addConstr(3*B+6*S <= 420) #Amount of labor available in a day

#Objective
#Maximize profit
a.setObjective(5*B+6*S,gp.GRB.MAXIMIZE)
a.optimize()

print("==========")
for v in a.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % a.objVal)