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
#
# # connect to db
# mydb = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#
#    database="ecoins"
# )

mydb = mysql.connector.connect(
    host="",
    user="crypto",
    password="",
    auth_plugin="mysql_native_password",
    database=""
)

dash.register_page(__name__)


def update_city_selected(input_value):
    return f'You selected: {input_value}'


mycursor = mydb.cursor()
mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES LIMIT 10 ")
coinlist = mycursor.fetchall()
coinlistdrop = []
coinlistdrop2=[]
coinlist=list(set(coinlist))
for x in (coinlist):
    # print(x)
    # for i in x:
    #     # print(i)
    #     v=x[0]+" - "+x[1]
# print(coinlistdrop)
    # coinlistdrop.append(coinlist[x])
    # print("table name:", x[0])
    try:
        mycursor.execute('SELECT * FROM ' + x[0] + ' LIMIT 1')
        cname=mycursor.fetchall()

        var=json.loads(cname[0][2])
        if "/" in var:
            var = var.split('/')[0]
        # print("description:",var['description'])
        coinlistdrop.append(x[0])
        coinlistdrop2.append(x[0]+" -"+var['description'])
    except:pass

coinlistdrop=list(set(coinlistdrop))

options = [{'label': coinlistdrop2[i], 'value':coinlistdrop[i]} for i in range(len(coinlistdrop2))]


layout = html.Div([

    html.Div(id='coinsearch',
             children=''),
    dcc.Input(id='input-coin-state', type='text', value=''),
    html.Button(id='coin-button-state', n_clicks=0, children='Search Coins'),
    html.Div(id='coin-output-state'),

    html.H4('Life expentancy progression of countries per continents!!!!!!!!'),
    dcc.Graph(id="graph11", figure={"layout": {"height": 300, "width": 700}, }),

    html.Div(id='output-container-button10',
             children=''),
    dcc.Input(id='input-11-state', type='text', value='2022-06-21'),
    dcc.Input(id='input-12-state', type='text', value='2022-06-22'),
    html.Button(id='submit-button-state10', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
    dcc.Dropdown(
    options=options,
    id='hl-dropdown',
    value='bitmex_ethusd_eth',
    placeholder="bitmex_ethusd_eth"
),

])



@dash.callback(
    dash.dependencies.Output('graph11', 'figure'),
    dash.dependencies.Input('submit-button-state10', 'n_clicks'),
    dash.dependencies.State('input-11-state', 'value'),
    dash.dependencies.State('input-12-state', 'value'),
    [dash.dependencies.Input('hl-dropdown', 'value')]
)


def update_output(n_clicks, input2, input3,val):
    crypto_name = val
    crypto_date1 = input2
    crypto_date2 = input3

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * from "+  crypto_name + " WHERE date > %s AND date < %s limit 100", (crypto_date1, crypto_date2,))
    myresult = mycursor.fetchall()

    pd1 = pd.DataFrame(myresult, columns=['id', 'cdate', 'price',])

    pd.set_option('display.max_rows', None)
    low_data=[]
    for x in pd1.price:
        d=json.loads(x)
        low_data.append(d['low'])

    high_data=[]
    for x in pd1.price:
        d=json.loads(x)
        high_data.append(d['high'])
    price_data=[]
    for x in pd1.price:
        d=json.loads(x)
        price_data.append(d['close'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=pd1.cdate, y=low_data,
                             mode='lines',
                             name='low'))

    fig.add_trace(go.Scatter(x=pd1.cdate, y=price_data,
                             mode='lines',
                             name='close'))

    fig.add_trace(go.Scatter(x=pd1.cdate, y=high_data,
                             mode='lines',
                             name='high'))

    return fig

