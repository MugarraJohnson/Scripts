nhl_df = nhl_df[nhl_df['year'] == 2018]
nhl_df["team"] = nhl_df["team"].apply(lambda x: x.strip ())
nhl_df["team"] = nhl_df["team"].apply(lambda x: re.sub(r"Â|\*|\s\(\d+\)$", "", x))
