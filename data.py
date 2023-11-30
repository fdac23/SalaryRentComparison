import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re

from dash import dcc


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


def clean_data():
    df = read_data("data/OES_Report.csv",'Area Name')
    df2 = read_data2("data/Metro_zori_sm_month.csv","RegionName")

    merged_df = pd.merge(df, df2, on=['city', 'state_id'], how='outer')

    # Go through the columns in the merged_df and change all "-" to NaN to be dropped later.
    for column in merged_df.columns:
        merged_df[column] = merged_df[column].apply(lambda x: np.nan if str(x).strip() == '-' else x)

    loc_df = pd.read_csv("data/simplemaps_uscities_basicv1/uscities.csv")

    final_df = pd.merge(merged_df, loc_df, on=['city', 'state_id']).dropna(subset=['Area Name', 'Annual median wage(2)','2022-05-31'])

    # Display the resulting DataFrame
    # print(merged_df[['city', 'state_id','Annual median wage(2)','2022-05-31']].dropna())
    # print(final_df[['city', 'state_id','lat', 'lng', 'Annual median wage(2)', '2022-05-31']])
    final_df.to_csv("data/clean_data.csv")


"""
Compares the median wages between two selected cities.

Args:
    name1 (str): Name of the first city
    wage1 (str): Median wage of the first city
    name2 (str): Name of the second city
    wage2 (str): Median wage of the second city

Returns:
    dcc.Graph: A bar graph comparing the median wages of the two cities for easy comparison
"""
def compare_cities_median_wage(name1, wage1, name2, wage2):
    areas = [name2, name1]
    wage1 = int(wage1)
    wage2 = int(wage2)
    wages = [wage2, wage1]
    
    trace = go.Bar(
        x=areas,
        y=wages,
        marker=dict(color='red')  # Change color as needed
    )

    layout = go.Layout(
        title='Annual Median Wage Comparison',
        xaxis=dict(title='City'),
        yaxis=dict(title='Annual Median Wage')
    )

    fig = go.Figure(data=[trace], layout=layout)
    fig.update_layout(height=400, width=500)

    return dcc.Graph(figure=fig)

  
"""
Compare the monthly rent between two selected cities.

Args:
    name1 (str): Name of the first city
    rent1 (str): Monthly rent of the first city
    name2 (str): Name of the second city
    rent2 (str): Monthly rent of the second city

Returns:
    dcc.Graph: A bar graph comparing the monthly rent of the two cities for easy comparison
"""
def compare_cities_rent(name1, rent1, name2, rent2):
    areas = [name2, name1]
    rent1 = float(rent1)
    rent2 = float(rent2)
    rents = [rent2, rent1]
    
    trace = go.Bar(
        x=areas,
        y=rents,
        marker=dict(color='green')  # Change color as needed
    )

    layout = go.Layout(
        title='Monthly Rent Comparison',
        xaxis=dict(title='City'),
        yaxis=dict(title='Monthly Rent')
    )

    fig = go.Figure(data=[trace], layout=layout)
    fig.update_layout(height=400, width=500)

    return dcc.Graph(figure=fig)


"""
Compares the ratio of rent to monthly wage between two selected cities.

Args:
    name1 (str): Name of the first city
    wage1 (str): Median wage of the first city
    rent1 (str): Monthly rent of the first city
    name2 (str): Name of the second city
    wage2 (str): Median wage of the second city
    rent2 (str): Monthly rent of the second city

Returns:
    dcc.Graph: A bar graph comparing the ratio of monthly rent to median wage of the two cities for easy comparison
"""
def compare_cities_ratio(name1, wage1, rent1, name2, wage2, rent2):
    areas = [name2, name1]
    ratio1 = float(float(rent1)*12/float(wage1))
    ratio2 = float(float(rent2)*12/float(wage2))
    rentPerc = [ratio2, ratio1]
    
    trace = go.Bar(
        x=areas,
        y=rentPerc,
        marker=dict(color='blue')  # Change color as needed
    )

    layout = go.Layout(
        title='Rent to Wage Ratio Comparison',
        xaxis=dict(title='City'),
        yaxis=dict(title='Rent / Income')
    )

    fig = go.Figure(data=[trace], layout=layout)
    fig.update_layout(height=400, width=500)

    return dcc.Graph(figure=fig)


