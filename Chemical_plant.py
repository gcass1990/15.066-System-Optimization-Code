import gurobipy as gp
m = gp.Model("ChemicalPlant ")

#Decision variables
#How much of cargo Xi to place in location l
N11 = m.addVar(lb=4,name="N11") # starting Monday night
N12 = m.addVar(lb=4,name="N12") #
N13 = m.addVar(lb=4,name="N13") #
N14 = m.addVar(lb=4,name="N14") #
N15 = m.addVar(lb=4,name="N15") #
N16 = m.addVar(lb=4,name="N16") #
N17 = m.addVar(lb=4,name="N17") #
N21 = m.addVar(lb=4,name="N21") # starting Monday DAY
N22 = m.addVar(lb=4,name="N22") #
N23 = m.addVar(lb=4,name="N23") #
N24 = m.addVar(lb=4,name="N24") #
N25 = m.addVar(lb=4,name="N25") #
N26 = m.addVar(lb=4,name="N26") #
N27 = m.addVar(lb=0,name="N27") #
N31 = m.addVar(lb=0,name="N31") # starting Monday late
N32 = m.addVar(lb=0,name="N32") #
N33 = m.addVar(lb=0,name="N33") #
N34 = m.addVar(lb=0,name="N34") #
N35 = m.addVar(lb=0,name="N35") #
N36 = m.addVar(lb=0,name="N36") #
N37 = m.addVar(lb=0,name="N37") #


#Constraints
m.addConstr(N11+N12+N13+N14+N15+N16+N17+ N21+N22+N23+N24+N25+N26+N27 + N31+N32+N33+N34+N35+N36+N37 <= 60) # total capacity
#Monday Night
m.addConstr(N11 +N15+N16+N17 >= 5)
#etc

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