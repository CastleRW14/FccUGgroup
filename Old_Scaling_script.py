#Based off of Amandeep's code

i     = 0
f     = open('filelist', 'r')
lines = f.readlines()


for line in lines :
    i   += 1
    line = line.strip('\n')
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
        cfg.write("module load anaconda/5.3.1-py37")
        cfg.write("\n")
        cfg.write("source activate phardcas37env")
        cfg.write("\n")
        cfg.write("cd /home/phardcas/scaling")
        cfg.write("\n")
        cfg.write("python DataProcessorWCutsAndPermuatations_v2.py " + str(line) + " Processed/File_" + str(i) + ".csv")
        cfg.write("\n")