"""
Compare the wage percentiles between two selected cities. Includes the 10th, 25th, 50th, 75th, and 90th percentiles.

Args:
    name1 (str): Name of the first city
    median1 (str): Median wage of the first city
    _10th_percentile1 (str): 10th percentile wage of the first city
    _25th_percentile1 (str): 25th percentile wage of the first city
    _75th_percentile1 (str): 75th percentile wage of the first city
    _90th_percentile1 (str): 90th percentile wage of the first city
    name2 (str): Name of the second city
    median2 (str): Median wage of the second city
    _10th_percentile2 (str): 10th percentile wage of the second city
    _25th_percentile2 (str): 25th percentile wage of the second city
    _75th_percentile2 (str): 75th percentile wage of the second city
    _90th_percentile2 (str): 90th percentile wage of the second city

Returns:
    dcc.Graph: Graph containing two boxplots comparing the wage percentiles of the two cities
"""
def compare_cities_percentiles(name1, median1, _10th_percentile1, _25th_percentile1, _75th_percentile1, _90th_percentile1, 
                     name2, median2, _10th_percentile2, _25th_percentile2, _75th_percentile2, _90th_percentile2):
    data = {
        'City': [name2, name2, name2, name2, name2, name1, name1, name1, name1, name1],
        'Percentile': ['10th', '25th', '50th', '75th', '90th', '10th', '25th', '50th', '75th', '90th'],
        'Wage': [_10th_percentile2, _25th_percentile2, median2, _75th_percentile2, _90th_percentile2, _10th_percentile1, _25th_percentile1, median1, _75th_percentile1, _90th_percentile1]  
    }
    
    df = pd.DataFrame(data)

    fig = px.box(df, x='City', y='Wage', color='City',
                title='Annual Wages Percentiles Comparison',
                points='all', hover_data=['Percentile', 'Wage'],
                boxmode='overlay', color_discrete_sequence=['red', 'blue'])

    return dcc.Graph(figure=fig)


"""
Extracts different characteristics from the text data. For example, extracts the city and state, median wage, monthly rent, etc.

Args:
    text (str): Text data to extract from (comes from the point on the map)

Returns:
    All extracted data (name, wage, rent, percentiles)
"""
def extract_text_data(text):    
    # Get everything separated by commas except for the first one (city, state)
    pattern = r'([^,]+,\s*[A-Z]{2}),\s*(.*),(.*),(.*),(.*),(.*),(.*)'
    matches = re.match(pattern, text)

    if matches:
        name = matches.group(1)  # Extract city and state together
        wage = matches.group(2)  # Extract the first numerical value
        rent = matches.group(3)  # Extract the second numerical value
        _10th_percentile = matches.group(4)
        _25th_percentile = matches.group(5)
        _75th_percentile = matches.group(6)
        _90th_percentile = matches.group(7)
        return name, wage, rent, _10th_percentile, _25th_percentile, _75th_percentile, _90th_percentile
    
    return "No matches found..."


"""
Plots the trends of rental pricing for the two selected cities. Also plots the average rental pricing across the US.

Args:
    data1 (dict): Dictionary containing the data for the first city
    data2 (dict): Dictionary containing the data for the second city
    wanted_rent_columns (list): List of the columns to extract from the rental data

Returns:
    dcc.Graph: Graph containing the rental trends for the two cities and the average rental trend across the US
"""
def rent_trend_plot(data1, data2, wanted_rent_columns):
    city_1_name = list(data1.values())[0] + ", " + list(data1.values())[1]
    city_2_name = list(data2.values())[0] + ", " + list(data2.values())[1]
    plot_name = "Monthly Rent Comparison: " + city_1_name + " vs. " + city_2_name
    
    average_rent_trend = get_rent_trend_across_us(wanted_rent_columns)
    
    city1_plot = go.Scatter(
        x=list(data1.keys())[2:],
        y=list(data1.values())[2:],
        mode='lines+markers',
        name=city_1_name,
    )
    
    city2_plot = go.Scatter(
        x=list(data2.keys())[2:],
        y=list(data2.values())[2:],
        mode='lines+markers',
        name=city_2_name,
    )
    
    avg_plot = go.Scatter(
        x=list(average_rent_trend.keys()),
        y=list(average_rent_trend.values()),
        mode='lines+markers',
        name="Average Rent Across US",
    )
    
    fig = go.Figure(data=[city1_plot, city2_plot, avg_plot])
    
    fig.update_layout(
        title=plot_name,
        xaxis_title="Date",
        yaxis_title="Monthly Rent ($)",
    )
    
    return dcc.Graph(figure=fig)


"""
Get the average rent trend across the US.

Args:
    wanted_rent_columns (list): List of the columns to extract from the rental data

Returns:
    dict: Dictionary containing the average rent trend across the US from 2015-2022
"""
def get_rent_trend_across_us(wanted_rent_columns):
    df = pd.read_csv("./data/clean_data.csv")
    
    rent_dates_data = wanted_rent_columns[2:]
    df_all_rent_dates = df[rent_dates_data]
    average_rent_trend = df_all_rent_dates.mean()
    
    return average_rent_trend.to_dict()