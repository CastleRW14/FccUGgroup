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

electrons = events['electrons']
epdgid = electrons['electrons.core.pdgId'].array()
epx = electrons['electrons.core.p4.px'].array()
epy = electrons['electrons.core.p4.py'].array()
epz = electrons['electrons.core.p4.pz'].array()
em = electrons['electrons.core.p4.mass'].array()
eq = electrons['electrons.core.charge'].array()

muons = events['muons']
mpdgid = muons['muons.core.pdgId'].array()
mpx = muons['muons.core.p4.px'].array()
mpy = muons['muons.core.p4.py'].array()
mpz = muons['muons.core.p4.pz'].array()
mm = muons['muons.core.p4.mass'].array()
mq = muons['muons.core.charge'].array()

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

for i in range(len(epx)):
    inds = []
    pts = []
    pdgs = []
    for v in range(len(epx[i])):
        p1pdg = epdgid[i][v]
        p1x = epx[i][v]
        p1y = epy[i][v]
        p1z = epz[i][v]
        p1m = em[i][v]
        p1E = CalcE(p1x, p1y, p1z, p1m)
        lv = ROOT.TLorentzVector()
        lv.SetPxPyPzE(p1x, p1y, p1z, p1E)
        p1pt = lv.Pt()
        p1eta = lv.Eta()
        if p1pt > 20:
            if np.abs(p1pt) < 2.4:
                print(1)
                pts.append(p1pt)
                inds.append([11, v])
                pdgs.append(p1pdg)
    print(0)
    for v in range(len(mpx[i])):
        p1pdg = mpdgid[i][v]
        p1x = mpx[i][v]
        p1y = mpy[i][v]
        p1z = mpz[i][v]
        p1m = mm[i][v]
        p1E = CalcE(p1x, p1y, p1z, p1m)
        lv = ROOT.TLorentzVector()
        lv.SetPxPyPzE(p1x, p1y, p1z, p1E)
        p1pt = lv.Pt()
        p1eta = lv.Eta()
        if p1pt > 20:
            if np.abs(p1pt) < 2.4:
                print(1)
                pts.append(p1pt)
                inds.append([13, v])
                pdgs.append(p1pdg)
    pair = FindHighestPair(inds, pts, pdgs)
    if (type(pair[0]) == type(1)) or (type(pair[1]) == type(1)):
        continue
    if pair[0][0] == 11:
        p1pdg = epdgid[i][pair[0][1]]
    elif pair[0][0] == 13:
        p1pdg = mpdgid[i][pair[0][1]]
    print(pair)
    if pair[1][0] == 11:
        p2pdg = epdgid[i][pair[1][1]]
    elif pair[1][0] == 13:
        p2pdg = mpdgid[i][pair[1][1]]
    pppdg = [p1pdg, p2pdg]
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
        if v[0] == 11:
            p1pdg = epdgid[i][v[1]]
            p1x = epx[i][v[1]]
            p1y = epy[i][v[1]]
            p1z = epz[i][v[1]]
            p1m = em[i][v[1]]
            p1q = eq[i][v[1]]
        elif v[0] == 13:
            p1pdg = mpdgid[i][v[1]]
            p1x = mpx[i][v[1]]
            p1y = mpy[i][v[1]]
            p1z = mpz[i][v[1]]
            p1m = mm[i][v[1]]
            p1q = mq[i][v[1]]
        p1E = CalcE(p1x, p1y, p1z, p1m)
        lv = ROOT.TLorentzVector()
        lv.SetPxPyPzE(p1x, p1y, p1z, p1E)
        p1pt = lv.Pt()
        p1phi = lv.Phi()
        p1eta = lv.Eta()
        skimgenfile.write(
            str(i) + ',' + str(p1pdg) + ',' + str(p1x) + ',' + str(p1y) + ',' + str(p1z) + ',' + str(
                p1m) + ',' + str(p1q) + ',' + str(
                p1E) + ',' + str(p1pt) + ',' + str(p1phi) + ',' + str(p1eta) + '\n')