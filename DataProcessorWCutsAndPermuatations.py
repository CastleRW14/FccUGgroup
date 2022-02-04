#README
#to run this code in a bash shell use
#python DataProcessorWCutsAndPermuations.py FilePath/filename.root TargetFilePath/
#e.g.
#python3 DataProcessorWCutsAndPermuations.py Data/Raw/events_000012600.root Data/Processed/
#That would output csv files electronwcutsevents_000012600.root.txt and muonwcutsevents_000012600.root.txt

import ROOT
import numpy as np
import sys
import os
import uproot

def CalcE(px,py,pz,m):
	E = np.sqrt(px**2 + py**2 + pz**2 + m**2)
	return E

def ViablePairs(eCharges,mCharges):
	possiblepairs = []
	for i in range(len(eCharges)):
		for v in range(len(mCharges)):
			if(eCharges[i]*mCharges[v]==-1):
				possiblepairs.append((i,v))
	return possiblepairs

filenamepath = os.path.split(sys.argv[1])
filename = filenamepath[1]
filepath = filenamepath[0]

if(len(sys.argv)>2):
	targetpath = os.path.split(sys.argv[2])[0]
else:
	targetpath = filepath

if(filepath!=''):
	filepath = filepath+'/'
if(targetpath!=''):
	targetpath = targetpath+'/'

rootfile = uproot.open(sys.argv[1])

events = rootfile['events']

electrons = events['electrons']
electronspx = electrons['electrons.core.p4.px'].array()
electronspy = electrons['electrons.core.p4.py'].array()
electronspz = electrons['electrons.core.p4.pz'].array()
electronsmass = electrons['electrons.core.p4.mass'].array()
electronscharge = electrons['electrons.core.charge'].array()

muons = events['muons']
muonspx = muons['muons.core.p4.px'].array()
muonspy = muons['muons.core.p4.py'].array()
muonspz = muons['muons.core.p4.pz'].array()
muonsmass = muons['muons.core.p4.mass'].array()
muonscharge = muons['muons.core.charge'].array()

emcutcount = 0
ptcutcount = 0
etacutcount = 0

elecfile = open(targetpath+'electronwcutsandperm'+filename+'.txt','w')
elecfile.write('EventIndex,px,py,pz,mass,E,pT,phi,eta\n')
elecfile.close()
elecfile = open(targetpath+'electronwcutsandperm'+filename+'.txt','a')

muonfile = open(targetpath+'muonwcutsandperm'+filename+'.txt','w')
muonfile.write('EventIndex,px,py,pz,mass,E,pT,phi,eta\n')
muonfile.close()
muonfile = open(targetpath+'muonwcutsandperm'+filename+'.txt','a')

for i in range(len(electronspx)):
	if((len(electronspx[i])>=1)&(len(muonspx[i])>=1)):
		emcutcount+=1
		ptpaircount = 0
		etapaircount = 0
		pairs = ViablePairs(electronscharge[i],muonscharge[i])
		if len(pairs) == 0: continue
		for v in pairs:
			
			elecpx = electronspx[i][v[0]]
			elecpy = electronspy[i][v[0]]
			elecpz = electronspz[i][v[0]]
			elecmass = electronsmass[i][v[0]]
			elecE = CalcE(elecpx,elecpy,elecpz,elecmass)
			eleclv = ROOT.TLorentzVector()
			eleclv.SetPxPyPzE(elecpx,elecpy,elecpz,elecE)
			elecpT = eleclv.Pt()
			elecphi = eleclv.Phi()
			eleceta = eleclv.Eta()
			
			muonpx = muonspx[i][v[1]]
			muonpy = muonspy[i][v[1]]
			muonpz = muonspz[i][v[1]]
			muonmass = muonsmass[i][v[1]]
			muonE = CalcE(muonpx,muonpy,muonpz,muonmass)
			muonlv = ROOT.TLorentzVector()
			muonlv.SetPxPyPzE(muonpx,muonpy,muonpz,muonE)
			muonpT = muonlv.Pt()
			muonphi = muonlv.Phi()
			muoneta = muonlv.Eta()
			
			if((elecpT>20)&(muonpT>20)):
				ptpaircount += 1
				if((np.abs(eleceta)<2.4)&(np.abs(muoneta)<2.4)):
					elecfile.write(str(i)+','+str(elecpx)+','+str(elecpy)+','+str(elecpz)+','+str(elecmass)+','+str(elecE)+','+str(elecpT)+','+str(elecphi)+','+str(eleceta)+'\n')
					muonfile.write(str(i)+','+str(muonpx)+','+str(muonpy)+','+str(muonpz)+','+str(muonmass)+','+str(muonE)+','+str(muonpT)+','+str(muonphi)+','+str(muoneta)+'\n')
					etapaircount = 1
		ptcutcount += ptpaircount
		etacutcount += etapaircount
elecfile.close()
muonfile.close()

print('At least 1 electron and 1 muon')
print(emcutcount)
print(emcutcount/len(electronspx))
print('PT cut')
print(ptcutcount)
print(ptcutcount/len(electronspx))
print('Eta cut')
print(etacutcount)
print(etacutcount/len(electronspx))
print('Total Events')
print(len(electronspx))