

from sklearn.linear_model import LinearRegression


import dash
# from dash import html, dcc, callback, Input, Output


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

#DB CONN
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="ecoins"
)
#grabbing slopes for each coin to display onto dash
def bltc_slope():
    mycursor = mydb.cursor()
    # QUERY TO GRAB COIN
    mycursor.execute("SELECT * from coin_data WHERE cname = 'BITMEX:BLTC'")
    myresult = mycursor.fetchall()
    # CREATING DF
    pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])
    # line
    # CDATE IS OUR INDEPENDENT VAR
    pd1['cdate'] = pd.to_datetime(pd1['cdate'])
    # CHANGING DATE FORMAT TO ORDINAL
    pd1['cdate'] = pd1['cdate'].apply(lambda x: x.toordinal())
    # RESHAPING DATA FOR LIN-REG
    x = pd1['cdate'].to_numpy().reshape((-1, 1))
    # PRICE IS OUR DEPENDENT VAR
    y = pd1['price'].to_numpy()
    # CHOOSING A MODEL
    model = LinearRegression()
    # FITTING THE DATA TO MODEL
    model.fit(x, y)
    # MAKING SLOPE GLOBAL SO ALL 3 CAN BE DISPLAYED ON THIS PAGE
    global slope_bltc
    slope_bltc=str(model.coef_)


def eth_slope():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from coin_data WHERE cname = 'BITMEX:ETHUSD_ETH'")
    myresult = mycursor.fetchall()
    pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])
    # line
    pd1['cdate'] = pd.to_datetime(pd1['cdate'])
    pd1['cdate'] = pd1['cdate'].apply(lambda x: x.toordinal())
    x = pd1['cdate'].to_numpy().reshape((-1, 1))
    y = pd1['price'].to_numpy()
    model = LinearRegression()
    model.fit(x, y)
    global slope_eth
    slope_eth=str(model.coef_)

def ltc_slope():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from coin_data WHERE cname = 'BITMEX:LTCUSD'")
    myresult = mycursor.fetchall()
    pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])
    # line
    pd1['cdate'] = pd.to_datetime(pd1['cdate'])
    pd1['cdate'] = pd1['cdate'].apply(lambda x: x.toordinal())
    x = pd1['cdate'].to_numpy().reshape((-1, 1))
    y = pd1['price'].to_numpy()
    model = LinearRegression()
    model.fit(x, y)
    global slope_ltc
    slope_ltc=str(model.coef_)
# CALLING THE FUNCS I CREATED SO WE HAVE ACCESS TO TEH GLOBAL OUTPUTS
bltc_slope()
eth_slope()
ltc_slope()

dash.register_page(__name__,)
# def update_city_selected(input_value):
    # return f'You selected: {input_value}'

# HTML COMPONENTS AND DISPLAYING SLOPES FOR EACH COIN
layout = html.Div([
    html.H4('%%VERSUS'),
    dcc.Graph(id="graph5", figure={"layout": {"height": 300, "width": 700}, }),
    html.H4("LTC slope ="+slope_ltc),
    html.H4("BLTC slope =" + slope_bltc),
    html.H4("ETH slope =" + slope_eth),
    # SUBMIT BUTTON SEEMS TO BE REQUIRED BY DASH BY I HONESTLY DONT USE IT
    html.Div(
            # [dcc.Input(id='input-box4', type='text'),
             # dcc.Input(id='input-box5', type='text'),
             html.Button('Submit', id='button-example-5')
             # ]
),

    html.Div(id='output-container-button5',
             children='Enter a value and press submit'),
])
#REQUIRED DASH CALLBACK
@dash.callback(
    dash.dependencies.Output('graph5', 'figure'),
    [dash.dependencies.Input('button-example-5', 'n_clicks')],

)
#CHART FUNC
def update_output(n_clicks,):
    # print(" number of clicks", n_clicks)
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * from coin_data limit 1000")
    # CAN ADD OPTIONAL "LIMIT Z" COMMAND FOR A PRETTIER CHART OUTPUT
    myresult = mycursor.fetchall()

    pd1 = pd.DataFrame(myresult, columns=['id', 'cname', 'cdate', 'price', 'lows', 'highs'])
    # print(pd1)
    pd1['cdate'] = pd.to_datetime(pd1['cdate'])




    # GROUPING DATA BY COIN NAME
    groups = pd1.groupby(by='cname')
    # EMPTY ARRAY TO APPEND RESULTS TO
    data = []
    # COLORS FOR OUR LINES
    colors = ['red', 'blue', 'green']

    for group, dataframe in groups:



        # SORTING VALS BY DATE
        dataframe = dataframe.sort_values(by=['cdate'])
        # CREATING P_CHANGE COLLUMN,GROUPING BY CNAME AND APPLYING FUNC TO PRICE
        dataframe['p_change']=dataframe.groupby('cname')['price'].pct_change(-1)
        # print("pd1",pd1)
        # print("dataframe",dataframe)
        trace = go.Scatter(x=dataframe.cdate.tolist(),
                       y=dataframe.p_change.tolist(),
                       marker=dict(color=colors[len(data)]),
                       name=group)
        data.append(trace)
        # print(data)
    # CHART FEATURES
    layout = go.Layout(xaxis={'title': 'Time'},
                   yaxis={'title': 'Percent Change'},
                   margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                   hovermode='x')

    figure = go.Figure(data=data, layout=layout)
    # print('processing figure...')
    figure.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black'
    )
    return figure
# figure.show()
# ??figure displays but the next print statement never gets reached
#     print('after .show')
