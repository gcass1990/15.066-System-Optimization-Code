#!/usr/bin/env python
# coding: utf-8




import gurobipy as gp
m = gp.Model("facility location with service installation costs")

# These lists contain the facilities, the services, and the customers
facilities = ['f1', 'f2', 'f3']
services = ['s1', 's2', 's3', 's4']
customers = ['c1', 'c2', 'c3','c4','c5','c6', 'c7']

# the cost of opening any one facility are as follows
facility_opening_costs = {'f1': 13, 'f2': 15, 'f3': 12}

# Below are the costs of installing a service in an opened facility
# Notice that it's given in a so-called "nested dictionary"; the cost of installing service
# s3 at facility f1 is service_installation_costs['f1']['s3'] which turns out
# to be 1 (in this example)
service_installation_costs = {'f1': {'s1':2, 's2':4, 's3':1, 's4':2},
                              'f2': {'s1':1, 's2':1, 's3':1, 's4':0},
                              'f3': {'s1':2, 's2':4, 's3':1, 's4':2}}

# For each customer, the below dictionary captures what service they require
customer_service_needs = {'c1': 's1', 'c2': 's1', 'c3': 's2',
                          'c4':'s2', 'c5':'s3', 'c6': 's3', 'c7':'s4'}

# For each pair of customer and facility, this nested dictionary captures
# the cost of connecting facility f and customer c. so
# facility_customer_assignment_costs['f3']['c4'] would give the cost of
# connecting facility 3 and customer 4 (in this case: 6)
facility_customer_assignment_costs = {'f1': {'c1':4, 'c2':4, 'c3':3, 'c4':4, 'c5':5, 'c6':7, 'c7':8},
                                     'f2': {'c1':4, 'c2':4, 'c3':3, 'c4':4, 'c5':5, 'c6':7, 'c7':8},
                                     'f3': {'c1':5, 'c2':2, 'c3':1, 'c4':6, 'c5':15, 'c6':6, 'c7':7}
                                     }

#Get the number of  facilities, customers, servceices for looping
nf =len(facilities)
nc= len(customers)
ns = len(services)

#Set up Decision Variables and cost coeficients with those decision variables
decision_vars = {} #intialize
total_cost = 0
for i in facilities:
    for j in services:
        for k in customers:
            dv_name = i+"-"+j+"-"+k
            decision_vars[(i,j,k)] = m.addVar(lb=0,ub=1,vtype=gp.GRB.INTEGER, name=dv_name) #This path is chosen or not

            #Calculate cost of making this decision
            open_cost = facility_opening_costs[i]
            ass_cost = facility_customer_assignment_costs[i][k]
            serv_cost =service_installation_costs[i][j]
            decision_cost = open_cost +  ass_cost + serv_cost

            #Add to the total cost, which will be minimized
            total_cost = total_cost + (decision_cost)*decision_vars[(i,j,k)]

#print(decision_vars)
print(len(decision_vars))
print(total_cost)

#Set up constraints that service must be captured
for k in customers:  #for each customer
    service_provided = 0
    j = customer_service_needs[k] #determine the service need
    for i in facilities:   #make sure it comes from 1 of the facilities
        #print(i,j,k)
        service_provided = service_provided+decision_vars[(i,j,k)]
    #print(service_provided)
    m.addConstr(service_provided == 1)

m.setObjective(total_cost,gp.GRB.MINIMIZE)

m.optimize()
print("==========")
for v in m.getVars():
    print((v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)