import os
import sys

filepath = sys.argv[1]

os.system('ls ' + filepath + 'events*.root>' + 'filelist.txt')

f     = open('filelist.txt', 'r')

lines = f.readlines()

i = 0

for line in lines :
    line = line.replace('\n','')
    sh_file = 'Process_data_' + str(i) + '.sh'
    with open(sh_file, 'w') as cfg : #Loops the commands to run the file
        cfg.write("#!/bin/bash")
        cfg.write("\n")
        cfg.write("#SBATCH  -A cms")
        cfg.write("\n")
        cfg.write("#SBATCH --nodes=1")
        cfg.write("\n")
        cfg.write("#SBATCH --time=00:05:00")
        cfg.write("\n")
        cfg.write("cd /home/miacobuc/FCCAn/FccUGgroup")
        cfg.write("\n")
        cfg.write("module load anaconda")
        cfg.write("\n")
        cfg.write("source activate mycmsenv")
        cfg.write("\n")
        cfg.write("source /cvmfs/fcc.cern.ch/sw/latest/setup.sh")
        cfg.write("\n")
        cfg.write("python RecoData.py " + str(line) + " /home/miacobuc/FCCAn/Data/")
        cfg.write("\n")
    i += 1