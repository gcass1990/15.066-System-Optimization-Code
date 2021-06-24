import gurobipy as gp
m = gp.Model("Wedding Planning - Min Flow ")

#Decision variables -> proportion of time spend on each task
C1 = m.addVar(lb=0,name="C1") #decision variable constraint, task1 time
P1 = m.addVar(lb=0,name="P1") #decision variable constraint, task1 time
J1 = m.addVar(lb=0,name="J1") #decision variable constraint, task1 time
C2 = m.addVar(lb=0,name="C2") #decision variable constraint, task2 time
P2 = m.addVar(lb=0,name="P2") #decision variable constraint, task2 time
J2 = m.addVar(lb=0,name="J2") #decision variable constraint, task2 time
C3 = m.addVar(lb=0,name="C3") #decision variable constraint, task3 time
P3 = m.addVar(lb=0,name="P3") #decision variable constraint, task3 time
J3 = m.addVar(lb=0,name="J3") #decision variable constraint, task3 time
C = m.addVar(lb=0,name="C") #decision variable constraint, C labor time
P = m.addVar(lb=0,name="P") #decision variable constraint, P labor time
J = m.addVar(lb=0,name="J") #decision variable constraint, J labor time

#For each worker (connie, philp), job

#Constraints
#All work must be completed
m.addConstr(40*C1+20*P1+30*J1 == 200) #Fold Invitations
m.addConstr(50*C2+10*P2+20*J2 == 125)  #RSVPs
m.addConstr(25*C3+10*P3+20*J3 == 150)  #Wrap wedding

#Time constraints
m.addConstr(C1+C2+C3 == C) #C
m.addConstr(P1+P2+P3 == P) #P
m.addConstr(J1+J2+J3 == J) #J
#Flow constraint = they must all work the same amount of time and they are always working 100%
m.addConstr(P==C)
m.addConstr(J==C)

#Objective
#Maximize utility
m.setObjective(C, gp.GRB.MINIMIZE)

m.optimize() #solve it

var_store = m.getVars()
print("==========")
for v in m.getVars():
    print('%s %g' % (v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)
