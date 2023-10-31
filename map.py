from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


from urllib.request import urlopen
import json

app = Dash(__name__)

# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)
# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
#                    dtype={"fips": str})
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')

df = pd.read_csv('./data/simplemaps_uscities_basicv1/uscities.csv')

df['text'] = df['city'] + ', ' + df['state_id']

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
)

app.layout = html.Div([
    html.H4('Dot map of cities'),
    dcc.Graph(id="graph", figure=fig),
    html.P(id="text")
])


@app.callback(
    Output("text", "children"), 
    Input("graph", "clickData"))
def display_selection(clickData):
    if(clickData == None):
        return "Make a selection"
    else:
        print(clickData)
        return clickData["points"][0]["text"]

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

if __name__ == '__main__':
    app.run_server(debug=True)