import gurobipy as gp
m = gp.Model("dual")
#Decision Variables
A1 = m.addVar(lb=0,name="A1")
A2 = m.addVar(lb =0,name="A2")
B1 = m.addVar(lb =0,name="B1")
B2 = m.addVar(lb =0,name="B2")
C1 = m.addVar(lb =0,name="C1")
C2 = m.addVar(lb =0,name="C2")
D1 = m.addVar(lb =0,name="D1")
D2 = m.addVar(lb =0,name="D2")


#Constraints
c1=m.addConstr(A1+A2 <= 40)
c2=m.addConstr(B1+B2 <= 30)
c3=m.addConstr(C1+C2 <= 30)
c4=m.addConstr(D1+D2 <= 48)
c5=m.addConstr(20*A1+20*B1+45*C1+5*D1<=960)
c6=m.addConstr(15*A2+25*B2+30*C2+10*D2<=960)

#Objective function
m.setObjective(8*(A1+A2)+7*(B1+B2)+15*(C1+C2)+8*(D1+D2),gp.GRB.MAXIMIZE)
m.optimize() #solve it

print("==========")
for v in m.getVars():
    print((v.varName, v.x, v.RC,v.SAObjUp)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)
print("========DUAL==========")
#The new right hand side
print(c1.pi,c2.pi,c3.pi,c4.pi,c5.pi, c6.pi)

dual_c = [c1.pi,c2.pi,c3.pi,c4.pi,c5.pi, c6.pi]
b = [40,30,30,10,960,960]
sum = 0
for i in range(len(b)):
    sum = sum+b[i]*dual_c[i]
print(sum)
dual_c_RHS_sensitivity= [c1.SARHSLow,c2.SARHSLow,c3.SARHSLow,c4.SARHSLow,c5.SARHSLow, c6.SARHSLow]
dual_c_RHS_sensitivity= [c1.SARHSUp,c2.SARHSUp,c3.SARHSUp,c4.SARHSUp,c5.SARHSUp, c6.SARHSUp]
print(dual_c_RHS_sensitivity)