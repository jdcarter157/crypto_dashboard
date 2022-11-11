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
# import dash_daq as daq
import scipy.stats as stats
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_daq as daq

import random

# connect to db
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",

   database="ecoins"
)

dash.register_page(__name__)


# df = pd.DataFrame({
#     "x": [1,2,3,4],
#     "y": [1,2,3,4],
#     "customdata": [1,2,3,4],
# })
#
# fig = px.line(df, x="x", y="y",  custom_data=["customdata"])
# fig.update_layout(clickmode='event+select')
# fig.update_traces(marker_size=20)

layout = html.Div([

    html.Div(id='coinsearch',
             children=''),


    dcc.Input(id='input-coin-state', type='text', value=''),
    html.Button(id='coin-button-state', n_clicks=0, children='Search Coins'),
    html.Div(id='coin-output-state'),

    dcc.Graph(id="graph_ch", figure={"layout": {"height": 300, "width": 700}, })

])

@dash.callback(
    # dash.dependencies.Output('my-gauge-1', 'value'),
               dash.dependencies.Output('graph_ch', 'figure'),

               dash.dependencies.Input('input-coin-state', 'value'),
              dash.dependencies.State('coin-button-state', 'value'),
               )
# def update_output(lk, n_clicks):
#     lookupname = lk
#     mycursor = mydb.cursor()
#     mycursor.execute("SELECT popularity from coin_popularity WHERE coin_name = %s",
#                      (lookupname,))
#     myresult = mycursor.fetchall()
#     return_gauge = 0
#     for row in myresult:
#         return_gauge = row[0]
#     return_gauge *= 10
#     return return_gauge



def update_fig(df,fig):

    mycursor = mydb.cursor()
    # QUERY DATA FROM DB


    mycursor.execute("SELECT date,COUNT(content) AS num_tweets from tweets GROUP BY DATE(date)",())
    myresult = mycursor.fetchall()

    # print(myresult)
    # SETTING COLLUMNS FOR DF


    chat = pd.DataFrame(myresult, columns=['date','num_tweets'])
    print("chat",chat)
    mycursor2 = mydb.cursor()
    # QUERY DATA FROM DB
    mycursor2.execute("SELECT price,cdate from coin_data where cname='BITMEX:LTCUSD'GROUP BY DATE(cdate)", )
    myresult2 = mycursor.fetchall()
    price=pd.DataFrame(myresult2, columns=['price','date'])
    # print(myresult2)
    print("price",price)
    # SETTING COLLUMNS FOR DF
    # df=pd.read_csv('scantest.csv')
    # price_std=df['litecoin_value'].std()
    price_std=price.price.std()

    # chatter_std=df['chatter'].std()
    chatter_std=chat.num_tweets.std()
    # price_mean=df['litecoin_value'].mean()
    price_mean=price.price.mean()
    print("price mean",price_mean)

    print(type(price))
    # df['price'][i]-mean
    zscores = stats.zscore(price.price)
    print("zscore",zscores)
    zscores_ch = stats.zscore(chat.num_tweets)
    print("!!!!zscores_ch",zscores_ch)

    print("price std",price_std)
    # chatter_mean=df['chatter'].mean()
    chatter_mean=chat.num_tweets.mean()
    # creating the collumn to see wich elements are 3 sd's away from mean or not
    # df['outliers']=(df['litecoin_value'] >= price_std*3) | (df['litecoin_value']<=price_std*-3)
    # df['outliners']=np.array([])
    # global outliers
    print("begin")
    outliers = []
    outliers_ch=[]
    # print("outs",df['outliers'])

    # for i in range(len(df['litecoin_value'])):
    #     if df['litecoin_value'][i] >= price_std*3 or df['litecoin_value'][i] <= price_std*-3:
    #         outliers.append(df['litecoin_value'][i])
    print("begin")
    # print("222222",type(zscores))
    for i in range(len(zscores)):
        # print(len(zscores))
        # print(zscores)
        # print(i)
        # print(zscores.price[i])
        if zscores[i] >= 2.0 or zscores[i] <= -2.0:
            # print("mid")
            outliers.append(price.price[i])
            # print("!!",outliers[i])
        else:
            # print("else")
            outliers.append(0)
            # print("!!",outliers[i])

    print(zscores_ch)
    print(chat)
    for i in range(len(chat)):
        if zscores_ch[i] >= 2 or zscores_ch[i] <= -2:
            outliers_ch.append(chat.num_tweets[i])
            print("++",outliers_ch)
        else:
            outliers_ch.append(0)
            # print("++",outliers_ch)
    print("appends.")
    print(outliers_ch)
    fig1=px.line(x=price.date,y=price.price,)
    fig2=px.scatter(x=price['date'],y=outliers)
    fig4=px.scatter(x=chat['date'],y=outliers_ch)
    fig5=px.bar(x=chat['date'],y=chat.num_tweets,)
    fig3=go.Figure(data=fig1.data+fig2.data+fig4.data+fig5.data)

    # fig.add_scatter(x=df['time'],y=outliers,)
    # fig1.add_trace(go.Scatter(y=[outliers], mode="markers",color='red'),)
    print("end.")
    return fig3
    # fig.add_trace()

