from sklearn.linear_model import LinearRegression


import dash


import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
import pandas as pd
import numpy as np
import math
import time
from datetime import datetime
import mysql
import mysql.connector



from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import random

# now = datetime.now()

 # DB CONN
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#
#     database="ecoins"
# )
mydb = mysql.connector.connect(
    host="192.168.0.122",
    user="crypto",
    password="crypto",
    auth_plugin="mysql_native_password",
    database="coindata"
)
# ADDING TO PAGES FOR FLASK

dash.register_page(__name__,)
mycursor = mydb.cursor()
mycursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES LIMIT 10 ")
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

years=['2022','2021','2020','2019','2018','2017','2016','2015','2014','2013']
months=['01','02','03','04','05','06','07','08','09','10','11','12']
days=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
# HTML COMPONENTS
layout = html.Div([
    html.H4(children='Simple Linear Regression',
            style={
                'textAlign':'center'
            }),
    dcc.Graph(id="graph_4", figure={"layout": {"height": 300, "width": 700}, }),

    html.Div(id='output-container-button',
             children=''),
    html.Div(id='output-container-button5',
             children='Enter a value and press submit'),

    dcc.Checklist(
        id="checklist",
        options=[
            {'label': 'ETH', 'value': 'line1'},
            {'label': 'BLTC', 'value': 'line2'},
            {'label': 'LTC', 'value': 'line3'},
            {'label': 'line4', 'value': 'line4'},
            {'label': 'line5', 'value': 'line5'},
            {'label': 'line6', 'value': 'line6'}

        ],
        labelStyle={'display': 'block'},
        value=[]
    ),
    dcc.Dropdown(id="year_drop",multi=False,value='2022',options=years),
    dcc.Dropdown(id="month_drop", multi=False, value='06', options=months),
    dcc.Dropdown(id="day_drop", multi=False, value='21', options=days),
    dcc.Dropdown(
    options=options,
    id='slr-dropdown',
    value='bitmex_ethusd_eth',
    placeholder="bitmex_ethusd_eth"
),
    dcc.Dropdown(
    options=options,
    id='slr-dropdown2',
    value='bitmex_bltc',
    placeholder="bitmex_bltc"
),
    dcc.Dropdown(
    options=options,
    id='slr-dropdown3',
    value='bitmex_ltcusd',
    placeholder="bitmex_ltcusd"
),



])
# DASH CALLBACK
@dash.callback(
    dash.dependencies.Output('graph_4', 'figure'),
    dash.dependencies.Input('year_drop','value'),
    dash.dependencies.Input('month_drop', 'value'),
    dash.dependencies.Input('day_drop', 'value'),
    [dash.dependencies.Input('checklist','value'),
     [dash.dependencies.Input('slr-dropdown', 'value')],
     [dash.dependencies.Input('slr-dropdown2', 'value')],
     [dash.dependencies.Input('slr-dropdown3', 'value')],

     ]
)

def update_output(year_drop,month_drop,day_drop,checklist,val,val2,val3):
    # print ("----")
    # print ( in1 )
    # print ( date5 + "" + date6)
    #
    # print ("----")

    # print(" number of clicks", n_clicks)
    # print(" value-->", value)
    # VALUE IS FROM HTML FORM INPUT
