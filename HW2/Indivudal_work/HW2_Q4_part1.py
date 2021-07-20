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

#Set up Decision Variables
open_fac = {} #intailize, holds decision about whether or not to open facility
decision_vars = {} #intailize, holds decision about whether or not to connect customer, service, facility
open_serv = {} #intailize, holds decision about whether or not to open facility

#Cost Variables for the objective Function
open_cost = 0 #initialize, cost of openning a facility
connection_cost = 0 #intialize, cost of making a connection with a customer and facility
serv_cost = 0 #itnialize, the cost of installing a service at the facility.
total_cost = 0 #intialize, total cost



for i in facilities:
    open_fac[i] = m.addVar(lb=0, ub=1, vtype=gp.GRB.INTEGER, name=i)  # This facility is opened or not
    open_cost = open_cost + facility_opening_costs[i] * open_fac[i]    #the cost of opening a facility

    for j in services:
        open_serv[(i,j)] = m.addVar(lb=0, ub=1, vtype=gp.GRB.INTEGER, name=i+j)  # This service is installed at a service or not
        serv_cost = serv_cost + open_serv[(i,j)]*service_installation_costs[i][j] # the cost of installing a service

        for k in customers:
            dv_name = i+"-"+j+"-"+k #this is just a name
            decision_vars[(i,j,k)] = m.addVar(lb=0,ub=1,vtype=gp.GRB.INTEGER, name=dv_name) #This path is chosen or not

            #print(i,j,k, serv_cost,ass_cost)
            connection_cost = connection_cost + (facility_customer_assignment_costs[i][k]*decision_vars[(i,j,k)]) # cost of connecting

            #Add constraint that can only make the connection if the facility is open
            #3*7*4 = 84 constraints total
            m.addConstr(open_fac[i] >=decision_vars[(i,j,k)])

            # Add a constraint that you can only serve a customer if the service is open
            m.addConstr(open_serv[(i, j)]>= decision_vars[(i,j,k)])

total_cost=  open_cost +connection_cost + serv_cost
#print(decision_vars)
#print(len(decision_vars))
#print(total_cost)

#Set up constraints that service must be provided to the customer from one of the three facilities
#7 constraints total
for k in customers:  #for each customer
    service_provided = 0
    j = customer_service_needs[k] #determine the service need
    for i in facilities:   #make sure it comes from 1 of the facilities
        #print(i,j,k)
        service_provided = service_provided+decision_vars[(i,j,k)]
    #print(service_provided)
    m.addConstr(service_provided == 1)

# Set objective
m.setObjective(total_cost,gp.GRB.MINIMIZE)

m.optimize()
print("==========")
for v in m.getVars():
    print((v.varName, v.x)) #%s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)