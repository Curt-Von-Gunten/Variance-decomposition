# -*- coding: utf-8 -*-
"""
Created on Tue May 21 16:36:59 2019

@author: cv85
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
############################################################################
def CronbachAlpha(itemscores):
    itemscores = np.asarray(itemscores)
    itemvars = itemscores.var(axis=0, ddof=1)
    tscores = itemscores.sum(axis=1)
    nitems = itemscores.shape[1]
    calpha = nitems / float(nitems-1) * (1 - itemvars.sum() / float(tscores.var(ddof=1)))
    return calpha
############################################################################
path = "S:/IRB/Wu/VonGunten_2018/Simulation Project_10-32/Data_Code_Output/Anti/Revision"
os.chdir(path)
Anti = pd.read_csv('Anti_Ready_Revision.txt', sep="\t")
##############################Random: max number of subs########################################
AntiSubs = list(Anti.Subject.unique())
AlphaResultsRand = pd.DataFrame(columns=['Numb_of_Subs', 'Numb_of_Trials', "Cronbach's"])
SubjectNumber = [20,35,50,100,150]
TrialNumber = [6,16,26,50,80]
for e in SubjectNumber:
    for f in TrialNumber:
        Alpha = [] 
        for h in range(1,501):
            SubList = list(np.random.choice(AntiSubs, int(e)))
            temp = Anti[Anti.Subject.isin(SubList)]
            temp = temp = temp[temp['Trial'] <= f]
            temp = pd.pivot_table(temp,index='Subject',columns='Trial',values='Acc')
            tempAlpha = CronbachAlpha(temp)
            Alpha.append(tempAlpha)
            print("Simulation " + str(h) + ": " + str(round(tempAlpha,2)) + ' (Sub: ' + str(e) + '; Trial: ' +  str(f) + ")" ) 
        AlphaMean = np.mean(Alpha)
        Experiment = [[e,f,AlphaMean]]
        ExpAlpha = pd.DataFrame(Experiment,columns=['Numb_of_Subs', 'Numb_of_Trials', "Cronbach's"])
        AlphaResultsRand = AlphaResultsRand.append(ExpAlpha)
###########################Save Files######################################          
AlphaResultsRand.to_csv("Anti_rel_seqonly.txt", sep="\t", index=False)
############################################################################ 
##############################Plotting######################################
############################################################################
path = "S:/IRB/Wu/VonGunten_2018/Simulation Project_10-32/Data_Code_Output/Anti/Revision"
os.chdir(path)
Anti_Rel_Seq_subsrand = pd.read_csv('Anti_rel_seqonly.txt', sep="\t")
sns.set(style="whitegrid", font_scale=1.2)
g = sns.catplot(x="Numb_of_Trials", y="Cronbach's", hue="Numb_of_Subs", kind="point",
            style = "Numb_of_Subs", data=Anti_Rel_Seq_subsrand, 
            aspect=.8, legend = False, palette=sns.cubehelix_palette(5, start=0, rot=-.4, hue=1, dark=.2, light=.8));
#plt.errorbar(x=Stroop_Rel_Two["Numb_of_Trials"].index, y=Stroop_Rel_Two["SplitHalf"], yerr=(Stroop_Rel_Two["Low"], Stroop_Rel_Two['High']), ecolor = 'teal', linestyle='', capsize=4, elinewidth=1, markeredgewidth=1, label=None) 
plt.legend(loc='upper left', title='Subjects')
plt.xlabel("Number of antisaccade trials")
plt.ylabel("Cronbach's alpha")
plt.title("Antisaccade internal reliability")
#plt.axhline(.8, color='k', linestyle='-', linewidth=.5)
plt.axvline(2.91, color='k', linestyle='-', linewidth=.5)
#plt.axvline(3.9, color='k', linestyle=':', linewidth=.9)
g.set(ylim=(0, 1))

##############################Export######################################
plt.savefig('Anti_rel_seqonly.pdf', bbox_inches = 'tight')
#plt.savefig('TreatPercTable_v1.tiff', bbox_inches = 'tight', dpi=300)
