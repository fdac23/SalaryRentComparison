# TODO: Clean up all data (for salaries, drop the zip code at end of city name, etc)
# Add to consistency of data for both sets / general data processing
import pandas as pd


def read_data(filename,area):
    df = pd.read_csv(filename)
    #print(df)
    df['City'] = df[area].str.extract(r'^(.*?)(?:-[^,]*)?,', expand=False)
    df['State'] = df[area].str.extract(r'([A-Z]{2})(?:[^,]*)?\(', expand=False)
    
    # Remove any leading or trailing whitespace
    df['City'] = df['City'].str.strip()
    df['State'] = df['State'].str.strip()
    
    # Modify city and state names further
    df['City'] = df['City'].str.split('-').str[0]  # Keep only the part before the first dash
    df['State'] = df['State'].str.split('-').str[0]  # Keep only the part before the first dash
    
    # Display the resulting DataFrame
    #print(df[['City', 'State']])

    #print(df[['City', 'State']])

    return df


df = read_data("data/OES_Report.csv",'Area Name')

def read_data2(filename,area):
    df = pd.read_csv(filename)
    #print(df)
    df['City'] = df[area].str.extract(r'^(.*?)(?:-[^,]*)?,', expand=False)
    df['State'] = df['StateName']#.str.extract(r'([A-Z]{2})(?:[^,]*)?\(', expand=False)
    
    # Remove any leading or trailing whitespace
    df['City'] = df['City'].str.strip()
    df['State'] = df['State'].str.strip()
    
    # Modify city and state names further
    df['City'] = df['City'].str.split('-').str[0]  # Keep only the part before the first dash
    df['State'] = df['State'].str.split('-').str[0]  # Keep only the part before the first dash
    
    # Display the resulting DataFrame
    #print(df[['City', 'State']].dropna())
    #print(df[['City', 'State']])

    return df


df2 = read_data2("data/Metro_zori_sm_month.csv","RegionName")

merged_df = pd.merge(df, df2, on=['City', 'State'], how='outer')

# Display the resulting DataFrame
print(merged_df[['City', 'State','Annual median wage(2)','2022-05-31']].dropna())
