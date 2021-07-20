import gurobipy as gp
import csv

m = gp.Model("Heuristic - cut each rod on its own beam ")


def import_data(file_name):
    data_dict = {}  # empty dictionary
    with open(file_name, "r") as opened_file:
        dict_reader = csv.DictReader(opened_file)  #
        i = 1  # index
        for row in dict_reader:
            data_dict[i] = [int(row['Number of pieces']), float(row['Length in mm'])]  # put the data in there
            i = i + 1
    opened_file.close()
    return data_dict


file_name = "Rod_cutting_input.csv"

input_data = import_data(file_name)
print(input_data)

# Create the L Matrix
L = []
for i in range(1, len(input_data) + 1, 1):
    num_loops = input_data[i][0]  # number of times to append
    for j in range(num_loops):
        L.append(input_data[i][1])

use_beam = {}  # Do we use beam j
cut_rod_on_beam = {}  # Do we cut rod i on beam j
total_beam_num = 0  # Intalize total number of beams used

for j in range(0, len(L), 1):  # for each beam j
    beam_name = "beam-" + str(j + 1)  # create a name for the decision variable
    use_beam[j] = m.addVar(vtype=gp.GRB.BINARY, name=beam_name)  # do i use the beam or not
    total_beam_num = total_beam_num + use_beam[j]  # update total number of beams term

    beam_cut_length = 0  # Intalize the beam cut length to zero
    sum_of_cuts = 0  # intialize the sum of cuts to be zero

    for i in range(0, len(L), 1):  # For each rod i
        rod_beam_name = "rod-" + str(i + 1) + "-beam-" + str(j + 1)  # create a name for the decision variable
        cut_rod_on_beam[(i, j)] = m.addVar(vtype=gp.GRB.BINARY, name=rod_beam_name)  # The rod is cut on the beam or not

        rod_length = L[i]  # length of rod for that specific cut
        beam_cut_length = (rod_length + 5) * cut_rod_on_beam[(i, j)] + beam_cut_length  # Length of cuts on the beam

        sum_of_cuts = sum_of_cuts + cut_rod_on_beam[i, j]  # Sum of cuts on that specific beam

        # Add a constraint that to cut the rod on the beam, the beam must be selected
        m.addConstr(use_beam[j] >= cut_rod_on_beam[i, j])

    # Add a constraint that  total length of cuts must be less than standard beam size
    m.addConstr(beam_cut_length <= 12005)

    # Add a constraint that sum of cuts must be 1 (i.e. every rod get its own beam)
    m.addConstr(sum_of_cuts >= 1)

for j in range(1, len(L) - 1, 1):
    # Add  constraints that we only use beam j+1 if we have used beam j at all
    m.addConstr(use_beam[j] >= use_beam[j + 1])

for i in range(0, len(L), 1):  # For each rod i
    rod_sum = 0
    for j in range(1, len(L) - 1, 1):  # for each beam
        rod_sum = rod_sum + cut_rod_on_beam[i, j]
    m.addConstr(rod_sum == 1)  # constraint that the rod is cut

# Set objective
m.setObjective(total_beam_num, gp.GRB.MINIMIZE)

m.optimize()

print("==========")
for v in m.getVars():
    print((v.varName, v.x))  # %s  = string format , %g = floating point format

print('Obj: %g' % m.objVal)

print("===============Model 2 =========")
m2 = gp.Model("Determine the optimal using a warm start  ")

use_beam2 = {}  # Do we use beam j
cut_rod_on_beam2 = {}  # Do we cut rod i on beam j
total_beam_num2 = 0  # Intalize total number of beams used

for j in range(0, len(L), 1):  # for each beam j
    beam_name2 = "beam-" + str(j)  # create a name for the decision variable
    use_beam2[j] = m2.addVar(vtype=gp.GRB.BINARY, name=beam_name2)  # do i use the beam or not
    total_beam_num2 = total_beam_num2 + use_beam2[j]  # update total number of beams term
    use_beam2[j].start = use_beam[j].x  # warm start

    beam_cut_length2 = 0  # Intalize the beam cut length to zero
    sum_of_cuts2 = 0  # intialize the sum of cuts to be zero

    for i in range(0, len(L), 1):  # For each rod i
        rod_beam_name2 = "rod-" + str(i + 1) + "-beam-" + str(j + 1)  # create a name for the decision variable
        cut_rod_on_beam2[(i, j)] = m2.addVar(vtype=gp.GRB.BINARY,
                                             name=rod_beam_name2)  # The rod is cut on the beam or not
        cut_rod_on_beam2[(i, j)].start = cut_rod_on_beam[(i, j)].x  # warm start

        rod_length2 = L[i]  # length of rod for that specific cut
        beam_cut_length2 = (rod_length + 5) * cut_rod_on_beam2[(i, j)] + beam_cut_length2  # Length of cuts on the beam

        # Add a constraint that to cut the rod on the beam, the beam must be selected
        m2.addConstr(use_beam2[j] >= cut_rod_on_beam2[i, j])

    # Add a constraint that  total length of cuts must be less than standard beam size
    m2.addConstr(beam_cut_length2 <= 12005)

for j in range(1, len(L) - 1, 1):  # for each beam
    # Add  constraints that we only use beam j+1 if we have used beam j at all
    m2.addConstr(use_beam2[j] >= use_beam2[j + 1])

for i in range(0, len(L), 1):  # For each rod i
    rod_sum2 = 0
    for j in range(1, len(L) - 1, 1):  # for each beam
        rod_sum2 = rod_sum2 + cut_rod_on_beam2[i, j]
    m2.addConstr(rod_sum2 == 1)  # constraint that the rod is cut

# Set objective
m2.setObjective(total_beam_num2, gp.GRB.MINIMIZE)

m2.optimize()

print("==========")
for v in m2.getVars():
    print((v.varName, v.x))  # %s  = string format , %g = floating point format

print('Obj: %g' % m2.objVal)
