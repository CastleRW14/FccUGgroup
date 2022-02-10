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

