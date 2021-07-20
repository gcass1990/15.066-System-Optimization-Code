import gurobipy as gp
import csv

m = gp.Model("Part A")


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

    for i in range(0, len(L), 1):  # For each rod i
        rod_beam_name = "rod-" + str(i + 1) + "-beam-" + str(j + 1)  # create a name for the decision variable
        cut_rod_on_beam[(i, j)] = m.addVar(vtype=gp.GRB.BINARY, name=rod_beam_name)  # The rod is cut on the beam or not

        rod_length = L[i]  # length of rod for that specific cut
        beam_cut_length = (rod_length + 5) * cut_rod_on_beam[(i, j)] + beam_cut_length  # Length of cuts on the beam

        # Add a constraint that to cut the rod on the beam, the beam must be selected
        m.addConstr(use_beam[j] >= cut_rod_on_beam[i, j])

    # Add a constraint that  total length of cuts must be less than standard beam size
    m.addConstr(beam_cut_length <= 12005)


for j in range(1, len(L) - 1, 1):
    # Add  constraints that we only use beam j+1 if we have used beam j at all
    m.addConstr(use_beam[j] >= use_beam[j + 1])

#Add a constraint that the first beam to be used is beam 1
m.addConstr(use_beam[0] >= 1)

for i in range(0, len(L), 1):  # For each rod i
    rod_sum = 0
    for j in range(1, len(L) - 1, 1):  # for each beam
        rod_sum = rod_sum + cut_rod_on_beam[i, j]
    m.addConstr(rod_sum == 1)  # constraint that each rod is cut

# Set objective
m.setObjective(total_beam_num, gp.GRB.MINIMIZE)

m.optimize()

print("==========")
ans = {} #blank dictionary for answer
for v in m.getVars():
    print((v.varName, v.x))  # %s  = string format , %g = floating point format
    ans[v.varName]= v.x  #assign
print('Obj: %g' % m.objVal)

with open('dict.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in ans.items():
       writer.writerow([key, value])
