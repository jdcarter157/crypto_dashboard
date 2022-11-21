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
def update_city_selected(input_value):
    return f'You selected: {input_value}'
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

# HTML COMPONENTS
layout = html.Div([
    html.H4(children='Simple Linear Regression',
            style={
                'textAlign':'center'
            }),
    dcc.Graph(id="graph3", figure={"layout": {"height": 300, "width": 700}, }),


    html.Button('Submit', id='button-example-3'),
    html.Div(id='output-container-button3',
             children='Enter a value and press submit'),
    dcc.Dropdown(
    options=options,
    id='lr-dropdown',
    value='bitmex_bltc',
    placeholder="bitmex_bltc"
),
])
# DASH CALLBACK
@dash.callback(
    dash.dependencies.Output('graph3', 'figure'),
    [dash.dependencies.Input('button-example-3', 'n_clicks')],
    [dash.dependencies.Input('lr-dropdown', 'value')]
)

def update_output(n_clicks, value):
    # print(" number of clicks", n_clicks)
    # print(" value-->", value)
    # VALUE IS FROM HTML FORM INPUT
    crypto_name = value
    mycursor = mydb.cursor()
    # QUERY DATA FROM DB
    mycursor.execute("SELECT * from " + crypto_name)
    myresult = mycursor.fetchall()
    # print(myresult)
    # SETTING COLLUMNS FOR DF
    pd1 = pd.DataFrame(myresult, columns=['id', 'cdate', 'price',])


    # line
    x=pd1['cdate']
    # print(x)
    # pd1['cdate'] = pd.to_datetime(pd1['cdate'])
    # print(pd1['cdate'])
    # CHANGING DATES FROM STRINGS TO ORDINAL INTS
    # pd1['cdate_ord'] = pd1['cdate'].apply(lambda x: x.toordinal())
    # RESHAPING FOR LINEAR REG
    x = pd1['cdate'].to_numpy().reshape((-1, 1))
    # print(x)
    price_data=[]

    for w in pd1.price:
        d = json.loads(w)
        price_data.append(d['low'])
    y = price_data
    # print("x",x)
    # print("y",y)
    # CHOOSING A MODEL TYPE
    model = LinearRegression()
    # FITTING THE MODEL

    # model.fit(x, y)
    # # 2 in one
    # # model = LinearRegression().fit(x, y)

    # r_sq = model.score(x, y)
    # print("r_sq",r_sq)
    # # PRINTING STATS
    # print(f"coefficient of determination: {r_sq}")
    # print(f"intercept: {model.intercept_}")
    # print(f"slope: {model.coef_}")
    # y_pred = model.predict(x)
    # print(f"predicted response:\n{y_pred}")
    # alternative syntax math
    # y_pred = model.intercept_ + model.coef_ * x

    pd.set_option('display.max_rows', None)

    # print(pd1)
    # CREATING FIGURE FOR WEB DISPLAY
    fig = px.scatter(pd1,
                  x='cdate', y=price_data , trendline='ols')

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='WHITE'
    )
    return fig
    # return p1
