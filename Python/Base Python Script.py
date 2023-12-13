import pandas as pd
import numpy as np
import networkx as nx


import scipy.stats as stats
import numpy as np
import pandas as pd

df = pd.read_csv("assets/NISPUF17.csv")
df = df.dropna(subset=['HAD_CPOX', 'P_NUMVRC'])
df = df.fillna(value={'HAD_CPOX': 0, 'P_NUMVRC': 0})

def corr_chickenpox():

    corr, pval = stats.pearsonr(df['HAD_CPOX'], df['P_NUMVRC'])
    
    return corr

corr = corr_chickenpox()

print(corr)

#print("Yes, the dataset have the data we would need to investigate on the timing of the dose") 
