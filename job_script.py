import subprocess

for count in range(7306) :   #I think len(filelist)=7306
    #print('sbatch Process_data_' + str(count) + '.sh')
    subprocess.call('sbatch Process_data_' + str(count) + '.sh', shell=True)
    # rm Processed*.sh
    # rm slurm*.txt
    # ls -l | wc -l
