import gurobipy as gp
m2 = gp.Model("Recitation ")

#Decision Variables
#How many units to produce of each family
F1 = m2.addVar(lb = 0,name = "F1")
F2= m2.addVar(lb = 0,name = "F2")
F3= m2.addVar(lb=0,name = "F3")

#Should we even make it
X1 = m2.addVar(name = "X1",vtype=gp.GRB.BINARY)
X2= m2.addVar(name = "X2",vtype=gp.GRB.BINARY)
X3= m2.addVar(name = "X3",vtype=gp.GRB.BINARY)

#Constraints
#Department
c1 = m2.addConstr(3*F1+4*F2+8*F3 <= 2000)
c2 = m2.addConstr(3*F1+5*F2+6*F3 <= 2000)
c3 = m2.addConstr(2*F1+3*F2+9*F3 <= 2000)

#Demand
c4 = m2.addConstr(F1 <= 300*X1)
c5 = m2.addConstr(F2 <= 200*X2)
c6 = m2.addConstr(F3 <= 50*X3)


#Maximize Profit
profit = (1.2*F1+1.8*F2+2.2*F3) - 60*X1 - 200*X2 - 100*X3
# Set objective
m2.setObjective(profit,gp.GRB.MAXIMIZE)

m2.optimize()
print("==========")
for v in m2.getVars():
    print((v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m2.objVal)