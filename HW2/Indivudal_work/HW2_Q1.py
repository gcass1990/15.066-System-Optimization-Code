#!/usr/bin/env python
# coding: utf-8




import gurobipy as gp
m = gp.Model("Product Mix and profit Max ")

cost = {'0': 110, '1': 100, '2': 90}
revenue = {'0': 480, '1': 500, '2': 520}
shipping_cost = {('0','0'):30+110 , ('1','0'):20, ('2','0'):60,
                 ('0','1'):35, ('1','1'):25, ('2','1'):40}

maxunits = {'0': 460, '1': 560}
labor_cost = {'0': 260, '1': 210}

decision_vars = {}
for i in range (3): # products
    for j in range(2): # of plans ( 0 = south, 1 = central)
        for k in range(3): # o distributors
            decision_vars[(i,j,k)] =  m.addVar(lb=0, name=str(i)+str(j)+str(k))
print(len(decision_vars))

#Unit Cost and Revenue Cost
total_unit_cost = 0
total_revenue = 0
for i in range(3):
    unit_revenue = revenue[str(i)] #unit revenue for that product
    unit_cost = cost[str(i)] #unit cost for that product
    for j in range(2):
        for k in range(3):
            total_unit_cost = total_unit_cost+ decision_vars[(i,j,k)]*unit_cost
            total_revenue = total_revenue+ decision_vars[(i,j,k)]*unit_revenue
print(total_unit_cost)
print(total_revenue)

print("=========Shipping Cost =========")
#Shipping cost
total_shipcost=0
for i in range (3):
    for j in range(2):
        unit_ship_cost = shipping_cost[(str(i),str(j))]
        for k in range (3):
            total_shipcost = total_shipcost+ decision_vars[(i,j,k)]*unit_ship_cost
print(total_shipcost)

print("=========Labor Cost =========")
#Labor Cost
total_labor_cost = 0
for j in range(2):
    plant_labor = labor_cost[str(j)]
    for i in range(3):
        for k in range(3):
            total_labor_cost = total_labor_cost+ decision_vars[(i,j,k)]*plant_labor
print(total_labor_cost)

Profit = total_revenue - (total_unit_cost+ total_shipcost+total_labor_cost)
m.setObjective(Profit,gp.GRB.MAXIMIZE)

print("============Add capacity constraints==========")
for j in range(2):
    maxprod = 0
    capacity = maxunits[str(j)]
    for i in range(3):
        for k in range(3):
            maxprod = maxprod + decision_vars[(i, j, k)]
    print(capacity,maxprod)
    m.addConstr(maxprod <= capacity)

m.optimize()

print("==========")
for v in m.getVars():
    print((v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)