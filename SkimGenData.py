import ROOT
import numpy as np
import sys
import os
import uproot

def CalcE(px,py,pz,m):
	E = np.sqrt(px**2 + py**2 + pz**2 + m**2)
	return E

def ViablePairs(c1,c2):
	possiblepairs = []
	for i in range(len(c1)):
		for v in range(len(c2)):
			if(c1[i]*c2[v]==-1):
				possiblepairs.append((i,v))
	return possiblepairs

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

skimgenfile = open(targetpath + '/skimgen_mumu' + filename + '.txt', 'w')
skimgenfile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
skimgenfile.close()
skimgenfile = open(targetpath + '/skimgen_ee' + filename + '.txt', 'w')
skimgenfile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
skimgenfile.close()
skimgenfile = open(targetpath + '/skimgen_e+mu' + filename + '.txt', 'w')
skimgenfile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
skimgenfile.close()
skimgenfile = open(targetpath + '/skimgen_e-mu' + filename + '.txt', 'w')
skimgenfile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
skimgenfile.close()
skimgenfile = open(targetpath + '/skimgen_misc' + filename + '.txt', 'w')
skimgenfile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
skimgenfile.close()
for i in range(len(px)):
	survindex = []
	survpdg = []
	survcharge = []
	for v in range(len(px[i])):
		partpdg = pdgid[i][v]
		if np.abs(partpdg) == 11 or np.abs(partpdg) == 13:
			partpx = px[i][v]
			partpy = py[i][v]
			partpz = pz[i][v]
			partmass = mass[i][v]
			partE = CalcE(partpx, partpy, partpz, partmass)
			partCharge = charge[i][v]
			lv = ROOT.TLorentzVector()
			lv.SetPxPyPzE(partpx, partpy, partpz, partE)
			partpT = lv.Pt()
			partphi = lv.Phi()
			parteta = lv.Eta()
			if partpT > 20 and np.abs(parteta) < 2.4:
				survindex.append(v)
				survpdg.append(partpdg)
				survcharge.append(partCharge)
		'''skimgenfile.write(str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(partmass) + ',' + str(
			partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
		print(i)
		print(v)'''
	temppairs = ViablePairs(survcharge, survcharge)
	pairs = []
	for i in temppairs:
		if i[0] != i[1]:
			pairs.append(i)
	for v in pairs:
		print(v)
		p1 = survindex[v[0]]
		p2 = survindex[v[1]]
		pdg1 = pdgid[i][p1]
		pdg2 = pdgid[i][p2]
		if (pdg1 == 11 and pdg2 == -11) or (pdg2 == -11 and pdg2 == 11):
			skimgenfile = open(targetpath + '/skimgen_ee' + filename + '.txt', 'a')
		elif (pdg1 == 11 and pdg2 == -13) or (pdg1 == -13 and pdg2 == 11):
			skimgenfile = open(targetpath + '/skimgen_e-mu' + filename + '.txt', 'a')
		elif (pdg1 == -11 and pdg2 == 13) or (pdg1 == 13 and pdg2 == -11):
			skimgenfile = open(targetpath + '/skimgen_e+mu' + filename + '.txt', 'a')
		elif (pdg1 == -13 and pdg2 == 13) or (pdg1 == 13 and pdg2 == -13):
			skimgenfile = open(targetpath + '/skimgen_mumu' + filename + '.txt', 'a')
		else:
			skimgenfile = open(targetpath + '/skimgen_misc' + filename + '.txt', 'a')
		partpdg = pdgid[i][p1]
		partpx = px[i][p1]
		partpy = py[i][p1]
		partpz = pz[i][p1]
		partmass = mass[i][p1]
		partE = CalcE(partpx, partpy, partpz, partmass)
		partCharge = charge[i][p1]
		lv = ROOT.TLorentzVector()
		lv.SetPxPyPzE(partpx, partpy, partpz, partE)
		partpT = lv.Pt()
		partphi = lv.Phi()
		parteta = lv.Eta()
		skimgenfile.write(
			str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(
				partmass) + ',' + str(partCharge) + ',' + str(
				partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
		partpdg = pdgid[i][p2]
		partpx = px[i][p2]
		partpy = py[i][p2]
		partpz = pz[i][p2]
		partmass = mass[i][p2]
		partE = CalcE(partpx, partpy, partpz, partmass)
		partCharge = charge[i][p2]
		lv = ROOT.TLorentzVector()
		lv.SetPxPyPzE(partpx, partpy, partpz, partE)
		partpT = lv.Pt()
		partphi = lv.Phi()
		parteta = lv.Eta()
		skimgenfile.write(
			str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(
				partmass) + ',' + str(partCharge) + ',' + str(
				partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
		skimgenfile.close()
		


print('done')
