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

electrons = events['electrons']
electronspdgid = electrons['electrons.core.pdgId'].array()
electronspx = electrons['electrons.core.p4.px'].array()
electronspy = electrons['electrons.core.p4.py'].array()
electronspz = electrons['electrons.core.p4.pz'].array()
electronsmass = electrons['electrons.core.p4.mass'].array()
electronscharge = electrons['electrons.core.charge'].array()

muons = events['muons']
muonspdgid = muons['muons.core.pdgId'].array()
muonspx = muons['muons.core.p4.px'].array()
muonspy = muons['muons.core.p4.py'].array()
muonspz = muons['muons.core.p4.pz'].array()
muonsmass = muons['muons.core.p4.mass'].array()
muonscharge = muons['muons.core.charge'].array()

recofile = open(targetpath + '/reco_mumu' + filename + '.txt', 'w')
recofile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
recofile.close()
recofile = open(targetpath + '/reco_ee' + filename + '.txt', 'w')
recofile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
recofile.close()
recofile = open(targetpath + '/reco_e+mu' + filename + '.txt', 'w')
recofile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
recofile.close()
recofile = open(targetpath + '/reco_e-mu' + filename + '.txt', 'w')
recofile.write('EventIndex,pdgId,px,py,pz,mass,charge,E,pT,phi,eta\n')
recofile.close()

totale = 0
eaftercuts = 0
totalm = 0
maftercuts = 0

