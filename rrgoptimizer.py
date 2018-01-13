# Wrestler Class

import sys
from random import *
import os;

class wrestler:
    def __init__(self, id, fname, lname, school,  weight):
        self.start = False;
        self.id = id;
        self.fname = fname;
        self.lname = lname;
        self.school = school;
        self.weight = weight;
        self.abname = self.fname + " " + self.lname + "(" + self.school +")";

    def __str__(self):
        return "Wrestler " + str(self.id) + ": " + self.abname + " " + str(self.weight);

# Helper Methods

def printGroups(groups):
    count = 0;
    for group in groups:
        count += 1;
        groupMaxWeight = getMaxWeight(group);
        #groupMinWeight = getMinWeight(group)* (1+allowance);
        size = len(group);
        if size == 1:
            size = ("********************************************* This is a one man bracket.  please fix this.");
        elif int(size) <= 3:
            size = "********************************************* Bracket Size of " + str(size);
        else: 
            size = str(size);
        print("Bracket " + str(count) + " Max weight: " + str(groupMaxWeight) + "\tSize: " + size);
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
    print("\nStats:")
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
            percent = float(stats[i]*100)/len(groups);
            total[0] += stats[i];
            total[1] += percent;
            total[2] += i * stats[i];
            print("Size " + str(i) + ":\t" + str(stats[i]) + "\t" + str(round(percent, 2)) + "%" + "\t# Wrestlers: " + str(i * stats[i]));
    print(".................\nTotal:\t" + str(total[0]) + "\t" + str(total[1]) + "%\t" + "# Wrestlers: " + str(total[2]));
# Optimization Methods

def optimizeByWeightAllowance(wrestlers, n, allowance):
    groups = [];
    group = [];
    count = 0;
    maxweight = 0;
    for wrestler in wrestlers:
        if count == 0 or wrestler.start == True:
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

def makePreAdjustments(wrestlers, txt):
    lines = txt.split("\n");
    for line in lines[1:len(lines)-1]:
        commands = line.split(":");
        if "START" in commands[0]:
            for wrestler in wrestlers:
                if wrestler.id == commands[1]:
                    wrestler.start = True;
        elif "OVERRIDE" in commands[0]:
            for wrestler in wrestlers:
                if wrestler.id == commands[1]:
                    wrestler.weight = float(commands[2]); 
        elif "REMOVE" in commands[0]:
            wrestlerindex = 0;
            for i in range(0, len(wrestlers)):
                if wrestlers[i].id == commands[1]:
                    wrestlerindex = i;
            wrestlers.pop(wrestlerindex);
    #printGroups(groups);
    return wrestlers;

def makePostAdjustments(groups, txt):
    lines = txt.split("\n");
    for line in lines[1:len(lines)-1]:
        commands = line.split(":");
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
    return groups;

# Execution Functions
def createRRGs(groups, templates, errors):
    os.system("cd RRGs/\nrm *");
    index = 0;
    for group in groups:
        index += 1;
        temp = templates[len(group)];
        found = False;
        for i in range(len(group), 50):
            if templates[i] != 0:
                if found == False and len(group) <= i:
                    temp = templates[i];
                    found = True; 
        if len(group) == 1:
            errors += "\nBracket " + str(index) + " is a one man group, fix this before writing to RRG file";
        for i in range(0, len(group)):
            temp = temp.replace("WRESTLER" + str(i+1), group[len(group) - i - 1].abname);
        for i in range(0, 50):
            temp = temp.replace("WRESTLER" + str(i+1), "BYE (BYE)");
        strindex = str(index);
        if index < 10:
            strindex = "0" + str(index);
        fh = open("RRGs/BR" + strindex + ".txt", "w+");
        fh.write(temp);
        fh.close();
    return errors;

# Executable Code

tourneyname = sys.argv[1];
brackettype = "";
bracketsize = 0;
bracketallowance = float(sys.argv[2]);
writeRRGs = sys.argv[3];
bracketsmallmax = 0;
errors = "Errors:";
bracketadj = "";
enddata = "";
templates = [];
for i in range(0, 50):
    templates.append(0);
try:
    cfg = open(tourneyname + ".cfg", "r");
    config = cfg.read();
    lines = config.split("\n");
    for line in range(0,len(lines) -1):
        param = lines[line].split(":");
        if param[0] == "brackettype": brackettype = param[1];
        elif param[0] == "bracketsize": bracketsize = int(param[1]);
        elif param[0] == "bracketsmallmax": bracketsmallmax = int(param[1]); 
        elif param[0] == "usebracket":
            num = int(param[1][2:]);
            templatefile = open("templates/" + param[1] + ".rrg");
            template = templatefile.read();
            templates[num] = template;
except:
    errors += "\ncannot open " + tourneyname + ".cfg";

if writeRRGs != "w": prwrite = "editting";
else: prwrite = "writing";
enddata += "Input > " + brackettype + " " + tourneyname + ": size: " + str(bracketsize) + ", bracketallowance: " + str(bracketallowance *100) + "%, smallest bracket size: " + str(bracketsmallmax) + ", action: " + prwrite;

try:
    file = open(tourneyname + ".ovr", "r");
    bracketadj = file.read();
    adjdata = bracketadj.split("\n",1)[1];
    enddata += "\nOverride file:\n" + adjdata[0:len(adjdata)-1];
except:
    errors += "\ncannot open " + tourneyname + ".ovr";
wrestlers = [];

op = [];

try:
    csv = open(tourneyname + ".csv");
    data = csv.read();
    lines = data.split("\n");
    index = 0;
    for line in range(0,len(lines) -1):
        index += 1;
        elems = lines[line].split(",");
        w = wrestler(str(index), elems[0], "", elems[1], float(elems[2]));
        wrestlers.append(w);
    wrestlers = makePreAdjustments(wrestlers, bracketadj);
    wrestlers = sortByWeight(wrestlers);
    op = optimizeByWeightAllowance(wrestlers, bracketsize, bracketallowance);
    op = makePostAdjustments(op, bracketadj);
except:
     errors += "\ncannot open " + tourneyname + ".csv";
printGroups(op);
printStats(op);

print(enddata);
if writeRRGs == "w": errors = createRRGs(op, templates, errors);
if errors == "Errors:":
    errors += " None, okay to write to RRG file";
print(errors);
