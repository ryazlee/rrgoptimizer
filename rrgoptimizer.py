# Wrestler Class

import sys

class wrestler:
    def __init__(self, fname, lname, weight):
        self.fname = fname;
        self.lname = lname;
        self.weight = weight;

    def __str__(self):
        return self.fname + " " + self.lname + " " + str(self.weight);

# Helper Methods


# Optimization Methods

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
    ret.append(temp);
    return ret;        

def sortByWeight(wrestlers):
    wrestlers.sort(key=lambda x: x.weight, reverse=False);
    sortedArr = sorted(wrestlers, key=lambda x: x.weight, reverse=False);
    return sortedArr;

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
bracketsize = 8;
bracketallowance = 0.05;
bracketsmallmax = 4;

ryan = wrestler("ryan", "lee", 126);
nicole = wrestler("nicole", "lee", 106);
melissa = wrestler("melissa", "lee", 226);
derek = wrestler("derek", "lee", 321);
maddie = wrestler("maddie", "lee", 26);
a = wrestler("a", "ld", 136);
b = wrestler("b", "lee", 126);
c = wrestler("c", "adf", 413);

wrestlers = [ryan, nicole, melissa, derek, maddie, a, b, c]
