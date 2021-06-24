import gurobipy as gp
m = gp.Model("Wedding Planning - Min Labor ")

#Decision variables -> time each worker spends on each task. Number of each task each worker completes
A = m.addVar(lb=0,name="A")
B = m.addVar(lb=0,name="B")
C = m.addVar(lb=0,name="C")
D = m.addVar(lb=0,name="D")
E = m.addVar(lb=0,name="E")
F = m.addVar(lb=0,name="F")
G = m.addVar(lb=0,name="G")
H = m.addVar(lb=0,name="H")
Profit = 49.5*A +50*B+61*C+63.5*D+66.5*E+F*71+G*72.5+80.0*H

#Constraints
#Cant do negative work. All work must be completed
m.addConstr(A<=300)  #Individual Capacity
m.addConstr(B<=600)  #Individual Capacity
m.addConstr(C<=510)  #Individual Capacity
m.addConstr(D<=655)  #Individual Capacity
m.addConstr(E<=575)  #Individual Capacity
m.addConstr(F<=680)  #Individual Capacity
m.addConstr(G<=450)  #Individual Capacity
m.addConstr(H<=490)  #Individual Capacity
m.addConstr(A+B+C+D+E+F+G+H == 1225)  #Total Capacity
m.addConstr(A*0.15+B*0.16+C*0.18+D*0.20+E*0.21+F*0.22+G*0.23+H*0.25 >= 1225*0.19) #Voltaility
m.addConstr(A+C+E+F <= 650) #Truck
m.addConstr(B+D+E+F <= 720) #Rail
m.addConstr(A+B+D+F >= C+E+G+H) #Union


#Objective
#Minimize total time spent on tasks  (Connie  only)  Minimize sum
m.setObjective(Profit,gp.GRB.MAXIMIZE)

m.optimize() #solve it

var_store = m.getVars()
print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)
