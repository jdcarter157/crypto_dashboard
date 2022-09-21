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

dash.register_page(__name__)





def update_city_selected(input_value):
    return f'You selected: {input_value}'





layout = html.Div([
    html.H4('Life expentancy progression of countries per continents!!!!!!!!'),
    dcc.Graph(id="graph2", figure={"layout": {"height": 300, "width": 700}, }),


    html.Div(dcc.Input(id='input-box2', type='text')),
    html.Button('Submit', id='button-example-2'),
    html.Div(id='output-container-button2',
             children='Enter a value and press submit'),
])

@dash.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('button-example-2', 'n_clicks')],
    [dash.dependencies.State('input-box2', 'value')])
def update_output(n_clicks, value):
    print(" number of clicks", n_clicks)
    print(" value-->", value)

    crypto_name = value
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from coin_data WHERE cname = %s", (crypto_name,))
    myresult = mycursor.fetchall()

    pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])

    mycursor.execute("SELECT cdate from coin_data WHERE cname = %s", (crypto_name,))
    myresult = mycursor.fetchall()

    datelist = []
    for x in myresult:
        datelist = x

    crypto_name = value
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from coin_data WHERE cname = %s", (crypto_name,))
    myresult = mycursor.fetchall()

    print(myresult)

    pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])

    pd.set_option('display.max_rows', None)

    print(pd1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pd1.cdate, y=pd1.lows,
                             mode='lines',
                             name='lines'))

    fig.add_trace(go.Scatter(x=pd1.cdate, y=pd1.price,
                             mode='lines',
                             name='lines'))

    fig.add_trace(go.Scatter(x=pd1.cdate, y=pd1.highs,
                             mode='lines',
                             name='lines'))

    return fig

