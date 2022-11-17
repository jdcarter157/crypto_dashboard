import mysql.connector
import dash_daq as daq
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


from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import random
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

import dash
from dash import html, dcc, callback, Input, Output

mydb = mysql.connector.connect(
    host="192.168.0.122",
    user="crypto",
    password="crypto",
    auth_plugin="mysql_native_password",
    database="coindata"
)




# connect to db
# mydb = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#
#    database="ecoins"
# )

mycursor = mydb.cursor()
mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES LIMIT 100")
# coinlist = mycursor.fetchall()
# print(coinlist)
# mycursor.execute("SHOW TABLES")
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
    mycursor.execute('SELECT * FROM ' + x[0] + ' LIMIT 1')
    cname=mycursor.fetchall()
    try:
        var=json.loads(cname[0][2])
        if "/" in var:
            var = var.split('/')[0]
        # print("description:",var['description'])
        coinlistdrop.append(x[0])
        coinlistdrop2.append(x[0]+" "+var['description'])
    except:pass
    # print(coinlistdrop)

    # for y in x:
    #     x=str(x)
    #     mycursor.execute('SELECT * FROM ' + x + ' LIMIT 100')
    #
    #     d=json.loads(y)
    #
    #     coinlistdrop2.append(x[0],d['description'])
    #
    #     # print(d['name'])
coinlistdrop=list(set(coinlistdrop))
# print(coinlistdrop2)
dash.register_page(__name__)
# print("searching hit")
options = [{'label': coinlistdrop2[i], 'value':coinlistdrop[i]} for i in range(len(coinlistdrop2))]

layout = html.Div([

    html.H1("Search Coins:"),


        # html.I(
        #     "Search for coins by typing:"),
        #
        # html.Br(),
        # html.Br(),
        # dcc.Input(id="input1", type="text", placeholder="", style={'marginRight': '10px'}),

        # html.Div(id="output"),
        # html.Div(id='dd-output-container'),

        html.Br(),
        html.Br(),
        html.I(
            "Search for coins by dropdown:"),
        html.Button('Submit',id='drop-submit2'),
dcc.Dropdown(
    options=options,
    id='demo-dropdown2',
    value='bitmex_ethusd_eth'
),

        # dcc.Dropdown(id='coins-dropdown'),

        html.Div(id='display-selected-values2'),


    dcc.Graph(id="search_graph2", figure={"layout": {"height": 300, "width": 700}, }),

])
def update_output(input1 ):
    crypto_name = input1
    match_ratios = process.extract(crypto_name, coinlist, scorer=fuzz.token_sort_ratio)
    # print("match ratio",match_ratios[0])
    best_match = process.extractOne(crypto_name, coinlist, scorer=fuzz.token_sort_ratio)
    # print("best match:",best_match[0])

    return f'Output: {match_ratios[:5]}'

    # return u'Input : {} '.format(input1)

@dash.callback(

    dash.dependencies.Output('search_graph2', 'figure'),
    [dash.dependencies.Input('demo-dropdown2', 'value')])
def update_graph(value):
    # print(" value-->", value)
    # VALUE IS FROM HTML FORM INPUT
    crypto_name = value
    print("cryptoname",crypto_name)
    # QUERY DATA FROM DB
    mycursor.execute('SELECT * FROM '+crypto_name+' LIMIT 100')

    myresult = mycursor.fetchall()
    # print(myresult)
    # SETTING COLLUMNS FOR DF
    pd1 = pd.DataFrame(myresult, columns=['id', 'date', 'low'])
    pd.set_option('display.max_rows', None)
    # print(type(pd1.low))
    # print("time",pd1.date)
    # print(pd1)
    # print(pd1)
    # CREATING FIGURE FOR WEB DISPLAY
    # print(pd1.low[0])
    lowdata=[]
    for x in pd1.low:
        d=json.loads(x)
        lowdata.append(d['low'])

        # print(d['name'])

    fig = px.scatter(pd1,
                  x=pd1.date, y=lowdata, trendline='ols')
    #
    # fig.update_layout(
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     font_color='WHITE'
    # )


    return fig



