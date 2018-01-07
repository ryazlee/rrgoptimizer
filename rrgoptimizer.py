# Wrestler Class

import sys
from random import *

class wrestler:
    def __init__(self, fname, lname, weight):
        self.fname = fname;
        self.lname = lname;
        self.weight = weight;

    def __str__(self):
        return self.fname + " " + self.lname + " " + str(self.weight);

# Helper Methods

def printGroups(groups, allowance):
    count = 0;
    for group in groups:
        count += 1;
        groupMinWeight = getMinWeight(group)* (1+allowance);
        print("Group " + str(count) + " Max weight: " + str(groupMinWeight));
        for wrestler in group:
            print("\t" + str(wrestler));

def getMaxWeight(group):
    max = group[0].weight;
    for wrestler in group:
        if wrestler.weight > max:
            max = wrestler.weight;
    return max;

def getMinWeight(group):
    min = group[0].weight;
    for wrestler in group:
        if wrestler.weight <  min:
            min = wrestler.weight;
    return min;

def sortByWeight(wrestlers):
    wrestlers.sort(key=lambda x: x.weight, reverse=False);
    sortedArr = sorted(wrestlers, key=lambda x: x.weight, reverse=False);
    return sortedArr;

def sortGroupsByWeight(groups):
    groups.sort(key=lambda x: getMaxWeight(x), reverse=False);
    sortedArr = sorted(groups, key=lambda x: getMaxWeight(x), reverse=False);
    return sortedArr;

def printStats(groups):
    stats = {};
    for group in groups:
        if stats[len(group)] == None:
            stats[len(group)] = 1;
        else:
            stats[len(group)] += 1;
    for i in stats:
        print(str(i) + ": " + str(stat[i]));

# Optimization Methods

def optimizeByWeightAllowance(wrestlers, n, allowance):
    groups = [];
    for start in range(0, len(wrestlers)):
        maxweight = wrestlers[start].weight*(1+allowance);
        count = 0;
        group = [];
        for end in range(start, len(wrestlers)):
            if wrestlers[end].weight < maxweight and count < n:
                count += 1;
                group.append(wrestlers[end]);
            elif count == n or wrestlers[end].weight >=  maxweight:
                start = end + 1;
                break;
        groups.append(group);    
    groups.remove(groups[len(groups)-1]);
    return groups;

def createGroupsBySize(wrestlers, n):
    ret = [];
    temp = [];
    count = 0;
    for wrestler in wrestlers:
        if count == n-1:
            temp.append(wrestler);
            ret.append(temp);
            temp = [];
            count = 0;
        else:
            temp.append(wrestler);
            count += 1;
    if temp != []:
        ret.append(temp);
    return ret;        

# Executable Code

'''
Command Line Inputs:
    brackettype = sys.argv[0] = RR or BR
    bracketsize = sys.argv[1] = int
    bracketallowance = sys.argv[2] = double
    bracketsmallmax = sys.argv[3] = int
'''

'''
Run this when code finishes:
brackettype = sys.argv[0];
bracketsize = sys.argv[1];
bracketallowance = sys.argv[2];
bracketsmallmax = sys.argv[3]];
'''

brackettype = "BR";
bracketsize = 7;
bracketallowance = 0.05;
bracketsmallmax = 4;

wrestlers = [];

for x in range(0, 80):
    r = randint(100,200);
    w = wrestler("FN: " + str(r), "LN", r);
    wrestlers.append(w);

wrestlers = sortByWeight(wrestlers);
groups = createGroupsBySize(wrestlers, bracketsize);
printGroups(groups, bracketallowance);
op = optimizeByWeightAllowance(wrestlers, bracketsize, bracketallowance);
printGroups(op, bracketallowance);
