import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df = pd.read_csv("assets/nhl.csv")
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities.columns = ["Metropolitan area", "Population", "NFL", "MLB", "NBA", "NHL"]

nhl_df = nhl_df[nhl_df['year']==2018]
nhl_df = nhl_df[~nhl_df['team'].str.contains('division', case = False)]
nhl_df["team"] = nhl_df["team"].str.replace(r'\[.*\]', '', regex=True)
nhl_df["team"] = nhl_df["team"].str.strip()

cities["Metropolitan area"] = cities["Metropolitan area"].str.replace(r'\[.*\]', '', regex=True)
cities["MLB"] = cities["MLB"].str.replace(r'\[.*\]', '', regex=True)
cities["NFL"] = cities["NFL"].str.replace(r'\[.*\]', '', regex=True)
cities["NBA"] = cities["NBA"].str.replace(r'\[.*\]', '', regex=True)
cities["NHL"] = cities["NHL"].str.replace(r'\[.*\]', '', regex=True)

cities["Metropolitan area"] = cities["Metropolitan area"].str.strip()
cities["NHL"] = cities["NHL"].str.strip()
cities["MLB"] = cities["MLB"].str.strip()
cities["NFL"] = cities["NFL"].str.strip()
cities["NBA"] = cities["NBA"].str.strip()



cities["NHL_words"] = cities["NHL"].str.split()
nhl_df["team_words"] = nhl_df["team"].str.split()


cities["common_words"] = cities["NHL_words"].apply(lambda x: common_words(x, nhl_df["team_words"].sum()))
cities = cities[cities["common_words"].str.len() > 0]
#merged_df = cities.merge(nhl_df, left_on="common_words", right_on="team_words", how="inner")

merged_df = pd.concat([cities, nhl_df], axis=1, join='inner')
merged_df = merged_df.drop(columns=["NHL_words", "team_words", "common_words"])


nhl_df["W"] = nhl_df["W"].astype(int)
nhl_df["L"] = nhl_df["L"].astype(int)
nhl_df["WinLossRatio"] = nhl_df["W"] / (nhl_df["W"] + nhl_df["L"])
    
    
population_by_region = merged_data["Population"].astype(int) 
win_loss_by_region = merged_data["WinLossRatio"]
    
    
correlation, p_value = stats.pearsonr(population_by_region, win_loss_by_region)
print(merged_df)
#print(cities)
#print(nhl_df)




import pandas as pd
import numpy as np
import scipy.stats as stats
import re


nhl_df = pd.read_csv("assets/nhl.csv")
cities = pd.read_html("assets/wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities.columns = ["Metropolitan area", "Population", "NFL", "MLB", "NBA", "NHL"]



nhl_df = nhl_df[nhl_df['year']==2018]
nhl_df = nhl_df[~nhl_df['team'].str.contains('division', case = False)]
nhl_df["team"] = nhl_df["team"].str.replace(r'\[.*\]', '', regex=True)
nhl_df["team"] = nhl_df["team"].str.strip()
#print(nhl_df)

cities["Metropolitan area"] = cities["Metropolitan area"].str.replace(r'\[.*\]', '', regex=True)
cities["MLB"] = cities["MLB"].str.replace(r'\[.*\]', '', regex=True)
cities["NFL"] = cities["NFL"].str.replace(r'\[.*\]', '', regex=True)
cities["NBA"] = cities["NBA"].str.replace(r'\[.*\]', '', regex=True)
cities["NHL"] = cities["NHL"].str.replace(r'\[.*\]', '', regex=True)

cities["Metropolitan area"] = cities["Metropolitan area"].str.strip()
cities["NHL"] = cities["NHL"].str.strip()
cities["MLB"] = cities["MLB"].str.strip()
cities["NFL"] = cities["NFL"].str.strip()
cities["NBA"] = cities["NBA"].str.strip()
#print(cities)


Common_words = cities.NHL.str.extract(r'(\w+)', expand = False)
Common_dict = dict(zip(Common_words, cities.Population))
#print(Common_dict) 



nhl_df['team'] = nhl_df.team.map(Common_words)
nhl_df.dropna(inplace=True)
print(nhl_df)
