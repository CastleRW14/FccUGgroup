#!/usr/bin/env_python

i     = 0
f     = open('filelist.txt', 'r')
lines = f.readlines()

runfile = open("RunSlurm_"+"filelist.txt".rsplit(".",1)[0]+".sh", "w")

runfile.write("#!/bin/sh")
runfile.write("\n")


for line in lines :
    i   += 1
    line = line.strip('\n')
    sh_file = 'SlurmJobs/Process_data_' + str(i) + '.sh'
    
    with open(sh_file, 'w') as cfg :
        cfg.write("#!/bin/bash") 
        cfg.write("\n")
        cfg.write("#SBATCH  -A cms")
        cfg.write("\n")
        cfg.write("#SBATCH --nodes=1")
        cfg.write("\n")
        cfg.write("#SBATCH --time=01:00:00")
        cfg.write("\n")
        cfg.write("module load anaconda/5.3.1-py37")
        cfg.write("\n")
        cfg.write("source activate phardcas37env")
        cfg.write("\n")
        cfg.write("source /cvmfs/fcc.cern.ch/sw/latest/setup.sh")
        cfg.write("\n")
        cfg.write("cd /home/phardcas/scaling")
        cfg.write("\n")
        cfg.write("python3 SkimGenData.py " + str(line) + " /home/phardcas/scaling/FccDataForUs/") 
        cfg.write("\n")

    runfile.write("sbatch SlurmJobs/Process_data_" + str(i) + ".sh")
    runfile.write("\n")
