import pandas as pd

skimgendata = pd.read_csv('Data/skimgendata.txt')
pdgid = skimgendata['pdgId']
pdgidlist = {}

for i in pdgid:
    if i in pdgidlist:
        pdgidlist[i] += 1
    else:
        pdgidlist[i] = 1

translation = {
    -1:'-d',
    1:'d',
    -2:'-u',
    2:'u',
    -3:'-s',
    3:'s',
    -4:'-c',
    4:'c',
    -5:'-b',
    5:'b',
    -6:'-t',
    6:'t',
    -11:'-e',
    11:'e',
    -12:'-neute',
    12:'neute',
    -13:'-mu',
    13:'mu',
    -14:'-neutu',
    14:'neutu',
    -15:'-tau',
    15:'tau',
    -16:'-neuttau',
    16:'neuttau',
    -21:'-g',
    21:'g',
    -22:'-photon',
    22:'photon',
    -24:'-W+',
    24:'W+',
    -130:'-K0L',
    130:'K0L',
    -211:'-pi+',
    211:'pi+',
    -321:'-K+',
    321:'K+',
    -2112:'-n',
    2112:'n',
    -2212:'-p',
    2212:'p'
}
translatedlist = {}

for i in sorted(pdgidlist):
    if i in translation:
        translatedlist[translation[i]] = pdgidlist[i]
    else:
        translatedlist[i] = pdgidlist[i]

for i in translatedlist:
    print(str(i) + ' ' + str(translatedlist[i]))
