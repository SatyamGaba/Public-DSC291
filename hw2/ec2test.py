#!/usr/bin/env python3

import numpy as np
from time import time
from os.path import isfile,isdir
from os import mkdir,chdir,getcwd
import pickle as pk

times = []
nTrials = 1000
nFibonacci = 10**4

# a dumb random computational task, on which to compare instances
inst_starttime = time()
for k in range(nTrials):
    starttime = time()
    fibonacci_previous = 1
    fibonacci_current = 1
    for i in range(2,nFibonacci):
        fibonacci_next = fibonacci_previous + fibonacci_current
        fibonacci_previous = fibonacci_current
        fibonacci_current = fibonacci_next
    DT = time() - starttime
    times.append(DT)
print(time() - inst_starttime)
    
#hist(times,bins=50)
exec_dir = getcwd()
log_dir = exec_dir + '/measurement_logs/'
if not isdir(log_dir):
    mkdir(log_dir)
fn = log_dir + 'stats.pkl'
with open(fn,'wb') as times_pkl:
    pk.dump(times,times_pkl,protocol=pk.HIGHEST_PROTOCOL)