import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import flask
import pandas as pd
from daten_ziehen import get_data

import time
import os
######

server = flask.Flask('app')

global dff
dff = pd.read_csv("data.csv", index_col=0)

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False

app.layout = html.Div([
    html.H1('Strava '),
    html.Button("Scrapen!", id="scraper", n_clicks=0),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Radfahrt', 'value': 'Radfahrt'},
            {'label': 'Lauf', 'value': 'Lauf'},
        ],
        value='Lauf'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value'),
               Input("scraper", "n_clicks")])
def update_graph(selected_dropdown_value, scraper):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    if "scraper" in changed_id:
        df = get_data()
        fig = px.scatter(
            df, x="Date", y="Distance")
        return fig
    else:
        dff = pd.read_csv("data.csv", index_col = 0)
        dff = dff[dff['Type'] == selected_dropdown_value]
        print(dff)
        fig= px.scatter(
            dff, x="Date", y="Distance")
        return fig
if __name__ == '__main__':
    app.run_server()




