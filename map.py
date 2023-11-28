from dash import Dash, dcc, html, Input, Output
from data import compare_cities_median_wage, compare_cities_ratio, compare_cities_rent, compare_cities_percentiles, extract_text_data, rent_trend_plot
from urllib.request import urlopen

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def create_map():
    app = Dash(__name__)

    # with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    #     counties = json.load(response)
    # df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
    #                    dtype={"fips": str})
    # df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')

    # df = pd.read_csv('./data/simplemaps_uscities_basicv1/uscities.csv')
    df = pd.read_csv('./data/clean_data.csv')
  
    wanted_rent_columns = [
        'city', 'state_id',
        '2015-01-31', '2015-02-28', '2015-03-31', '2015-04-30', '2015-05-31', '2015-06-30', '2015-07-31', '2015-08-31', '2015-09-30', '2015-10-31', '2015-11-30', '2015-12-31',
        '2016-01-31', '2016-02-29', '2016-03-31', '2016-04-30', '2016-05-31', '2016-06-30', '2016-07-31', '2016-08-31', '2016-09-30', '2016-10-31', '2016-11-30', '2016-12-31',
        '2017-01-31', '2017-02-28', '2017-03-31', '2017-04-30', '2017-05-31', '2017-06-30', '2017-07-31', '2017-08-31', '2017-09-30', '2017-10-31', '2017-11-30', '2017-12-31',
        '2018-01-31', '2018-02-28', '2018-03-31', '2018-04-30', '2018-05-31', '2018-06-30', '2018-07-31', '2018-08-31', '2018-09-30', '2018-10-31', '2018-11-30', '2018-12-31',
        '2019-01-31', '2019-02-28', '2019-03-31', '2019-04-30', '2019-05-31', '2019-06-30', '2019-07-31', '2019-08-31', '2019-09-30', '2019-10-31', '2019-11-30', '2019-12-31',
        '2020-01-31', '2020-02-29', '2020-03-31', '2020-04-30', '2020-05-31', '2020-06-30', '2020-07-31', '2020-08-31', '2020-09-30', '2020-10-31', '2020-11-30', '2020-12-31',
        '2021-01-31', '2021-02-28', '2021-03-31', '2021-04-30', '2021-05-31', '2021-06-30', '2021-07-31', '2021-08-31', '2021-09-30', '2021-10-31', '2021-11-30', '2021-12-31',
        '2022-01-31', '2022-02-28', '2022-03-31', '2022-04-30', '2022-05-31'
    ]

    city_selection = [None, None]

    # Create "text" column as string of information
    df['text'] = df['city'] + ', ' + df['state_id'] + ',' + (df['Annual median wage(2)']).astype(str) + ',' + round(df['2022-05-31'], 2).astype(str) + ',' + (df['Annual 10th percentile wage(2)']).astype(str) + ',' + (df['Annual 25th percentile wage(2)']).astype(str) + ',' + (df['Annual 75th percentile wage(2)']).astype(str) + ',' + (df['Annual 90th percentile wage(2)']).astype(str)
    df['hover_text'] = df['city'] + ', ' + df['state_id'] + '<br>' + 'Rent/Salary Ratio: ' + round((df['2022-05-31']*12/df['Annual median wage(2)'])*100, 3).astype(str) + '%'
    
    # Getting all rent data up to May 2022 for each city. Stores the Key with its corresponding value to be passed as customdata.
    rent_data = []
    for i, row in df.iterrows():
        rent_data_dict = {}
        for col_name in wanted_rent_columns:
            rent_data_dict[col_name] = row[col_name]
        rent_data.append(rent_data_dict)
    
    fig = go.Figure(data=go.Scattergeo(
        lon = df['lng'],
        lat = df['lat'],
        text = df['text'],
        hovertext=df['hover_text'],
        customdata=rent_data,
        mode = 'markers',
        marker_size = df['2022-05-31']*12/df['Annual median wage(2)']*100,
        marker_color = df['2022-05-31']*12/df['Annual median wage(2)']*100,
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
        html.H1('Salary vs. Rent Comparison Tool', style={'display': 'flex', 'justify-content': 'center'}),
        html.Div(dcc.Graph(id="graph", figure=fig), style={'display': 'flex', 'justify-content': 'center'}),
        html.Div(style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-evenly'}, children = [
            html.P(id="select"),
            html.P(id="compare"),
        ]),
        html.Div(style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}, children = [
            html.P(id="compare_chart"),
        ])
    ])


    @app.callback(
        Output("select", "children"), 
        Input("graph", "clickData"))
    def select(clickData):
        # Update city selections
        if len(city_selection) < 2:
            city_selection.append(clickData)
        else:
            city_selection.pop(0)
            city_selection.append(clickData)

        if(clickData == None):
            return "Make a selection"
        else:
            name, wage, rent, _, _, _, _ = extract_text_data(clickData["points"][0]["text"])
            return [
                html.P(html.B(name)),
                html.P("Median Wage: $" + wage),
                html.P("Monthly Rent: $" + rent),
                html.P("Percent of Income Spent on Rent: " + str(round((float(rent)*12/float(wage))*100, 3)) + "%")
            ]   


    @app.callback(
        Output("compare","children"),
        Input("graph", "clickData"))
    def compare(x):
        if city_selection[0] == None or city_selection[1] == None:
            return "Select another city to compare"
        
        name, wage, rent, _, _, _, _ = extract_text_data(city_selection[0]["points"][0]["text"])
        return [
            html.P(html.B(name)),
            html.P("Median Wage: $" + wage),
            html.P("Monthly Rent: $" + rent),
            html.P("Percent of Income Spent on Rent: " + str(round((float(rent)*12/float(wage))*100, 3)) + "%")
        ]  
    

    @app.callback(
        Output("compare_chart","children"),
        Input("graph", "clickData"))
    def compare_chart(x):
        if city_selection[0] == None or city_selection[1] == None:
            return "Select another city to view comparison chart"

        name1, wage1, rent1, _10th_percentile1, _25th_percentile1, _75th_percentile1, _90th_percentile1 = extract_text_data(city_selection[0]["points"][0]["text"])
        name2, wage2, rent2, _10th_percentile2, _25th_percentile2, _75th_percentile2, _90th_percentile2 = extract_text_data(city_selection[1]["points"][0]["text"])
        
        
        wage_plot = compare_cities_median_wage(name1, wage1, name2, wage2)
        rent_plot = compare_cities_rent(name1, rent1, name2, rent2)
        ratio_plot = compare_cities_ratio(name1, wage1, rent1, name2, wage2, rent2)
        
        percentiles_plot = compare_cities_percentiles(name1, wage1, _10th_percentile1, _25th_percentile1, _75th_percentile1, _90th_percentile1, name2, wage2, _10th_percentile2, _25th_percentile2, _75th_percentile2, _90th_percentile2)    
        rent_price_trend_plot = rent_trend_plot(city_selection[0]["points"][0]["customdata"], city_selection[1]["points"][0]["customdata"], wanted_rent_columns)
        
        return[
            html.Div(style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}, children = [
                wage_plot,
                rent_plot,
                ratio_plot,
            ]),
            html.Div(style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'center'}, children = [
                percentiles_plot,
                rent_price_trend_plot,
            ])
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