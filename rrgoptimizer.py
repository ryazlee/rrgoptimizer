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

def printGroups(groups):
    count = 0;
    for group in groups:
        count += 1;
        groupMaxWeight = getMaxWeight(group);
        #groupMinWeight = getMinWeight(group)* (1+allowance);
        size = len(group);
        if size <= 3:
            size = "********************************************** Group Size of " + str(size);
        else: size = str(size);

        print("Group " + str(count) + " Max weight: " + str(groupMaxWeight) + "\tSize: " + size);
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
    total = [];
    for i in range(0, 3):
        total.append(0);
    for i in range(0, 500):
        stats.append(0);
    for group in groups:
        stats[len(group)] += 1;
    for i in range(0, len(stats)):
        if stats[i] != 0:
            percent = stats[i]/len(groups)* 100;
            total[0] += stats[i];
            total[1] += percent;
            total[2] += i * stats[i];
            print("Size " + str(i) + ":\t" + str(stats[i]) + "\t" + str(round(percent, 2)) + "%" + "\tAmount: " + str(i * stats[i]));
    print(".................\nTotal:\t" + str(total[0]) + "\t" + str(total[1]) + "%\t" + "Amount: " + str(total[2]));
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
    lines = txt.split("\n");
    for line in lines[1:len(lines)-1]:
        commands = line.split(":");
        if "START" in commands[0]:
            newgroup = [];
            keepgroup = [];
            groupindex = 0;
            removegroup = None;
            for group in groups:
                cancontinue = False;
                index = 0;
                groupindex += 1;
                for wrestler in group:
                    if wrestler.id == commands[1] and index != 0:
                        removegroup = group;
                        keepgroup = group[:index];
                        newgroup = group[index:];
                    index += 1;
            if newgroup != []:
                groups.append(newgroup);
                groups.append(keepgroup);
                groups.remove(removegroup);
            groups = sortGroupsByWeight(groups);
        if "SWAP" in commands[0]:
            groupindex = 0; 
            group1 = 0;
            wrestler1 = 0;
            group2 = 0;
            wrestler2 = 0;
            for group in groups:
                wrestlerindex = 0;
                for wrestler in group:
                    if wrestler.id == commands[2]:
                        group1 = groupindex;
                        wrestler1 = wrestlerindex;
                    if wrestler.id == commands[1]:
                        group2 = groupindex;
                        wrestler2 = wrestlerindex;
                    wrestlerindex += 1;
                groupindex += 1;
            groups[group2][wrestler2], groups[group1][wrestler1] = groups[group1][wrestler1], groups[group2][wrestler2]
    
    printGroups(groups);
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
brackettype = sys.argv[1];
bracketsize = sys.argv[2];
bracketallowance = sys.argv[3];
bracketsmallmax = sys.argv[4]];
'''

tourneyname = sys.argv[1];
brackettype = "";
bracketsize = 0;
bracketallowance = float(sys.argv[2]);
bracketsmallmax = 0;
errors = "Errors:";
bracketadj = "";
try:
    cfg = open(tourneyname + ".cfg", "r");
    config = cfg.read();
    lines = config.split("\n");
    for line in range(0,len(lines) -1):
        param = lines[line].split(":");
        if param[0] == "brackettype": brackettype = param[1];
        elif param[0] == "bracketsize": bracketsize = int(param[1]);
        elif param[0] == "bracketsmallmax": bracketsmallmax = int(param[1]); 
except:
    errors += "\ncannot open " + tourneyname + ".cfg";

try:
    file = open(tourneyname + ".ovr", "r");
    bracketadj = file.read();
except:
    errors += "\ncannot open " + tourneyname + ".ovr";
wrestlers = [];

try:
    csv = open(tourneyname + ".csv");
    data = csv.read();
    lines = data.split("\n");
    index = 0;
    for line in range(0,len(lines) -1):
        index += 1;
        elems = lines[line].split(",");
        w = wrestler(str(index), elems[0], elems[1], float(elems[2]));
        wrestlers.append(w);
    wrestlers = sortByWeight(wrestlers);
    op = optimizeByWeightAllowance(wrestlers, bracketsize, bracketallowance);
    op = makeAdjustments(op, bracketadj);
    printStats(op);
except:
    errors += "\ncannot open " + tourneyname + ".csv";

if errors == "Errors:":
    errors += " None"
print(brackettype + " " + tourneyname + ": size: " + str(bracketsize) + ", bracketallowance: " + str(bracketallowance *100) + "%, smallest bracket size: " + str(bracketsmallmax));
print(errors);
