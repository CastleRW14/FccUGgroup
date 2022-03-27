import subprocess
import os
import sys

filepath = sys.argv[1]

os.system('ls ' + filepath + '/Process_data_*.sh>' + filepath + '/tempfilelist.txt')

filelist = open(filepath + '/tempfilelist.txt','r')

for i in filelist:
	i = i.replace('\n','')
    subprocess.call('sbatch ' + i, shell=True)
    
    # rm Processed*.sh
    # rm slurm*.txt
    # ls -l | wc -l
