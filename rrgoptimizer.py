# Wrestler Class

import sys

class wrestler:
    def __init__(self, fname, lname, weight):
        self.fname = fname;
        self.lname = lname;
        self.weight = weight;

    def __str__(self):
        return self.fname + " " + self.lname + " " + str(weight);

# Helper Methods


# Optimization Methods


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