for i in range(len(electronspx)):
	surveindex = []
	survepdg = []
	survecharge = []
	for v in range(len(electronspx[i])):
		totale += 1
		partpdg = electronspdgid[i][v]
		partpx = electronspx[i][v]
		partpy = electronspy[i][v]
		partpz =  electronspz[i][v]
		partmass =  electronsmass[i][v]
		partE = CalcE(partpx, partpy, partpz, partmass)
		partCharge =  electronscharge[i][v]
		lv = ROOT.TLorentzVector()
		lv.SetPxPyPzE(partpx, partpy, partpz, partE)
		partpT = lv.Pt()
		partphi = lv.Phi()
		parteta = lv.Eta()
		if partpT > 20 and np.abs(parteta) < 2.4:
			eaftercuts += 1
			surveindex.append(v)
			survepdg.append(partpdg)
			survecharge.append(partCharge)
	survmindex = []
	survmpdg = []
	survmcharge = []
	for v in range(len(muonspx[i])):
		totalm += 1
		partpdg = muonspdgid[i][v]
		partpx = muonspx[i][v]
		partpy = muonspy[i][v]
		partpz = muonspz[i][v]
		partmass = muonsmass[i][v]
		partE = CalcE(partpx, partpy, partpz, partmass)
		partCharge = muonscharge[i][v]
		lv = ROOT.TLorentzVector()
		lv.SetPxPyPzE(partpx, partpy, partpz, partE)
		partpT = lv.Pt()
		partphi = lv.Phi()
		parteta = lv.Eta()
		if partpT > 20 and np.abs(parteta) < 2.4:
			maftercuts += 1
			survmindex.append(v)
			survmpdg.append(partpdg)
			survmcharge.append(partCharge)
		pairs = ViablePairs(survecharge, survecharge)
		for v in pairs:
			p1 = surveindex[v[0]]
			p2 = surveindex[v[1]]
			pdg1 = electronspdgid[i][p1]
			pdg2 = electronspdgid[i][p2]
			partpdg = pdg1
			partpx = electronspx[i][p1]
			partpy = electronspy[i][p1]
			partpz = electronspz[i][p1]
			partmass = electronsmass[i][p1]
			partE = CalcE(partpx, partpy, partpz, partmass)
			partCharge = electronscharge[i][p1]
			lv = ROOT.TLorentzVector()
			lv.SetPxPyPzE(partpx, partpy, partpz, partE)
			partpT = lv.Pt()
			partphi = lv.Phi()
			parteta = lv.Eta()

			if (pdg1 == 11 and pdg2 == -11):
				recofile = open(targetpath + '/reco_ee' + filename + '.txt', 'a')
			else:
				continue
			recofile.write(
				str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(
					partmass) + ',' + str(partCharge) + ',' + str(
					partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
			partpdg = pdg2
			partpx = electronspx[i][p2]
			partpy = electronspy[i][p2]
			partpz = electronspz[i][p2]
			partmass = electronsmass[i][p2]
			partE = CalcE(partpx, partpy, partpz, partmass)
			partCharge = electronscharge[i][p2]
			lv = ROOT.TLorentzVector()
			lv.SetPxPyPzE(partpx, partpy, partpz, partE)
			partpT = lv.Pt()
			partphi = lv.Phi()
			parteta = lv.Eta()
			recofile.write(
				str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(
					partmass) + ',' + str(partCharge) + ',' + str(
					partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
			recofile.close()
		pairs = ViablePairs(survecharge, survmcharge)
		for v in pairs:
			p1 = surveindex[v[0]]
			p2 = survmindex[v[1]]
			pdg1 = electronspdgid[i][p1]
			pdg2 = muonspdgid[i][p2]
			partpdg = pdg1
			partpx = electronspx[i][p1]
			partpy = electronspy[i][p1]
			partpz = electronspz[i][p1]
			partmass = electronsmass[i][p1]
			partE = CalcE(partpx, partpy, partpz, partmass)
			partCharge = electronscharge[i][p1]
			lv = ROOT.TLorentzVector()
			lv.SetPxPyPzE(partpx, partpy, partpz, partE)
			partpT = lv.Pt()
			partphi = lv.Phi()
			parteta = lv.Eta()

			if (pdg1 == 11 and pdg2 == -13):
				recofile = open(targetpath + '/reco_e-mu' + filename + '.txt', 'a')
			elif (pdg1 == -11 and pdg2 == 13):
				recofile = open(targetpath + '/reco_e+mu' + filename + '.txt', 'a')
			else:
				continue
			recofile.write(
				str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(
					partmass) + ',' + str(partCharge) + ',' + str(
					partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
			partpdg = pdg2
			partpx = muonspx[i][p2]
			partpy = muonspy[i][p2]
			partpz = muonspz[i][p2]
			partmass = muonsmass[i][p2]
			partE = CalcE(partpx, partpy, partpz, partmass)
			partCharge = muonscharge[i][p2]
			lv = ROOT.TLorentzVector()
			lv.SetPxPyPzE(partpx, partpy, partpz, partE)
			partpT = lv.Pt()
			partphi = lv.Phi()
			parteta = lv.Eta()
			recofile.write(
				str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(
					partmass) + ',' + str(partCharge) + ',' + str(
					partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
			recofile.close()
		pairs = ViablePairs(survmcharge, survmcharge)
		for v in pairs:
			p1 = survmindex[v[0]]
			p2 = survmindex[v[1]]
			pdg1 = muonspdgid[i][p1]
			pdg2 = muonspdgid[i][p2]
			partpdg = pdg1
			partpx = muonspx[i][p1]
			partpy = muonspy[i][p1]
			partpz = muonspz[i][p1]
			partmass = muonsmass[i][p1]
			partE = CalcE(partpx, partpy, partpz, partmass)
			partCharge = muonscharge[i][p1]
			lv = ROOT.TLorentzVector()
			lv.SetPxPyPzE(partpx, partpy, partpz, partE)
			partpT = lv.Pt()
			partphi = lv.Phi()
			parteta = lv.Eta()

			if (pdg1 == -13 and pdg2 == 13):
				recofile = open(targetpath + '/reco_mumu' + filename + '.txt', 'a')
			else:
				continue
			recofile.write(
				str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(
					partmass) + ',' + str(partCharge) + ',' + str(
					partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
			partpdg = pdg2
			partpx = muonspx[i][p2]
			partpy = muonspy[i][p2]
			partpz = muonspz[i][p2]
			partmass = muonsmass[i][p2]
			partE = CalcE(partpx, partpy, partpz, partmass)
			partCharge = muonscharge[i][p2]
			lv = ROOT.TLorentzVector()
			lv.SetPxPyPzE(partpx, partpy, partpz, partE)
			partpT = lv.Pt()
			partphi = lv.Phi()
			parteta = lv.Eta()
			recofile.write(
				str(i) + ',' + str(partpdg) + ',' + str(partpx) + ',' + str(partpy) + ',' + str(partpz) + ',' + str(
					partmass) + ',' + str(partCharge) + ',' + str(
					partE) + ',' + str(partpT) + ',' + str(partphi) + ',' + str(parteta) + '\n')
			recofile.close()

print('e')
print(totale)
print(eaftercuts)
print(eaftercuts/totale)

print('m')
print(totalm)
print(maftercuts)
print(maftercuts/totalm)
