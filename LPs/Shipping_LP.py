#http://people.brunel.ac.uk/~mastjjb/jeb/or/lpmore.html
import gurobipy as gp
m = gp.Model("Shipping")

#Decision variables
#How much of cargo Xi to place in location l
S1A = m.addVar(lb=0,name="S1A") #Cargo 1 in front
S2A = m.addVar(lb=0,name="S2A") #Cargo 2 in front
S3A = m.addVar(lb=0,name="S3A") #Cargo 3 in front
S1B = m.addVar(lb=0,name="S1B") #Cargo 4 in front
S2B = m.addVar(lb=0,name="S2B") #Cargo 1 in center
S3B = m.addVar(lb=0,name="S3B") #Cargo 2 in center
Revenue = 50*(S1A+S2A+S3A+S1B+S2B+S3B)
PurchaseCost  = (S1A+S1B)*11 +(S2A+S2B)*10+(S3A+S3B)*9
ShippingCost = (S1A)*3 + S2A*2+S3A*6 +S1B*3.5 +S2B*2.5+S3B*4
LaborCost = (S1A+S2A+S3A)*26 + (S1B+S2B+S3B)*21
TotalCost = PurchaseCost + ShippingCost + LaborCost
Profit = Revenue - TotalCost

#Constraints
#Individual compartments
m.addConstr(S1A+S1B <= 200)#S1 total amount limit #supply constraint
m.addConstr(S2A+S2B <= 310)#S2 total amount limit
m.addConstr(S3A+S3B <= 420)#S3 total amount limit
m.addConstr(S1A+S2A + S3A  <= 460)#Plant A limit
m.addConstr(S1B+S2B + S3B  <= 560)#Plant B limit

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