#README
#to run this code in a bash shell use
#python CsvConcat.py FilePath/ TargetPath/
#e.g
#python3 CsvConcat.py Data/Processed/ Data/
#Will concatonate all appropriate files in Data/Processed/ and put the concatonated csv in Data/
#This also works without any secondary argument, that just outputs to current directory

import pandas as pd
import os
import sys

filepath = sys.argv[1]
if(len(sys.argv)>2):
	targetpath = sys.argv[2]
else:
	targetpath = ''

os.system('ls '+filepath+'electronwcutsand*.root.txt>'+targetpath+'electronfilelist.txt')
os.system('ls '+filepath+'muonwcutsand*.root.txt>'+targetpath+'muonfilelist.txt')

electronfilelist = open(targetpath+'electronfilelist.txt','r')
muonfilelist = open(targetpath+'muonfilelist.txt','r')

electronfiles = []
muonfiles = []

for i in electronfilelist:
	i = i.replace('\n','')
	electronfiles.append(pd.read_csv(i))
for i in muonfilelist:
	i = i.replace('\n','')
	muonfiles.append(pd.read_csv(i))

electrons = pd.concat(electronfiles)
muons = pd.concat(muonfiles)

electrons.to_csv(targetpath+'electronwcutsandperm.txt',index=False)
muons.to_csv(targetpath+'muonwcutsandperm.txt',index=False)

os.system('rm '+targetpath+'electronfilelist.txt')
os.system('rm '+targetpath+'muonfilelist.txt')