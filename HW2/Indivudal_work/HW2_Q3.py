#!/usr/bin/env python
# coding: utf-8




import gurobipy as gp
m = gp.Model("Shipping")

shipping_cost = {('1','4'):5 , ('1','5'):10, ('1','6'):11,
                 ('2','6'):9 , ('2','7'):9,
                 ('3','5'):8 , ('3','8'):7,
                ('4','9'):17 , ('5','12'):10,('6','9'):11 , ('6','10'):10,
                ('7','10'):12 , ('7','11'):13,('8','11'):11 , ('8','12'):14  }


demand = {'9': 30, '10': 50, '11':60,'12':60}
supply = {'1': 90, '2': 40, '3':70}

#Create decision variables
decision_vars = {}
for item in shipping_cost:
    dv_name = item[0]+"-"+item[1]
    decision_vars[(item[0],item[1])] =  m.addVar(lb=0, name=dv_name)

#Create Objective Function
totalcost = 0 #intialize
for item in shipping_cost:
    route_cost = decision_vars[(item[0],item[1])]*shipping_cost[(item[0],item[1])]
    totalcost =totalcost+route_cost
print(totalcost)
m.setObjective(totalcost,gp.GRB.MINIMIZE)

#Supply constraint
ONE_supply, TWO_supply,THREE_SUPPLY =0,0,0 #intialize
NINE_Demand,TEN_Demand,ELEVEN_Demand,TWELVE_Demand =0,0,0,0 #intialize
for item in shipping_cost:
    if int(item[0]) == 1:
        ONE_supply = ONE_supply + decision_vars[(item[0],item[1])]
    if int(item[0]) == 2:
        TWO_supply = TWO_supply + decision_vars[(item[0],item[1])]
    if int(item[0]) == 3:
        THREE_SUPPLY = THREE_SUPPLY + decision_vars[(item[0],item[1])]
    if int(item[1]) == 9:
        NINE_Demand = NINE_Demand + decision_vars[(item[0],item[1])]
    if int(item[1]) == 10:
        TEN_Demand = TEN_Demand + decision_vars[(item[0],item[1])]
    if int(item[1]) == 11:
        ELEVEN_Demand = ELEVEN_Demand + decision_vars[(item[0],item[1])]
    if int(item[1]) == 11:
        TWELVE_Demand = TWELVE_Demand + decision_vars[(item[0],item[1])]

#Supply Constraints
c1 = m.addConstr(ONE_supply == supply['1'])
c2 = m.addConstr(TWO_supply == supply['2'])
c3 = m.addConstr(THREE_SUPPLY == supply['3'])

#Demand Constraints
c4= m.addConstr(NINE_Demand == demand['9'])
c5 = m.addConstr(TEN_Demand == demand['10'])
c6 = m.addConstr(ELEVEN_Demand == demand['11'])
c7 = m.addConstr(TWELVE_Demand == demand['12'])

FOUR_IN, FIVE_IN,SIX_IN,SEVEN_IN,EIGHT_IN = 0,0,0,0,0
FOUR_OUT, FIVE_OUT,SIX_OUT,SEVEN_OUT,EIGHT_OUT = 0,0,0,0,0
for item in shipping_cost:
    if int(item[0]) == 4:
        FOUR_IN = FOUR_IN + decision_vars[(item[0],item[1])]
    if int(item[0]) == 5:
        FIVE_IN = FIVE_IN + decision_vars[(item[0],item[1])]
    if int(item[0]) == 6:
        SIX_IN = SIX_IN + decision_vars[(item[0],item[1])]
    if int(item[0]) == 7:
        SEVEN_IN = SEVEN_IN + decision_vars[(item[0],item[1])]
    if int(item[0]) == 8:
        EIGHT_IN = EIGHT_IN + decision_vars[(item[0],item[1])]
    if int(item[1]) == 4:
        FOUR_OUT = FOUR_OUT + decision_vars[(item[0],item[1])]
    if int(item[1]) == 5:
        FIVE_OUT= FIVE_OUT + decision_vars[(item[0],item[1])]
    if int(item[1]) == 6:
        SIX_OUT = SIX_OUT + decision_vars[(item[0],item[1])]
    if int(item[1]) == 7:
        SEVEN_OUT = SEVEN_OUT + decision_vars[(item[0],item[1])]
    if int(item[1]) == 8:
        EIGHT_OUT = EIGHT_OUT + decision_vars[(item[0],item[1])]

#IN-Out Constraints
c8 = m.addConstr(FOUR_IN == FOUR_OUT)
c9 = m.addConstr(FIVE_IN == FIVE_OUT)
c10 = m.addConstr(SIX_IN == SIX_OUT)
c11 = m.addConstr(SEVEN_IN == SEVEN_OUT)
c12 = m.addConstr(EIGHT_IN == EIGHT_OUT)
m.optimize()

print("==========")
for v in m.getVars():
    print((v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)

print("==============")
print(c2.pi, c2.SARHSLow,c2.SARHSUp)
#Therefore if we can increase it up to 80 without changing the solution
#For each unit we add, we increase cost by 18
#Original solution =m Obj: 3890
#If we change the supply to 60 --> expect 18*20 = 360 cost increase
#New objective = 4250       4250-360 = 3890 Voila
print("==============")
#Constraint that enforces amount of inventory in the warehouse is non-negative
print(c8.pi, c9.pi,c10.pi,c11.pi,c12.pi)
#Effective cost of using that warehouse this is why #4 and $ 12 have nothing going to them