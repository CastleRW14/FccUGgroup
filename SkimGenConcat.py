import pandas as pd
import os
import sys

filepath = sys.argv[1]
if(len(sys.argv)>2):
	targetpath = sys.argv[2]
else:
	targetpath = filepath

os.system('ls ' + filepath + '/skimgen_eeevents*.root.txt>' + targetpath + '/skimgenfilelist.txt')

filelist = open(targetpath + '/skimgenfilelist.txt','r')

files = []

for i in filelist:
	i = i.replace('\n','')
	files.append(pd.read_csv(i))

if os.path.exists(targetpath + '/skimgen_ee_data.txt'):
	files.append(pd.read_csv(targetpath + '/skimgen_ee_data.txt'))

skimgen = pd.concat(files)

skimgen.to_csv(targetpath + '/skimgen_ee_data.txt', index=False)

for i in filelist:
	i = i.replace('\n', '')
	os.system('rm ' + i)

os.system('rm ' + targetpath + '/skimgenfilelist.txt')

os.system('ls ' + filepath + '/skimgen_e-muevents*.root.txt>' + targetpath + '/skimgenfilelist.txt')

filelist = open(targetpath + '/skimgenfilelist.txt','r')

files = []

for i in filelist:
	i = i.replace('\n','')
	files.append(pd.read_csv(i))

if os.path.exists(targetpath + '/skimgen_e-mu_data.txt'):
	files.append(pd.read_csv(targetpath + '/skimgen_e-mu_data.txt'))

skimgen = pd.concat(files)

skimgen.to_csv(targetpath + '/skimgen_e-mu_data.txt', index=False)

os.system('rm ' + targetpath + '/skimgenfilelist.txt')

for i in filelist:
	i = i.replace('\n', '')
	os.system('rm ' + i)

os.system('ls ' + filepath + '/skimgen_e+muevents*.root.txt>' + targetpath + '/skimgenfilelist.txt')

filelist = open(targetpath + '/skimgenfilelist.txt','r')

files = []

for i in filelist:
	i = i.replace('\n','')
	files.append(pd.read_csv(i))

if os.path.exists(targetpath + '/skimgen_e+mu_data.txt'):
	files.append(pd.read_csv(targetpath + '/skimgen_e+mu_data.txt'))

skimgen = pd.concat(files)

skimgen.to_csv(targetpath + '/skimgen_e+mu_data.txt', index=False)

for i in filelist:
	i = i.replace('\n', '')
	os.system('rm ' + i)

os.system('rm ' + targetpath + '/skimgenfilelist.txt')

os.system('ls ' + filepath + '/skimgen_mumuevents*.root.txt>' + targetpath + '/skimgenfilelist.txt')

filelist = open(targetpath + '/skimgenfilelist.txt','r')

files = []

for i in filelist:
	i = i.replace('\n','')
	files.append(pd.read_csv(i))

if os.path.exists(targetpath + '/skimgen_mumu_data.txt'):
	files.append(pd.read_csv(targetpath + '/skimgen_mumu_data.txt'))

skimgen = pd.concat(files)

skimgen.to_csv(targetpath + '/skimgen_mumu_data.txt', index=False)

for i in filelist:
	i = i.replace('\n', '')
	os.system('rm ' + i)

os.system('rm ' + targetpath + '/skimgenfilelist.txt')

os.system('ls ' + filepath + '/survive_*.root.txt>' + targetpath + '/skimgenfilelist.txt')

filelist = open(targetpath + '/skimgenfilelist.txt','r')

files = []

for i in filelist:
	i = i.replace('\n','')
	files.append(pd.read_csv(i))

if os.path.exists(targetpath + '/survived_skimgen.txt'):
	files.append(pd.read_csv(targetpath + '/survived_skimgen.txt'))

skimgen = pd.concat(files)

skimgen.to_csv(targetpath + '/survived_skimgen.txt', index=False)

for i in filelist:
	i = i.replace('\n', '')
	os.system('rm ' + i)

os.system('rm ' + targetpath + '/skimgenfilelist.txt')
