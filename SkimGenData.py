import ROOT
import numpy as np
import sys
import os
import uproot

def CalcE(px,py,pz,m):
	E = np.sqrt(px**2 + py**2 + pz**2 + m**2)
	return E

[filepath, filename] = os.path.split(sys.argv[1])
if(len(sys.argv)>2):
	targetpath = os.path.split(sys.argv[2])[0]
else:
	targetpath = filepath

rootfile = uproot.open(filepath + '/' + filename)

events = rootfile['events']

skimgen = events['skimmedGenParticles']

px = skimgen['skimmedGenParticles.core.p4.px'].array()
py = skimgen['skimmedGenParticles.core.p4.py'].array()
pz = skimgen['skimmedGenParticles.core.p4.pz'].array()
mass = skimgen['skimmedGenParticles.core.p4.mass'].array()
charge = skimgen['skimmedGenParticles.core.charge'].array()
pdgid = skimgen['skimmedGenParticles.core.pdgId'].array()

skimgenfile = open(targetpath+'/skimgen'+filename+'.txt','w')
skimgenfile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
skimgenfile.close()
skimgenfile = open(targetpath+'/skimgen'+filename+'.txt','a')

for i in range(len(px)):
	for v in range(len(px[i])):
		partpdg = pdgid[i][v]
		partpx = px[i][v]
		partpy = py[i][v]
		partpz = pz[i][v]
		partmass = mass[i][v]
		partE = CalcE(partpx, partpy, partpz, partmass)
		lv = ROOT.TLorentzVector()
		lv.SetPxPyPzE(partpx, partpy, partpz, partE)
		partpT = lv.Pt()
		partphi = lv.Phi()
		parteta = lv.Eta()
		skimgenfile.write(str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(partmass) + ',' + str(
			partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
		print(i)
		print(v)

skimgenfile.close()
print('done')
