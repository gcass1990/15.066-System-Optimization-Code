import gurobipy as gp
import csv


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
L = {}
index = 0
for i in range(1, len(input_data) + 1, 1):
    num_loops = input_data[i][0]  # number of times to append
    for j in range(num_loops):
        index = index + 1
        L[index] = input_data[i][1]

used = {}
print(used)
combos =[]
while used != L: #while the two dictionaries are not the same
    for item in L:
        #print(item,L[item])
        beam_used = L[item] + 0.5 #intialize the cut
        used[item] =L[item] # add item to dictionary
        new_combo = [item] #intialize the new combo
        combos.append(new_combo)
        new_combo2 = new_combo
        for item2 in L: #iterate over
            new_length = beam_used + L[item2] + 0.5 #add another beam
            if new_length <= 12005: #check if if this new cut set it over, if not, add it
                used_keys = used.keys() #list of keys
                if item2 not in used_keys:
                    new_combo2.append(item2)
                    print(new_combo2,new_length,item2)
                    used[item2] = L[item2]
                    beam_used = new_length
            else: # if it is over



        combos.append(new_combo2) #add the new list
print(combos)

