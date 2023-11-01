import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
#renamed cities for convinience
cities.columns = ["Metropolitan area", "Population", "NFL", "MLB", "NBA", "NBA"]

#print(nba_df)
def nba_correlation(): 
    # YOUR CODE HERE
    # a dictionary to map team names to their corresponding metropolitan areas 
    team_to_area = {"Tampa Bay Lightning*":"Tampa Bay Area", "Boston Bruins*":"Boston", "Toronto Maple Leafs*":"Toronto", "Florida Panthers":"Miami–Fort Lauderdale", "Detroit Red Wings":"Detroit", "Montreal Canadiens":"Montreal", "Ottawa Senators":"Ottawa", "Buffalo Sabres":"Buffalo", "Washington Capitals*":"Washington, D.C", "Pittsburgh Penguins*":"Pittsburgh", "Philadelphia Flyers*":"Philadelphia", "Columbus Blue Jackets*":"Columbus", "New Jersey Devils*":"Newark", "Carolina Hurricanes":"Raleigh", "New York Islanders":"New York City", "New York Rangers":"New York City", "Nashville Predators*":"Nashville", "Winnipeg Jets*":"Winnipeg", "Minnesota Wild*":"Minneapolis–Saint Paul", "Colorado Avalanche*":"Denver", "St. Louis Blues":"St. Louis", "Dallas Stars":"Dallas–Fort Worth", "Chicago Blackhawks":"Chicago", "Vegas Golden Knights*":"Las Vegas", "Anaheim Ducks*":"Anaheim", "San Jose Sharks*":"San Jose", "Los Angeles Kings*":"Los Angeles", "Calgary Flames":"Calgary", "Edmonton Oilers":"Edmonton", "Vancouver Canucks":"Vancouver", "Arizona Coyotes":"Phoenix"}
    # Map the NBA teams to their respective metropolitan areas 
    nba_df['Metropolitan area'] = nba_df['team'].map(team_to_area)
    
    # W and L to numeric,
    nba_df['W'] = pd.to_numeric(nba_df['W'], errors='coerce')
    nba_df['L'] = pd.to_numeric(nba_df['L'], errors='coerce')
    nba_df = nba_df.dropna(subset=['W'])
    nba_df = nba_df.dropna(subset=['L'])


    ## Calculate the win/loss ratio for 2018 and store it in a new column 
    nba_df['WinLossRatio'] = nba_df['W'] / (nba_df['W'] + nba_df['L']) 
    # Group by the metropolitan area and calculate the average win/loss ratio for cities with multiple teams 
    average_win_loss_by_region = nba_df.groupby('Metropolitan area')['WinLossRatio'].mean().reset_index() 
    # Merge the average win/loss ratio data with the city data based on the metropolitan area 
    merged_data = cities.merge(average_win_loss_by_region, on='Metropolitan area', how='inner') 
    
    raise NotImplementedError()
    
    population_by_region = merged_data['Population'].astype(float) # pass in metropolitan area population from cities
    win_loss_by_region = merged_data['WinLossRatio'] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    #assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    #assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for nba"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)
print(nba_df)
