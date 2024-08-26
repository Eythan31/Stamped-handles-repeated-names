# -*- coding: utf-8 -*-
import numpy as np, random, statistics
from matplotlib import pyplot as plt

n = 80 # Number of bearers of seals and bullae 
m = 27 # Number of bearers of private jar-stamps
k = 1000000 # Number of samples of size k among the set of size n (seals&bullae)
ENFORCE_DIFFERENT_SUBSETS = False #Use False for a faster enumeration.
SEALS_BULLAE_FILE = 'seals-bullae.csv'
HANDLES_FILE = 'handles.csv'

def random_combination(iterable, r):
    "Random selection from itertools.combinations(iterable, r)"
    pool = tuple(iterable)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)

def take_subset(data, subset_indexes):
    return [data[i] for i in subset_indexes]    
    
def read_data(filename):
    all_pairs = []
    f = open(filename,'r')
    for line in f.readlines():
        line = line.rstrip()
        (a,b) = line.split(',')
        all_pairs.append((a,b))
    return all_pairs

# Number of repeated names
def count_nbr_repeated_names(comb): 
    repeated_names = []
    for i in range(0, len(comb)) :
        for j in range(i+1, len(comb)):
            seal1 = comb[i]
            seal2 = comb[j]
            if seal1[0] == seal2[0] or seal1[0] == seal2[1] :
                repeated_names.append(seal1[0])
            elif seal1[1] == seal2[0] or seal1[1] == seal2[1]:
                repeated_names.append(seal1[1])
    return len(set(repeated_names))

#Number of persons  with repeated names
def count_persons_with_rep_names(comb):
    persons = []
    for i in range(0, len(comb)) :
        for j in range(i+1, len(comb)):
            seal1 = comb[i]
            seal2 = comb[j]
            if seal1[0] == seal2[0] or seal1[0] == seal2[1] or \
                seal1[1] == seal2[0] or seal1[1] == seal2[1]:
                if not i in persons:
                    persons.append(i)
                if not j in persons:
                    persons.append(j)
    return len(persons)

# Number of repeated pairs (PN1=PN1 or PN2=PN2 or PN1=PN2 or PN2=PN1)
def count_repeated_pairs(comb): 
    count = 0
    for i in range(0, len(comb)) :
        for j in range(i+1, len(comb)):
            seal1 = comb[i]
            seal2 = comb[j]
            if seal1[0] == seal2[0] or seal1[0] == seal2[1] or \
                seal1[1] == seal2[0] or seal1[1] == seal2[1]:
                count = count+1
    return count

# Number of homonyms (PN1=PN1)
def count_homonyms(comb): 
    count = 0
    for i in range(0, len(comb)) :
        for j in range(i+1, len(comb)):
            seal1 = comb[i]
            seal2 = comb[j]
            if seal1[0] == seal2[0]:
                count = count+1
    return count

# Number of potential siblings (PN2=PN2)
def count_potential_siblings(comb): 
    count = 0
    for i in range(0, len(comb)) :
        for j in range(i+1, len(comb)):
            seal1 = comb[i]
            seal2 = comb[j]
            if seal1[1] == seal2[1]:
                count = count+1
    return count

# Number of potential father-son relations (PN1=PN2 or PN2=PN1)
def count_potential_genealogical_relations(comb): 
    count = 0
    for i in range(0, len(comb)) :
        for j in range(i+1, len(comb)):
            seal1 = comb[i]
            seal2 = comb[j]
            if seal1[0] == seal2[1] or seal1[1] == seal2[0]:               
                count = count+1
    return count
    
def print_plot(data, n, m, k, target, xlabel):
    LABEL_OFFSET = 3
    bins = np.arange(-100, 100, 1) # fixed bin size
    if(len(data) >0) :
        plt.xlim([min(data)-5, max(data)+5])
    plt.hist(data, bins=bins, alpha=1, label = "seals and bullae")
    plt.title(str(int(k/1000)) +'K random subsets of '+ str(m) +' seals among '
              + str(n)+ " seals")
    plt.xlabel(xlabel)
    plt.ylabel('Count')    
    plt.axvline(x = target, color = 'r', label="handles")    
    plt.plot([target, max(data)+5], [0, 0], color="red", lw=3, 
             linestyle='solid', label="_not in legend")    
    plt.annotate(str(round(count_geq(data, target)/k*100,4))+"%", 
                 xy=(target+(max(data)+5-target)/2, 
                     data.count(statistics.mode(data))*0.02), 
                 xytext=(0, 0), color="red",  
                 textcoords="offset pixels")
    plt.annotate(str(target), 
                 xy=(target, data.count(statistics.mode(data))*0.75), 
                 xytext=(LABEL_OFFSET, 0), color="red", 
                 textcoords="offset pixels")
    plt.legend()
    plt.savefig(xlabel+".jpg", dpi=300, bbox_inches='tight')
    plt.savefig(xlabel+".tif", dpi=300, bbox_inches='tight')
    plt.show()

def print_results(data, n, m, k, target, xlabel):    
    if(len(data) > 0) :
        print("Stamped handles value:", target)
        print("Seals & bullae values: ", end="")
        print("min=", min(data), 
              ", max=", max(data), 
              ", mode=", statistics.mode(data),               
              ", median=", round(statistics.median(data), 2), 
              ", mean=", round(statistics.mean(data), 2),               
              ", std-dev=", round(statistics.stdev(data), 2), 
              ", 95th percentile=", np.percentile(data, 95),
              sep="")
        print("Probability of having", target, "or more =", round(count_geq(data, target)/k*100, 4), "%")
    print_plot(data, n, m, k, target, xlabel)
    print()

#Choose k random uniform subsets of size m among the set [0, ..., n-1]. 
# Boolean parameter "different" enforces choice of different subsets, if True.
def get_random_indexes(n, m, k, different):
    samples = 0    
    all_combs = []    
    while samples < k:
        comb = random_combination(range(n), m)    
        if different and comb in all_combs:
            print("Already chosen")
        else:
            samples = samples+1
            all_combs.append(comb)
            if samples % 10000 == 0:
                print("\t", int(samples/1000), "/",int(k/1000), "k", sep='')
    return all_combs

def get_random_subsets(data, random_indexes):
    result = []
    for elem in random_indexes:
        result.append(take_subset(data, elem))
    return result

def count_geq(l, x): # number of elements in list l that are greater or equal to x 
    return len([i for i in l if i >= x])

def apply(func, handles, subsets, title):
    print(title)
    for i in range(len(title)):
        print("=", end="")
    print()
    count = func(handles)
    data =[func(elem) for elem in subsets]
    print_results(data, n, m, k, count, title)    
    
handles = read_data(HANDLES_FILE)
seals_bullae_data = read_data(SEALS_BULLAE_FILE)
print("Generating ", int(k/1000), "K subsets....", sep='')
random_indexes = get_random_indexes(n, m, k, ENFORCE_DIFFERENT_SUBSETS)
subsets = get_random_subsets(seals_bullae_data, random_indexes)
print("...done.\n")
    
apply(count_nbr_repeated_names, handles, subsets, "Number of repeated names")
apply(count_persons_with_rep_names, handles, subsets, 
      "Number of persons with repeated names")
apply(count_repeated_pairs, handles, subsets, "Number of repeated pairs")
apply(count_homonyms, handles, subsets, "Number of homonyms (PN1 = PN1)")
apply(count_potential_siblings, handles, subsets, 
      "Number of potential sibling relations (PN2 = PN2)")
apply(count_potential_genealogical_relations, handles, subsets, 
      "Number of potential genealogical relations (PN1 = PN2)")