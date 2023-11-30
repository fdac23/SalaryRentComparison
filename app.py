from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from data import clean_data
from map import create_map

def run_app():
    clean_data()
    _map = create_map()
    _map.run_server(debug=True)
    

if __name__ == "__main__":
    run_app()