import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
nfl_df = nfl_df[nfl_df['year'] == 2018]
nfl_df["team"] = nfl_df["team"].apply(lambda x: x.strip ())
nfl_df["team"] = nfl_df["team"].apply(lambda x: re.sub(r"Â|\*|\s\(\d+\)$", "", x))
#print(nfl_df)

cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
#renamed cities for convinience
cities.columns = ["Metropolitan area", "Population", "NFL", "MLB", "NBA", "NHL"]
cities["Metropolitan area"] = cities["Metropolitan area"].apply(lambda x: re.sub(r"Â|\*|\s\(\d+\)$", "", x))
cities["Metropolitan area"] = cities["Metropolitan area"].apply(lambda x: x.strip ())

def nfl_correlation():
    global nfl_df  # Declare nfl_df as a global variable
    # Map nfl teams to their corresponding metropolitan areas
    team_to_area = {"New York City": "New York Islanders", "Los Angeles": "Los Angeles Kings", "San Francisco Bay Area": "San Jose Sharks", "Chicago": "Chicago Blackhawks", "Dallas–Fort Worth": "Dallas Stars", "Washington, D.C.": "Washington Capitals", "Philadelphia": "Philadelphia Flyers", "Boston": "Boston Bruins", "Minneapolis–Saint Paul": "Minnesota Wild", "Denver": "Colorado Avalanche", "Miami–Fort Lauderdale": "Florida Panthers", "Phoenix": "Arizona Coyotes", "Detroit": "Detroit Red Wings", "Toronto": "Toronto Maple Leafs", "Houston": "Edmonton Oilers", "Atlanta": "Carolina Hurricanes", "Tampa Bay Area": "Tampa Bay Lightning", "Pittsburgh": "Pittsburgh Penguins", "Cleveland": "Columbus Blue Jackets", "Seattle": "Vegas Golden Knights", "Cincinnati": "Calgary Flames", "Kansas City": "Winnipeg Jets", "St. Louis": "St. Louis Blues", "Baltimore": "Nashville Predators", "Charlotte": "New Jersey Devils", "Indianapolis": "Montreal Canadiens", "Nashville": "Los Angeles Kings", "Milwaukee": "Vancouver Canucks", "New Orleans": "Buffalo Sabres", "Buffalo": "Anaheim Ducks", "Montreal": "Florida Panthers", "Vancouver": "New York Rangers", "Orlando": "San Jose Sharks", "Portland": "Chicago Blackhawks", "Columbus": "Pittsburgh Penguins", "Calgary": "Calgary Flames", "Ottawa": "Arizona Coyotes", "Edmonton": "Florida Panthers", "Salt Lake City": "Carolina Hurricanes", "Winnipeg": "Winnipeg Jets", "San Diego": "Buffalo Sabres", "San Antonio": "Anaheim Ducks", "Sacramento": "Arizona Coyotes", "Las Vegas": "Boston Bruins", "Jacksonville": "Buffalo Sabres", "Oklahoma City": "Chicago Blackhawks", "Memphis": "Colorado Avalanche", "Raleigh": "Columbus Blue Jackets", "Green Bay": "Detroit Red Wings", "Hamilton": "Edmonton Oilers", "Regina": "Los Angeles Kings" }

    # Map nfl teams to their respective metropolitan areas
    nfl_df['Metropolitan area'] = nfl_df['team'].map(team_to_area)
  
    
    
    #W and L to numeric,
    nfl_df['W'] = pd.to_numeric(nfl_df['W'], errors='coerce')
    nfl_df['L'] = pd.to_numeric(nfl_df['L'], errors='coerce')
    nfl_df = nfl_df.dropna(subset=['W'])
    nfl_df = nfl_df.dropna(subset=['L'])
    print(nfl_df)
    #Calculate the win/loss ratio for 2018 and store it in a new column
    nfl_df['WinLossRatio'] = nfl_df['W'] / (nfl_df['W'] + nfl_df['L'])
    
    
    
    
    
    #Group by the metropolitan area and calculate the average win/loss ratio for cities with multiple teams
    average_win_loss_by_region = nfl_df.groupby('Metropolitan area')['WinLossRatio'].mean().reset_index()
    print(average_win_loss_by_region)
    #Merge the average win/loss ratio data with the city data based on the metropolitan area
    merged_data = cities.merge(average_win_loss_by_region, on='Metropolitan area', how='inner')
    merged_data["NFL"] = merged_data["NFL"].apply(lambda x: re.sub(r"Â|\*|\s\(\d+\)$|\[note \d+\]", "", x))
    merged_data["NFL"].replace('', np.nan, inplace=True) 
    merged_data["NFL"].dropna(axis=0, how="any", inplace=True) 
    print(merged_data)
    
    # pass in metropolitan area population from cities
    population_by_region = merged_data['Population'].astype(int)
    
    # pass in win/loss ratio from NFL_df in the same order as cities["Metropolitan area"]
    win_loss_by_region = merged_data['WinLossRatio']

    #assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    #assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NFL"

    

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]

nfl_correlation_value = nfl_correlation()
print("NFL Win/Loss Ratio Correlation:", nfl_correlation_value)
unique_metropolitan_areas = nfl_df['Metropolitan area'].nunique()
print("Number of unique metropolitan areas:", unique_metropolitan_areas)
