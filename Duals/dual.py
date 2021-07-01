import gurobipy as gp
m = gp.Model("dual")
#Decision Variables
x = m.addVar(lb=0,name="x")
y = m.addVar(lb =0,name="y")
z = m.addVar(lb =0,name="z")

#Constraints
c1=m.addConstr(x+y+z <= 14)
c2=m.addConstr(2*x+2*z <=12)
c3=m.addConstr(y+z<=10)
c4=m.addConstr(2*y+z<=22)
m.setObjective(3*x+5*y+4*z,gp.GRB.MAXIMIZE) #Objective function
m.optimize() #solve it

print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)

#The new right hand side
print(c1.pi,c2.pi,c3.pi,c4.pi)
dual_c = [c1.pi,c2.pi,c3.pi,c4.pi]
b = [14,12,10,22]
sum = 0
for i in range(len(b)):
    sum = sum+b[i]*dual_c[i]
print(sum)
