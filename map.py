from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import re


from urllib.request import urlopen
import json

def create_map():
        
    app = Dash(__name__)

    # with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    #     counties = json.load(response)
    # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    #                    dtype={"fips": str})
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')

    # df = pd.read_csv('./data/simplemaps_uscities_basicv1/uscities.csv')
    df = pd.read_csv('./data/clean_data.csv')

    city_selection = [None, None]

    # Create "text" column as string of information
    df['text'] = df['city'] + ', ' + df['state_id'] + ': $' + df['Annual median wage(2)'].astype(str)

    fig = go.Figure(data=go.Scattergeo(
        lon = df['lng'],
        lat = df['lat'],
        text = df['text'],
        mode = 'markers',
        # marker_color = df['cnt'],
        ))

    fig.update_layout(
        title = 'US Cities',
        geo_scope='usa',
        width=1200,
        height=600,
        margin=dict(l=5, r=5, t=30, b=5),
        paper_bgcolor="LightSteelBlue",
    )

    app.layout = html.Div([
        html.H1('Salary vs. Rent Comparison Tool'),
        dcc.Graph(id="graph", figure=fig),
        html.P(id="text"),
        html.Div(id="compare")
    ])


    @app.callback(
        Output("text", "children"), 
        Input("graph", "clickData"))
    def select(clickData):

        # Update city selections
        if len(city_selection) < 2:
            city_selection.append(clickData)
        else:
            city_selection.pop(0)
            city_selection.append(clickData)
        # print(city_selection[0])
        # print(city_selection[1])
        # print("\n")

        if(clickData == None):
            return "Make a selection"
        else:
            return clickData["points"][0]["text"]


    @app.callback(
        Output("compare","children"),
        Input("graph", "clickData"))
    def compare(x):
        if city_selection[0] == None or city_selection[1] == None:
            return "Select another city to compare"

        # Parse city and state names out of selection
        city1 = re.split(r'(,+|:+)', city_selection[0]["points"][0]["text"])
        city2 = re.split(r'(,+|:+)', city_selection[1]["points"][0]["text"])

        #TODO: search by city AND state. There are duplicate city names
        city1 = df.loc[df['city'] == city1[0]]
        city2 = df.loc[df['city'] == city2[0]]


        string1 = city1["city"] + " has a salary of " + city1["Annual median wage(2)"].astype(str)
        string2 = city2["city"] + " has a salary of " + city2["Annual median wage(2)"].astype(str)

        #TODO: the comparison section could obviously use some changes
        return [
            html.P(string1),
            html.P(string2)
        ]
        
    return app

    # {
    #   "points": [
    #     {
    #       "curveNumber": 0,
    #       "pointNumber": 30348,
    #       "pointIndex": 30348,
    #       "lon": -94.9848,
    #       "lat": 39.4791,
    #       "location": null,
    #       "text": "Iatan, MO",
    #       "bbox": {
    #         "x0": 589.775741890541,
    #         "x1": 595.775741890541,
    #         "y0": 304.1862505916832,
    #         "y1": 310.1862505916832
    #       }
    #     }
    #   ]
    # }