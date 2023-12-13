   
import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
nhl_df = nhl_df[nhl_df['year'] == 2018]
nhl_df["team"] = nhl_df["team"].apply(lambda x: x.strip ())
nhl_df["team"] = nhl_df["team"].apply(lambda x: re.sub(r"Â|\*|\s\(\d+\)$", "", x))
#print(nhl_df)

cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
#renamed cities for convinience
cities.columns = ["Metropolitan area", "Population", "NFL", "MLB", "NBA", "NHL"]
cities["Metropolitan area"] = cities["Metropolitan area"].apply(lambda x: re.sub(r"Â|\*|\s\(\d+\)$", "", x))
cities["Metropolitan area"] = cities["Metropolitan area"].apply(lambda x: x.strip ())

def nhl_correlation():
    #YOUR CODE HERE
    global nhl_df # declare nhl_df as global
    #a dictionary to map team names to their corresponding metropolitan areas
    team_to_area = {"Toronto Raptors":"Toronto", "Boston Celtics":"Boston", "Philadelphia 76ers":"Philadelphia", "Cleveland Cavaliers":"Cleveland", "Indiana Pacers":"Indianapolis", "Miami Heat":"Miami–Fort Lauderdale", "Milwaukee Bucks":"Milwaukee", "Washington Wizards":"Washington, D.C", "Detroit Pistons":"Detroit", "Charlotte Hornets":"Charlotte", "New York Knicks":"New York City", "Brooklyn Nets":"Brooklyn", "Chicago Bulls":"Chicago", "Orlando Magic":"Orlando", "Atlanta Hawks":"Atlanta", "Houston Rockets":"Houston", "Golden State Warriors":"San Francisco Bay Area", "Portland Trail Blazers":"Portland", "Oklahoma City Thunder":"Oklahoma City", "Utah Jazz":"Salt Lake City", "New Orleans Pelicans":"New Orleans", "San Antonio Spurs":"San Antonio", "Minnesota Timberwolves":"Minneapolis–Saint Paul", "Denver Nuggets":"Denver", "Los Angeles Clippers":"Los Angeles", "Los Angeles Lakers":"Los Angeles", "Sacramento Kings":"Sacramento", "Dallas Mavericks":"Dallas–Fort Worth", "Memphis Grizzlies":"Memphis", "Phoenix Suns":"Phoenix"}

    #Map the nhl teams to their respective metropolitan areas
    nhl_df['Metropolitan area'] = nhl_df['team'].map(team_to_area)

    #W and L to numeric,
    nhl_df['W'] = pd.to_numeric(nhl_df['W'], errors='coerce')
    nhl_df['L'] = pd.to_numeric(nhl_df['L'], errors='coerce')
    nhl_df = nhl_df.dropna(subset=['W'])
    nhl_df = nhl_df.dropna(subset=['L'])

    #Calculate the win/loss ratio for 2018 and store it in a new column
    nhl_df['WinLossRatio'] = nhl_df['W'] / (nhl_df['W'] + nhl_df['L'])

    #Group by the metropolitan area and calculate the average win/loss ratio for cities with multiple teams
    average_win_loss_by_region = nhl_df.groupby('Metropolitan area')['WinLossRatio'].mean().reset_index()

    #Merge the average win/loss ratio data with the city data based on the metropolitan area
    merged_data = cities.merge(average_win_loss_by_region, on='Metropolitan area', how='inner')
    merged_data["NHL"] = merged_data["NHL"].apply(lambda x: re.sub(r"Â|\*|\s\(\d+\)$|\[note \d+\]", "", x))
    merged_data["NHL"].replace('', np.nan, inplace=True) 
    merged_data["NHL"].dropna(axis=0, how="any", inplace=True) 
    print(merged_data)
    
    # pass in metropolitan area population from cities
    population_by_region = merged_data['Population'].astype(int)
    
    # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]
    win_loss_by_region = merged_data['WinLossRatio']

    #assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    #assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for nhl"


    return stats.pearsonr(population_by_region, win_loss_by_region)

nhl_correlation_value = nhl_correlation()
print("NHL Win/Loss Ratio Correlation:", nhl_correlation_value)
#unique_metropolitan_areas = nhl_df['Metropolitan area'].nunique()
#print("Number of unique metropolitan areas:", unique_metropolitan_areas)

