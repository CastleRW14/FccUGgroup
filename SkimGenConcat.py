import pandas as pd
import os
import sys

filepath = sys.argv[1]
if(len(sys.argv)>2):
	targetpath = sys.argv[2]
else:
	targetpath = filepath

os.system('ls ' + filepath + '/skimgenevents*.root.txt>' + targetpath + '/skimgenfilelist.txt')

filelist = open(targetpath + '/skimgenfilelist.txt','r')

files = []

for i in filelist:
	i = i.replace('\n','')
	files.append(pd.read_csv(i))

skimgen = pd.concat(files)

skimgen.to_csv(targetpath + '/skimgendata.txt', index=False)

os.system('rm ' + targetpath + '/skimgenfilelist.txt')