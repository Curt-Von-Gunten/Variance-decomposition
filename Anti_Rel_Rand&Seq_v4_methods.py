# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 09:09:42 2018

@author: cv85
"""
import os
import pandas as pd
import numpy as np
import seaborn as sns
import pylab
import matplotlib.pyplot as plt

path = "S:/IRB/Wu/VonGunten_2018/Simulation Project_10-32/Data_Code_Output/Anti/Revision"
os.chdir(path)
############################################################################
def CronbachAlpha(itemscores):
    itemscores = np.asarray(itemscores)
    itemvars = itemscores.var(axis=0, ddof=1)
    tscores = itemscores.sum(axis=1)
    nitems = itemscores.shape[1]
    calpha = nitems / float(nitems-1) * (1 - itemvars.sum() / float(tscores.var(ddof=1)))
    return calpha
##############################Random########################################
Anti = pd.read_csv('Anti_Ready_Revision.txt', sep="\t")
AntiSubs = list(Anti.Subject.unique())
AlphaResultsRandom = pd.DataFrame(columns=['Numb_of_Subs', 'Numb_of_Trials', "Cronbach's", 'LowCI', 'HighCI'])
SubjectNumber = [25,50,75,100]
TrialNumber = [8,18,26,50,80,120,160]
for e in SubjectNumber:
    for f in TrialNumber:
        Alpha = [] 
        for h in range(1,501):
            SubList = list(np.random.choice(AntiSubs, int(e)))
            temp = Anti[Anti.Subject.isin(SubList)]
            TrialList = list(np.random.choice(list(temp.Trial), f))
            temp.set_index("Trial", inplace=True)
            temp = temp.loc[TrialList]
            temp.reset_index(inplace=True)
            temp = pd.pivot_table(temp,index='Subject',columns='Trial',values='Acc')
            tempAlpha = CronbachAlpha(temp)
            Alpha.append(tempAlpha)
            print("Simulation " + str(h) + ": " + str(round(tempAlpha,2)) + ' (Sub: ' + str(e) + '; Trial: ' +  str(f) + ")" ) 
        AlphaMean, AlphaLowCI, AlphaHighCI = abs(np.mean(Alpha)), abs(np.percentile(Alpha, 5)), abs(np.percentile(Alpha, 95)) 
        #print("Alpha: " + str(e) + "," + str(f) + "," + ": " + str(AlphaMean) + str(AlphaLowCI) + str(AlphaHighCI))
        Experiment = [[e,f,AlphaMean,AlphaLowCI,AlphaHighCI]]
        ExpAlpha = pd.DataFrame(Experiment,columns=['Numb_of_Subs', 'Numb_of_Trials', "Cronbach's", 'LowCI', 'HighCI'])
        AlphaResultsRandom = AlphaResultsRandom.append(ExpAlpha)
##############################Random: max number of subs########################################
AntiSubs = list(Anti.Subject.unique())
AlphaResultsRandom_maxsubs = pd.DataFrame(columns=['Numb_of_Subs', 'Numb_of_Trials', "Cronbach's", 'LowCI', 'HighCI'])
SubjectNumber = [445]
TrialNumber = [8,18,26,50,80,120,160]
for e in SubjectNumber:
    for f in TrialNumber:
        Alpha = [] 
        for h in range(1,501):
            SubList = list(np.random.choice(AntiSubs, int(e)))
            temp = Anti[Anti.Subject.isin(SubList)]
            TrialList = list(np.random.choice(list(temp.Trial), f))
            temp.set_index("Trial", inplace=True)
            temp = temp.loc[TrialList]
            temp.reset_index(inplace=True)
            temp = pd.pivot_table(temp,index='Subject',columns='Trial',values='Acc')
            tempAlpha = CronbachAlpha(temp)
            Alpha.append(tempAlpha)
            print("Simulation " + str(h) + ": " + str(round(tempAlpha,2)) + ' (Sub: ' + str(e) + '; Trial: ' +  str(f) + ")" ) 
        AlphaMean, AlphaLowCI, AlphaHighCI = abs(np.mean(Alpha)), abs(np.percentile(Alpha, 5)), abs(np.percentile(Alpha, 95)) 
        #print("Alpha: " + str(e) + "," + str(f) + "," + ": " + str(AlphaMean) + str(AlphaLowCI) + str(AlphaHighCI))
        Experiment = [[e,f,AlphaMean,AlphaLowCI,AlphaHighCI]]
        ExpAlpha = pd.DataFrame(Experiment,columns=['Numb_of_Subs', 'Numb_of_Trials', "Cronbach's", 'LowCI', 'HighCI'])
        AlphaResultsRandom_maxsubs = AlphaResultsRandom_maxsubs.append(ExpAlpha)
##############################Sequential########################################
AlphaResultsSequential = pd.DataFrame(columns=['Numb_of_Subs', 'Numb_of_Trials', "Cronbach's", 'LowCI', 'HighCI'])
SubjectNumber = [25,50,75,100]
TrialNumber = [8,18,26,50,80]
for e in SubjectNumber:
    for f in TrialNumber:
        Alpha = []  
        for h in range(1,501):
            SubList = list(np.random.choice(AntiSubs, int(e)))
            temp = Anti[Anti.Subject.isin(SubList)]
            temp = temp[temp.Trial <= f]
            temp = pd.pivot_table(temp,index='Subject',columns='Trial',values='Acc')
            tempAlpha = CronbachAlpha(temp)
            Alpha.append(tempAlpha)
            print("Simulation " + str(h) + ": " + str(round(tempAlpha,2)) + ' (Sub: ' + str(e) + '; Trial: ' +  str(f) + ")" )  
        AlphaMean, AlphaLowCI, AlphaHighCI = abs(np.mean(Alpha)), abs(np.percentile(Alpha, 5)), abs(np.percentile(Alpha, 95)) 
        #print("Alpha: " + str(e) + "," + str(f) + "," + ": " + str(AlphaMean) + str(AlphaLowCI) + str(AlphaHighCI))
        Experiment = [[e,f,AlphaMean,AlphaLowCI,AlphaHighCI]]
        ExpAlpha = pd.DataFrame(Experiment,columns=['Numb_of_Subs', 'Numb_of_Trials', "Cronbach's", 'LowCI', 'HighCI'])
        AlphaResultsSequential = AlphaResultsSequential.append(ExpAlpha)
 
##############################Sequential without random sampling########################################
Anti_copy = Anti
AlphaResultsRaw = pd.DataFrame(columns=['Numb_of_Trials', "Cronbach's"])
TrialNumber = [8,18,26,50,80]
for f in TrialNumber:
    Alpha = []  
    temp = Anti_copy[Anti_copy.Trial <= f]
    temp = pd.pivot_table(temp,index='Subject',columns='Trial',values='Acc')
    tempAlpha = CronbachAlpha(temp)           
    print("Alpha: " + str(f) + ": " + str(tempAlpha))    
    Experiment = [[f,tempAlpha]]
    ExpAlpha = pd.DataFrame(Experiment,columns=['Numb_of_Trials', "Cronbach's"])
    AlphaResultsRaw = AlphaResultsRaw.append(ExpAlpha)
 
###########################Save Files######################################          
AlphaResultsRandom.to_csv("Anti_Rel_Rand_Test_sub.txt", sep="\t", index=False) 
AlphaResultsRandom_maxsubs.to_csv("Anti_Rel_Rand_max_Test_sub.txt", sep="\t", index=False)
AlphaResultsSequential.to_csv("Anti_Rel_Seq_Test_sub.txt", sep="\t", index=False) 
AlphaResultsRaw.to_csv("Anti_Rel_Raw_Test_sub.txt", sep="\t", index=False) 
############################################################################ 
path = "S:/IRB/Wu/VonGunten_2018/Simulation Project_10-32/Data_Code_Output/Anti/Revision"
os.chdir(path)  
Anti_Rel_Rand = pd.read_csv('Anti_Rel_Rand_Test_sub.txt', sep="\t")
Anti_Rel_Rand_max = pd.read_csv('Anti_Rel_Rand_max_Test_sub.txt', sep="\t")
Anti_Rel_Seq = pd.read_csv('Anti_Rel_Seq_Test_sub.txt', sep="\t")
Anti_Rel_Raw = pd.read_csv('Anti_Rel_Raw_Test_sub.txt', sep="\t")

sns.catplot(x="Numb_of_Trials", y="Cronbach's", hue="Numb_of_Subs", kind="point",
            style = "Numb_of_Subs", aspect=.6, ci=95, data=Anti_Rel_Rand);
pylab.savefig('Anti_Rel_Rand_subs.pdf')
sns.catplot(x="Numb_of_Trials", y="Cronbach's", hue="Numb_of_Subs", kind="point",
            style = "Numb_of_Subs", aspect=.6, ci=95, data=Anti_Rel_Seq);
pylab.savefig('Anti_Rel_Seq_subs.pdf')

######Stacking without subs######
Anti_Rel_Rand['Method'] = 'Random'
Anti_Rel_Rand_max['Method'] = 'Random_max'
Anti_Rel_Seq['Method'] = 'Sequential'
Anti_Rel_Raw['Method'] = 'Raw'
Anti_Rel_All = pd.concat([Anti_Rel_Rand, Anti_Rel_Rand_max, Anti_Rel_Seq, Anti_Rel_Raw])

sns.catplot(x="Numb_of_Trials", y="Cronbach's", hue="Method", kind="point",
            style = "Method", aspect=.6, ci=95, data=Anti_Rel_All);
pylab.savefig('Anti_Rel_All_Test_sub_meth.pdf')


###With CIs###
#Doesn't work with all datasets.
#Also doesn't work when subject is varied. Probably need to redo the x-index.
sns.catplot(x="Numb_of_Trials", y="Cronbach's",  kind="point",
             aspect=.6, ci=95, data=Anti_Rel_Rand_max);
plt.errorbar(x=Anti_Rel_Rand_max["Numb_of_Trials"].index, y=Anti_Rel_Rand_max["Cronbach's"],
yerr=(Anti_Rel_Rand_max['LowCI']-Anti_Rel_Rand_max['HighCI']), linestyle='')     

Anti_Rel_Two = pd.concat([Anti_Rel_Rand_max, Anti_Rel_Raw])
sns.catplot(x="Numb_of_Trials", y="Cronbach's",  kind="point", hue="Method", Style="Method",
             aspect=.6, ci=95, data=Anti_Rel_Two);
plt.errorbar(x=Anti_Rel_Two["Numb_of_Trials"].index, y=Anti_Rel_Two["Cronbach's"],
yerr=(Anti_Rel_Two['LowCI']-Anti_Rel_Two['HighCI']), linestyle='', capsize=5, elinewidth=1, markeredgewidth=1)  

#Anti_Rel_Two = pd.concat([Anti_Rel_Rand_max, Anti_Rel_Raw])
Anti_Rel_Two['High'] = Anti_Rel_Two['HighCI'] - Anti_Rel_Two["Cronbach's"]
Anti_Rel_Two['Low'] = Anti_Rel_Two["Cronbach's"] - Anti_Rel_Two['LowCI']
sns.catplot(x="Numb_of_Trials", y="Cronbach's",  kind="point", hue="Method", Style="Method",
             aspect=.6, ci=95, data=Anti_Rel_Two);
plt.errorbar(x=Anti_Rel_Two["Numb_of_Trials"].index, y=Anti_Rel_Two["Cronbach's"],
yerr=(Anti_Rel_Two["Low"], Anti_Rel_Two['High']), linestyle='', capsize=5, elinewidth=1, markeredgewidth=1)  


