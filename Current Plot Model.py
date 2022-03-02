#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

def graphMaker():
    fileType = int(input('What file would you like to look over, EE [1], E+Mu [2], E-Mu [3], MuMu [4]'))
    graphType = int(input('What graph would you like to see, Pt Energy [1], Phi [2], Eta [3]'))

    #Importing the data in

    if fileType == 1:
        Data = pd.read_csv('skimgen_ee_data.txt')
        # Naming for the data and the chart
        RealName = 'Electron'
        AntiName = 'Positron'    
    elif fileType == 2:
        Data = pd.read_csv('skimgen_e+mu_data.txt')
        # Naming for the data and the chart
        RealName = 'Muon'
        AntiName = 'Positron'
    elif fileType == 3:
        Data = pd.read_csv('skimgen_e-mu_data.txt')
        # Naming for the data and the chart
        RealName = 'Electron'
        AntiName = 'Anti-Muon'
    elif fileType == 4:
        Data = pd.read_csv('skimgen_mumu_data.txt')
        # Naming for the data and the chart
        RealName = 'Muon'
        AntiName = 'Anti-Muon'
    else:
        print('Please choose your file type')


    #Spliting up the data into its particles

    # Electron Positron
    if fileType == 1:
        #Real Particle First (Electron)
        RData = Data['pdgId'] == 11
        ORData = Data[RData]

        #Anti Particle Next (Positron)
        AData = Data['pdgId'] == -11
        OAData = Data[AData]

    # Positron Muon
    elif fileType == 2:
        #Real Particle First (Muon)
        RData = Data['pdgId'] == 13
        ORData = Data[RData]

        #Anti Particle Next (Positron)
        AData = Data['pdgId'] == -11
        OAData = Data[AData]

    # Electron Anti-Muon
    elif fileType == 3:
        #Real Particle First (Electron)
        RData = Data['pdgId'] == 11
        ORData = Data[RData]

        #Anti Particle Next (Anti-Muon)
        AData = Data['pdgId'] == -13
        OAData = Data[AData]

    # Moun Anti-Muon
    elif fileType == 4:
        #Real Particle First (Muon)
        RData = Data['pdgId'] == 13
        ORData = Data[RData]

        #Anti Particle Next (Anti-Muon)
        AData = Data['pdgId'] == -13
        OAData = Data[AData]
    else:
        print('Please choose your file type')


    #Making our graphs
    if graphType == 1:
        #Making our Pt graph
        #Sepreating our data to only the pt of the particle
        ORpt = ORData['pT']
        OApt = OAData['pT']

        # Making our graph to compare the two energy levels and making them logrithmic for an easier viewing
        plt.hist(x=ORpt,bins=int(np.floor(ORpt.size**(1/2))),color='dodgerblue' , alpha=0.4, label=RealName)
        plt.xscale('log',base=10)
        plt.hist(x=OApt,bins=int(np.floor(OApt.size**(1/2))),color='forestgreen', alpha=0.35, label=AntiName)
        plt.xscale('log',base=10)
        plt.legend(loc='upper right')
        plt.title( RealName + ' ' + AntiName + ' Pt plot')
        plt.xlabel('Pt')
        plt.ylabel('Frequency')
        plt.plot(graphType)
        plt.show()

        #Print off the list of important information for the energy
        print('Pt   |'+ RealName + ' ' + AntiName)
        print('------------------------')
        print('Avg  |'+(str(ORpt.mean())[:10])+' '+(str(OApt.mean())[:10])+'|')
        print('Med  |'+(str(ORpt.median())[:10])+' '+(str(OApt.median())[:10])+'|')
        print('Min  |'+(str(ORpt.min())[:10])+' '+(str(OApt.min())[:10])+'|')
        print('Max  |'+(str(ORpt.max())[:10])+' '+(str(OApt.max())[:10])+'|')

    if graphType == 2:
        #Making our Phi graph
        #Sepreating our data to only the phi of the particle
        ORphi = ORData['phi']
        OAphi = OAData['phi']

        # Making our graph to compare the two phi values
        plt.hist(ORphi,bins=int(np.floor(ORphi.size**(1/2))),color='dodgerblue' , alpha=0.6, label=RealName)
        plt.hist(OAphi,bins=int(np.floor(OAphi.size**(1/2))),color='forestgreen', alpha=0.6, label=AntiName)
        plt.legend(loc='upper right')
        plt.title( RealName + ' ' + AntiName + ' Phi plot')
        plt.ylabel('Phi')
        plt.xlabel('Frequency')
        plt.plot(graphType)
        plt.show()

        #Print off the list of important information for the energy
        print('Phi  |'+ RealName + ' ' + AntiName)
        print('------------------------')
        print('Avg  |'+(str(ORphi.mean())[:10])+' '+(str(OAphi.mean())[:10])+'|')
        print('Med  |'+(str(ORphi.median())[:10])+' '+(str(OAphi.median())[:10])+'|')
        print('Min  |'+(str(ORphi.min())[:10])+' '+(str(OAphi.min())[:10])+'|')
        print('Max  |'+(str(ORphi.max())[:10])+' '+(str(OAphi.max())[:10])+'|')



    if graphType == 3:
        #Making our Eta graph
        #Sepreating our data to only the eta of the particle
        OReta = ORData['eta']
        OAeta = OAData['eta']

        # Making our graph to compare the two eta values
        plt.hist(x=OReta,bins=int(np.floor(OReta.size**(1/2))),color='dodgerblue' , alpha=0.6, label=RealName)
        plt.hist(x=OAeta,bins=int(np.floor(OAeta.size**(1/2))),color='forestgreen', alpha=0.6, label=AntiName)
        plt.legend(loc='upper right')
        plt.title( RealName + ' ' + AntiName + ' Eta plot')
        plt.ylabel('Eta')
        plt.xlabel('Frequency')
        plt.plot(graphType)
        plt.show()

        #Print off the list of important information for the energy
        print('Eta |'+ RealName + ' ' + AntiName)
        print('------------------------')
        print('Avg |'+(str(OReta.mean())[:10])+' '+(str(OAeta.mean())[:10])+'|')
        print('Med |'+(str(OReta.median())[:10])+' '+(str(OAeta.median())[:10])+'|')
        print('Min |'+(str(OReta.min())[:10])+' '+(str(OAeta.min())[:10])+'|')
        print('Max |'+(str(OReta.max())[:10])+' '+(str(OAeta.max())[:10])+'|')
        
    n = input('Would you like to make another [y] or [n]')
    if n == 'y':
        graphMaker()
    else:
        n = 0

graphMaker()

