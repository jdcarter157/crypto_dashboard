import dash
from dash import html, dcc, callback, Input, Output


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import pandas as pd
import numpy as np
import math
import time
from datetime import datetime
now = datetime.now()
import mysql.connector

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import random

# connect to db
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="ecoins"
)


layout = html.Div(children=[
    html.H1(children='This is our Analytics2 page!!!!!!!!!!!!!!!!'),

    html.Div(dcc.Input(id='input-box2', type='text')),
    html.Button('Submit', id='button-example-2'),

    html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Submit', id='button-example-1'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit!!!'),

    html.Div([
        dcc.Markdown("""
               **Click Data**

               Click on points in the graph.
           """),
        html.Pre(id='click-data'),
    ], className='three columns'),
])



def update_city_selected(input_value):
    return f'You selected: {input_value}'

layout = html.Div([
    html.H4('Life expentancy progression of countries per continents!!!!!!!!'),
    dcc.Graph(id="graph", figure={"layout": {"height": 300, "width": 700}, }),


    html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Submit', id='button-example-1'),
    html.Div(id='output-container-button',
             children='Enter a value and press submit'),
])

@dash.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('button-example-1', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks, value):
    print(" number of clicks", n_clicks)
    print(" value-->", value)

    crypto_name = value
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from coin_data WHERE cname = %s", (crypto_name,))
    myresult = mycursor.fetchall()

    print(myresult)

    pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])

    pd.set_option('display.max_rows', None)

    print(pd1)

    fig = px.line(pd1,
                  x="cdate", y="price")

    return fig