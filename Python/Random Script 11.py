import pandas as pd
import numpy as np

# Load Energy dataset
Energy = pd.read_excel('assets/Energy Indicators.xls', header=None, skipfooter=2)
Energy = Energy.iloc[17:244, 2:]
Energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x * 1000000 if x != '...' else np.nan)
Energy['Country'] = Energy['Country'].str.replace(r'\(.*\)|[0-9]+', '', regex=True)
Energy['Country'] = Energy['Country'].replace({"Republic of Korea": "South Korea",
                                               "United States of America": "United States",
                                               "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                               "China, Hong Kong Special Administrative Region": "Hong Kong"})

# Load GDP dataset
GDP = pd.read_csv('assets/world_bank.csv', skiprows=4)
GDP['Country Name'] = GDP['Country Name'].replace({"Korea, Rep.": "South Korea",
                                                   "Iran, Islamic Rep.": "Iran",
                                                   "Hong Kong SAR, China": "Hong Kong"})

# Load ScimEn dataset
ScimEn = pd.read_excel('assets/scimagojr-3.xlsx')

# Merge the three datasets
data = pd.merge(ScimEn, Energy, how='inner', left_on='Country', right_on='Country')
data = pd.merge(data, GDP, how='inner', left_on='Country', right_on='Country Name')

# Keep only the last 10 years of GDP data (2006-2015)
columns_to_keep = ['Country', 'Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                   'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable',
                   '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
data = data[columns_to_keep]

# Set 'Country' as the index and sort by 'Rank'
data = data.set_index('Country').sort_values(by='Rank')

# Keep only the top 15 countries by 'Rank'
data = data.head(15)

# Return the final DataFrame
def answer_one():
    return data

answer_one()
