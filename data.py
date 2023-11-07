# TODO: Clean up all data (for salaries, drop the zip code at end of city name, etc)
# Add to consistency of data for both sets / general data processing
import pandas as pd
import numpy as np


def read_data(filename,area):
    df = pd.read_csv(filename)
    #print(df)
    df['city'] = df[area].str.extract(r'^(.*?)(?:-[^,]*)?,', expand=False)
    df['state_id'] = df[area].str.extract(r'([A-Z]{2})(?:[^,]*)?\(', expand=False)
    
    # Remove any leading or trailing whitespace
    df['city'] = df['city'].str.strip()
    df['state_id'] = df['state_id'].str.strip()
    
    # Modify city and state_id names further
    df['city'] = df['city'].str.split('-').str[0]  # Keep only the part before the first dash
    df['state_id'] = df['state_id'].str.split('-').str[0]  # Keep only the part before the first dash
    
    # Display the resulting DataFrame
    #print(df[['City', 'State']])

    #print(df[['City', 'State']])

    return df


def read_data2(filename,area):
    df = pd.read_csv(filename)
    #print(df)
    df['city'] = df[area].str.extract(r'^(.*?)(?:-[^,]*)?,', expand=False)
    df['state_id'] = df['StateName']#.str.extract(r'([A-Z]{2})(?:[^,]*)?\(', expand=False)
    
    # Remove any leading or trailing whitespace
    df['city'] = df['city'].str.strip()
    df['state_id'] = df['state_id'].str.strip()
    
    # Modify city and state_id names further
    df['city'] = df['city'].str.split('-').str[0]  # Keep only the part before the first dash
    df['state_id'] = df['state_id'].str.split('-').str[0]  # Keep only the part before the first dash
    
    # Display the resulting DataFrame
    #print(df[['City', 'State']].dropna())
    #print(df[['City', 'State']])

    return df


df = read_data("data/OES_Report.csv",'Area Name')
df2 = read_data2("data/Metro_zori_sm_month.csv","RegionName")

merged_df = pd.merge(df, df2, on=['city', 'state_id'], how='outer')

# Go through the columns in the merged_df and change all "-" to NaN to be dropped later.
for column in merged_df.columns:
    merged_df[column] = merged_df[column].apply(lambda x: np.nan if str(x).strip() == '-' else x)

loc_df = pd.read_csv("data/simplemaps_uscities_basicv1/uscities.csv")

final_df = pd.merge(merged_df, loc_df, on=['city', 'state_id']).dropna(subset=['Area Name', 'Annual median wage(2)'])

# Display the resulting DataFrame
# print(merged_df[['city', 'state_id','Annual median wage(2)','2022-05-31']].dropna())
print(final_df[['city', 'state_id','lat', 'lng', 'Annual median wage(2)', '2022-05-31']])
final_df.to_csv("data/clean_data.csv")
