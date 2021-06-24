import gurobipy as gp
m = gp.Model("ChemicalPlant ")

#Decision variables
#How much of product to make on each machine
XY1 = m.addVar(lb=0,name="XY1") # X made on machine 1
X2 = m.addVar(lb=0,name="X2") #
X3 = m.addVar(lb=0,name="X3") #
X4 = m.addVar(lb=0,name="X4") #
Y2 = m.addVar(lb=0,name="Y2") #
Y3 = m.addVar(lb=0,name="Y3") #
Y4 = m.addVar(lb=0,name="Y4") #
Profit = 10*(XY1)+12*(X2+Y2)+17*(X3+Y3)+8*(X4+Y4)

#Constraints
m.addConstr(0.1*(XY1)+0.15*(X2+Y2)+0.5*(X3+Y3)+0.05*(X4+Y4) <= 50) # square footage requirement
m.addConstr((X3+Y3)*2 == (X2+Y2)) # Make 2 times amount of 3 as of 2
m.addConstr(10*XY1+12*X2+13*X3+8*X4 <= 35*60*0.95) # production time limit for machine X
m.addConstr(27*XY1+19*X2+33*X3+23*X4 <= 35*60*0.93) # production time limit for machine Y

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