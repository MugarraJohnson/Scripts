mlb_df=pd.read_csv("assets/mlb.csv")
nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
cities.columns = ["Metropolitan area", "Population", "NFL", "MLB", "NBA", "NHL"]

# Use regular expressions to clean and standardize the values in the metropolitan area column
cities["Metropolitan area"] = cities["Metropolitan area"].apply(lambda x: re.sub(r"[^\w\s]", "", x)) # Remove punctuation
cities["Metropolitan area"] = cities["Metropolitan area"].apply(lambda x: re.sub(r"\s+", " ", x)) # Remove extra spaces
cities["Metropolitan area"] = cities["Metropolitan area"].apply(lambda x: x.strip()) # Remove leading and trailing spaces
cities["Metropolitan area"] = cities["Metropolitan area"].apply(lambda x: x.lower()) # Convert to lowercase

def sports_team_performance():
    # YOUR CODE HERE
    sports_data = {'NFL': nfl_df,'NBA': nba_df,'NHL': nhl_df,'MLB': mlb_df }
    
    #raise NotImplementedError()
    
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
    for sport1 in sports:
        for sport2 in sports:
            if sport1 == sport2:
                continue
            cities_with_sport1 = cities[cities[sport1].notna()]
            cities_with_sport2 = cities[cities[sport2].notna()]
            
            common_cities = set(cities_with_sport1['Metropolitan area']).intersection(cities_with_sport2['Metropolitan area'])
            
            if common_cities:
                p_value = np.nan
                # Group by the metropolitan area and calculate the average win-loss ratio for each metropolitan area
                data_sport1 = sports_data[sport1].groupby("team")["W"].mean().reset_index()
                data_sport2 = sports_data[sport2].groupby("team")["W"].mean().reset_index()
                # Merge the data by the metropolitan area column
                merged_data = cities_with_sport1.merge(data_sport1, left_on=sport1, right_on="team", how="inner")
                merged_data = merged_data.merge(data_sport2, left_on=sport2, right_on="team", how="inner")
                # Perform a t-test on the win-loss ratios of the two sports
                _, p = stats.ttest_rel(merged_data["W_x"], merged_data["W_y"])
                p_value = p
                p_values.loc[sport1, sport2] = p_value
                p_values.loc[sport2, sport1] = p_value
                
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values

p_values = sports_team_performance()
print("P-Values:")
print(p_values)
