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
import dash_daq as daq

from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import random

# # connect to db
# mydb = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#
#    database="ecoins"
# )
mydb = mysql.connector.connect(
    host="192.168.0.122",
    user="crypto",
    password="crypto",
    auth_plugin="mysql_native_password",
    database="coindata"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES LIMIT 10 ")

# mycursor.execute("SELECT distinct cname from coin_data order by cdate")
coinlist = mycursor.fetchall()
coinlistdrop = []
coinlistdrop2=[]
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

# print ( coinlist )
testlist = []
for x in coinlist:
    testlist.append(x[0])

# print ( testlist )

dash.register_page(__name__)

def update_city_selected(input_value):
    return f'You selected: {input_value}'

layout = html.Div([

    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div([
    ]),

    html.H4('Life expentancy progression of countries per continents!!!!!!!!'),
    dcc.Graph(id="graph", figure={"layout": {"height": 300, "width": 700}, }),

    html.Div(id='output-container-button',
             children=''),
    dcc.Input(id='input-2-state', type='text', value='2021-06-21'),
    dcc.Input(id='input-3-state', type='text', value='2023-06-22'),
    html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
    dcc.Dropdown(
    options=options,
    id='line-dropdown',
    value='bitmex_ethusd_eth',
    placeholder="bitmex_ethusd_eth"
),
])

@dash.callback(dash.dependencies.Output('graph', 'figure'),
              dash.dependencies.Input('submit-button-state', 'n_clicks'),
              dash.dependencies.State('input-2-state', 'value'),
              dash.dependencies.State('input-3-state', 'value'),
               [dash.dependencies.Input('line-dropdown', 'value')]
               )
def update_output( n_clicks,input2, input3,val):
    crypto_name = val
    crypto_date1 = input2
    crypto_date2 = input3
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from "+crypto_name+ " WHERE date > %s AND date < %s order by date", (crypto_date1, crypto_date2,))
    myresult = mycursor.fetchall()
    price_data=[]

  #  pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])
    pd1 = pd.DataFrame(myresult, columns=['id','date', 'price'])
    for x in pd1.price:
        d=json.loads(x)
        price_data.append(d['low'])

    # print ( pd1.to_string() )

    pd.set_option('display.max_rows', None)

    fig = px.line(pd1,
                  x="date", y=price_data)

    # print ( pd1 )

    return fig
