import ROOT
import numpy as np
import sys
import os
import uproot

def CalcE(px,py,pz,m):
	E = np.sqrt(px**2 + py**2 + pz**2 + m**2)
	return E

def FindHighestPair(partis, partpts, partpdgs):
    max1 = 0
    max2 = 0
    ind1 = 0
    ind2 = 0
    pdg1 = 0
    pdg2 = 0
    for i in range(len(partpts)):
        if partpts[i] >= max1:
            max1 = partpts[i]
            ind1 = partis[i]
            pdg1 = partpdgs[i]
    for i in range(len(partpts)):
        if (partpts[i] >= max2) & (partis[i] != ind1) & (partpdgs[i] * pdg1 < 0):
            max2 = partpts[i]
            ind2 = partis[i]
            pdg2 = partpdgs[i]
    return [ind1, ind2]

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

for i in range(len(px)):
    inds = []
    pts = []
    pdgs = []
    for v in range(len(px[i])):
        p1pdg = pdgid[i][v]
        if (p1pdg == -11) or (p1pdg == 11) or (p1pdg == -13) or (p1pdg == 13):
            p1x = px[i][v]
            p1y = py[i][v]
            p1z = pz[i][v]
            p1m = mass[i][v]
            p1E = CalcE(p1x, p1y, p1z, p1m)
            lv = ROOT.TLorentzVector()
            lv.SetPxPyPzE(p1x, p1y, p1z, p1E)
            p1pt = lv.Pt()
            p1eta = lv.Eta()
            if p1pt > 20:
                if np.abs(p1pt) < 2.4:
                    pts.append(p1pt)
                    inds.append(v)
                    pdgs.append(p1pdg)
    pair = FindHighestPair(inds, pts, pdgs)
    if (type(pair[0]) == type(1)) or (type(pair[1]) == type(1)):
        continue
    pppdg = [pdgid[i][pair[0]], pdgid[i][pair[1]]]
    if (pppdg[0] == 11 and pppdg[1] == -11) or (pppdg[1] == 11 and pppdg[0] == -11):
        skimgenfile = open(targetpath + '/skimgen_ee' + filename + '.txt', 'a')
    elif (pppdg[0] == 11 and pppdg[1] == -13) or (pppdg[1] == 11 and pppdg[0] == -13):
        skimgenfile = open(targetpath + '/skimgen_e-mu' + filename + '.txt', 'a')
    elif (pppdg[0] == -11 and pppdg[1] == 13) or (pppdg[1] == -11 and pppdg[0] == 13):
        skimgenfile = open(targetpath + '/skimgen_e+mu' + filename + '.txt', 'a')
    elif (pppdg[0] == -13 and pppdg[1] == 13) or (pppdg[1] == -13 and pppdg[0] == 13):
        skimgenfile = open(targetpath + '/skimgen_mumu' + filename + '.txt', 'a')
    else:
        continue
    for v in pair:
        p1pdg = pdgid[i][v]
        p1x = px[i][v]
        p1y = py[i][v]
        p1z = pz[i][v]
        p1m = mass[i][v]
        p1E = CalcE(p1x, p1y, p1z, p1m)
        lv = ROOT.TLorentzVector()
        lv.SetPxPyPzE(p1x, p1y, p1z, p1E)
        p1pt = lv.Pt()
        p1phi = lv.Phi()
        p1eta = lv.Eta()
        p1q = charge[i][v]
        p1pdg = pdgid[i][v]
        skimgenfile.write(
            str(i) + ',' + str(p1pdg) + ',' + str(p1x) + ',' + str(p1y) + ',' + str(p1z) + ',' + str(
                p1m) + ',' + str(p1q) + ',' + str(
                p1E) + ',' + str(p1pt) + ',' + str(p1phi) + ',' + str(p1eta) + '\n')