#    crypto_name = value
    crypto_name = val[0]
    print(crypto_name)
    # print ("in1:", in1)
    # if ( crypto_name == "" ):
    #     crytoname = "BITMEX:ETHUSD_ETH"

    mycursor = mydb.cursor()
    # QUERY DATA FROM DB
    mycursor.execute("SELECT * from "+ crypto_name,)
    myresult = mycursor.fetchall()
    # print(myresult)
    # SETTING COLLUMNS FOR DF
    pd1 = pd.DataFrame(myresult, columns=['crid', 'cdate', 'price',])
    price_data=[]
    for f in pd1.price:
        d=json.loads(f)
        price_data.append(d['low'])
    # line


    pd.set_option('display.max_rows', None)

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=pd1.cdate, y=pd1.lows))

    ## add second line ##########################################

    # print("in2:", in2)
    # if (crypto_name == "None"):
    #     crytoname = "BITMEX:ETHUSD_ETH"

    crypto_name2 = val2[0]
    print("yuur",crypto_name2)
    # print ("in1:", in1)
    # if ( crypto_name == "" ):
    #     crytoname = "BITMEX:ETHUSD_ETH"

    mycursor2 = mydb.cursor()
    # QUERY DATA FROM DB
    mycursor2.execute("SELECT * from "+ crypto_name2,)
    myresult2 = mycursor2.fetchall()
    # print(myresult)
    # SETTING COLLUMNS FOR DF
    pd2 = pd.DataFrame(myresult2, columns=['crid', 'cdate', 'price',])
    price_data2=[]
    for w in pd2.price:
        d=json.loads(w)
        price_data2.append(d['low'])

    # print ( pd2.price)

    ## add second line ##########################################
    crypto_name3 = val3[0]
    print("y",crypto_name3)

    # print ("in1:", in1)
    # if ( crypto_name == "" ):
    #     crytoname = "BITMEX:ETHUSD_ETH"

    mycursor3 = mydb.cursor()
    # QUERY DATA FROM DB
    mycursor3.execute("SELECT * from "+ crypto_name3,)
    myresult3 = mycursor3.fetchall()
    # print(myresult)
    # SETTING COLLUMNS FOR DF
    pd3 = pd.DataFrame(myresult3, columns=['crid', 'cdate', 'price',])
    price_data3=[]
    for z in pd3.price:
        d=json.loads(z)
        price_data3.append(d['low'])


    # print(pd3.cdate)
    # print(price_data)
    # data=[[price_data],[price_data2],[price_data3]]
    print(len(pd1),len(pd2),len(pd3))
    data={
        crypto_name:price_data,
        crypto_name2:price_data2,
        crypto_name3:price_data3
    }
    # labs=[crypto_name,crypto_name2,crypto_name3]
    pd4=pd.DataFrame(data=data,)
    # print(pd4)
    # pd4= pd.concat([pd1.cdate,price_data,price_data2,price_data3],axis=1)
    p_change=pd4[crypto_name].pct_change()
    # print(p_change)
    p_change2=pd4[crypto_name2].pct_change()
    p_change3=pd4[crypto_name3].pct_change()

    # print(pd4)
    # print(pd2.price)
    # print("!!!",price_data,)
    # print("@@@",price_data2,)
    # print("###",price_data3,)

    # print(p_change3)
    fig=px.scatter(x=pd1['cdate'], y=[p_change,p_change2,p_change3], trendline='ols')
    # fig.update_layout(
    #     plot_bgcolor='rgba(0,0,0,0)',
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     font_color='WHITE'
    # )

    # update figure on checkbox toggle
    # fig.update_traces(marker_color="RoyalBlue",
    #                   selector=dict(marker_color="MediumPurple"))

    print(checklist)
    # allowing users to hide and unhide traces for better view using checklist
    if checklist == ['line1']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'ETH'}))
    elif checklist==['line2']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'BLTC'}))
    elif checklist==['line3']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'p_change3'}))
    elif checklist==['line1','line2']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'ETH'}))
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'BLTC'}))
    elif checklist==['line2','line1']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'ETH'}))
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'BLTC'}))
    elif checklist==['line1','line3']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'ETH'}))
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'BLTC'}))
    elif checklist==['line3','line1']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'ETH'}))
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'LTC'}))
    elif checklist==['line2','line3']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'LTC'}))
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'BLTC'}))
    elif checklist==['line3','line2']:
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'LTC'}))
        fig.update_traces(overwrite=True, marker={"opacity": 0},selector=({'name':'BLTC'}))

    return fig
    # return p1
