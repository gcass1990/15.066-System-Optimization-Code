import gurobipy as gp
m = gp.Model("Lecture2 Breakout ")

#Decision variables
#How much of cargo Xi to place in location l
X1F = m.addVar(lb=0,name="X1F") #Cargo 1 in front
X2F = m.addVar(lb=0,name="X2F") #Cargo 2 in front
X3F = m.addVar(lb=0,name="X3F") #Cargo 3 in front
X4F = m.addVar(lb=0,name="X4F") #Cargo 4 in front
X1C = m.addVar(lb=0,name="X1C") #Cargo 1 in center
X2C = m.addVar(lb=0,name="X2C") #Cargo 2 in center
X3C = m.addVar(lb=0,name="X3C") #Cargo 3 in center
X4C = m.addVar(lb=0,name="X4C") #Cargo 4 in center
X1R = m.addVar(lb=0,name="X1R") #Cargo 1 in rear
X2R = m.addVar(lb=0,name="X2R") #Cargo 2 in rear
X3R = m.addVar(lb=0,name="X3R") #Cargo 3 in rear
X4R = m.addVar(lb=0,name="X4R") #Cargo 4 in rear
Profit = 310*(X1F+X1R+X1C)+380*(X2F+X2R+X2C)+350*(X3R+X3C+X3F)+285*(X4R+X4C+X4F) #Profit equation

#Constraints
#Individual compartments
m.addConstr(18*X1F+15*X2F+23*X3F+12*X4F <= 220) #Front Weight Constraint
m.addConstr(18*X1C+15*X2C+23*X3C+12*X4C <= 260) #Center Weight Constraint
m.addConstr(18*X1R+15*X2R+23*X3R+12*X4R <= 160) #Rear Weight Constraint
m.addConstr(480*X1F+650*X2F+580*X3F+390*X4F <= 6800) #Front Volume Constraint
m.addConstr(480*X1C+650*X2C+580*X3C+390*X4C <= 8700) #Center Volume Constraint
m.addConstr(480*X1R+650*X2R+580*X3R+390*X4R <= 5300) #Rear Volume Constraint

#Proportionality constraints
m.addConstr((18*X1F+15*X2F+23*X3F+12*X4F)/220 == (18*X1C+15*X2C+23*X3C+12*X4C)/ 260 ) # Front and Center proportionality must be same
m.addConstr((18*X1F+15*X2F+23*X3F+12*X4F)/220 == (18*X1R+15*X2R+23*X3R+12*X4R)/ 160)

#Objective
#Minimize total time spent on tasks  (Connie  only)  Minimize sum
m.setObjective(Profit,gp.GRB.MAXIMIZE)

m.optimize() #solve it

var_store = m.getVars()
print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)
