import gurobipy as gp
m = gp.Model("dual")
#Decision Variables
x1 = m.addVar(lb=0,name="x1")
x2 = m.addVar(lb =0,name="x2")
x3 = m.addVar(lb =0,name="x3")

#Constraints
c1=m.addConstr(x1<= 4)
c2=m.addConstr(x2 <=4)
c3=m.addConstr(x1+x2<=6)
c4=m.addConstr(-x1+2*x3<=4)
m.setObjective(2*x1+x2+x3,gp.GRB.MAXIMIZE) #Objective function
m.optimize() #solve it

print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)

print("============Dual==========")
#The new right hand side
print(c1.pi,c2.pi,c3.pi,c4.pi)
dual_c = [c1.pi,c2.pi,c3.pi,c4.pi] #Shadow prices
b = [4,4,6,4]
sum = 0
for i in range(len(b)):
    sum = sum+b[i]*dual_c[i]
print(sum)
dual_c_RHS_sensitivity= [c1.SARHSUp,c2.SARHSUp,c3.SARHSUp,c4.SARHSUp]
print(dual_c_RHS_sensitivity)