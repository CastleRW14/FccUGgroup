import subprocess
#r = range(0,7306)
r = range(2000,4000)
for count in r :   #I think len(filelist)=7306
    #print('sbatch Process_data_' + str(count) + '.sh')
    subprocess.call('sbatch Process_data_' + str(count) + '.sh', shell=True)
    # rm Processed*.sh
    # rm slurm*.txt
    # ls -l | wc -l
