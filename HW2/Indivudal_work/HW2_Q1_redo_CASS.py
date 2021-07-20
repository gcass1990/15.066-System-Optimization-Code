#!/usr/bin/env python
# coding: utf-8




import gurobipy as gp
m = gp.Model("Product Mix and profit Max ")

net_prof = {('0','0'):480- (30+110+260) , ('1','0'):500-(20+100+260), ('2','0'):520-(60+90+260),
                 ('0','1'):480-(35+110+210), ('1','1'):500-(25+100+210), ('2','1'):520-(40+90+210)}
maxunits = {'0': 460, '1': 560}

decision_vars = {}
for i in range (3): # products
    for j in range(2): # of plans ( 0 = south, 1 = central)
        decision_vars[(i,j)] =  m.addVar(lb=0, name=str(i)+str(j))
print(len(decision_vars))

#Unit Cost and Revenue Cost
total_netprof = 0
for i in range(3):
    for j in range(2):
            total_netprof = total_netprof+ decision_vars[(i,j)]*net_prof[(str(i),str(j))]

m.setObjective(total_netprof,gp.GRB.MAXIMIZE)

print("============Add capacity constraints==========")
for j in range(2):
    maxprod = 0
    capacity = maxunits[str(j)]
    for i in range(3):
        maxprod = maxprod + decision_vars[(i, j)]
    m.addConstr(maxprod <= capacity)

m.optimize()

print("==========")
for v in m.getVars():
    print((v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)