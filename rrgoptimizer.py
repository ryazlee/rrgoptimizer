# Wrestler Class

import sys
from random import *

class wrestler:
    def __init__(self, id, fname, lname, weight):
        self.id = id;
        self.fname = fname;
        self.lname = lname;
        self.weight = weight;

    def __str__(self):
        return "Wrestler " + str(self.id) + ": " + self.fname + " " + self.lname + " " + str(self.weight);

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
    min = 10000;
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
    print("Stats:")
    stats = [];
    for i in range(0, 500):
        stats.append(0);
    for group in groups:
        stats[len(group)] += 1;
    for i in range(0, len(stats)):
        if stats[i] != 0:
            percent = stats[i]/len(groups)* 100;
            print("Size " + str(i) + ": " + str(stats[i]) + " " + str(round(percent, 2)) + "%");

# Optimization Methods

def optimizeByWeightAllowance(wrestlers, n, allowance):
    groups = [];
    group = [];
    count = 0;
    maxweight = 0;
    for wrestler in wrestlers:
        if count == 0:
            maxweight = wrestler.weight * (1 + allowance);
            group = [wrestler];
            count += 1;
        elif wrestler.weight < maxweight and count < n:
            group.append(wrestler);
            count += 1;
        else:
            groups.append(group);
            group = [wrestler];
            maxweight = wrestler.weight * (1 + allowance);
            count = 1;
    groups.append(group);
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

def makeAdjustments(groups, txt):
    lines = txt.split(",");
    for line in lines[:len(lines)-1]:
        commands = line.split(":");
        if commands[2] == "START":
            newgroup = [];
            keepgroup = [];
            groupindex = 0;
            removegroup = None;
            for group in groups:
                cancontinue = False;
                index = 0;
                groupindex += 1;
                for wrestler in group:
                    if wrestler.id == commands[0] and index != 0:
                        removegroup = group;
                        keepgroup = group[:index];
                        newgroup = group[index:];
                    index += 1;
            if newgroup != []:
                groups.append(newgroup);
                groups.append(keepgroup);
                groups.remove(removegroup);
            groups = sortGroupsByWeight(groups);
        if commands[2] == "SWAP":
            groupindex = 0; 
            group1 = 0;
            wrestler1 = 0;
            group2 = 0;
            wrestler2 = 0;
            for group in groups:
                wrestlerindex = 0;
                for wrestler in group:
                    if wrestler.id == commands[0]:
                        group1 = groupindex;
                        wrestler1 = wrestlerindex;
                    if wrestler.id == commands[1]:
                        group2 = groupindex;
                        wrestler2 = wrestlerindex;
                    wrestlerindex += 1;
                groupindex += 1;
            groups[group2][wrestler2], groups[group1][wrestler1] = groups[group1][wrestler1], groups[group2][wrestler2]
    return groups;

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
bracketsize = 3;
bracketallowance = 0.02;
bracketsmallmax = 4;
file = open("adjustments.ovr", "r");
bracketadj = file.read();
bracketadj = bracketadj.replace("\n", "");
wrestlers = [];

for x in range(0, 6):
    r = randint(100,110);
    w = wrestler(str(x) , "FN:" + str(x), "", r);
    wrestlers.append(w);

wrestlers = sortByWeight(wrestlers);
#groups = createGroupsBySize(wrestlers, bracketsize);
op = optimizeByWeightAllowance(wrestlers, bracketsize, bracketallowance);
printGroups(op, bracketallowance);
print("After adjustments......");
op = makeAdjustments(op, bracketadj);
printGroups(op, bracketallowance);
printStats(op);
