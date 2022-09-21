
from sklearn.linear_model import LinearRegression


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





mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="ecoins"
)
dash.register_page(__name__,)
def update_city_selected(input_value):
    return f'You selected: {input_value}'

layout = html.Div([
    html.H4('continents!!!!!!!!'),
    dcc.Graph(id="graph3", figure={"layout": {"height": 300, "width": 700}, }),


    html.Div(dcc.Input(id='input-box3', type='text')),
    html.Button('Submit', id='button-example-3'),
    html.Div(id='output-container-button3',
             children='Enter a value and press submit'),
])
@dash.callback(
    dash.dependencies.Output('graph3', 'figure'),
    [dash.dependencies.Input('button-example-3', 'n_clicks')],
    [dash.dependencies.State('input-box3', 'value')])
def update_output(n_clicks, value):
    # print(" number of clicks", n_clicks)
    # print(" value-->", value)

    crypto_name = value
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * from coin_data WHERE cname = %s", (crypto_name,))
    myresult = mycursor.fetchall()
    # print(myresult)

    pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])


    # line
    pd1['cdate'] = pd.to_datetime(pd1['cdate'])
    pd1['cdate'] = pd1['cdate'].apply(lambda x: x.toordinal())

    x = pd1['cdate'].to_numpy().reshape((-1, 1))
    y = pd1['price'].to_numpy()
    #
    # print(x)
    # print(y)
    model = LinearRegression()
    model.fit(x, y)
    # # 2 in one
    # # model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    print(f"coefficient of determination: {r_sq}")
    print(f"intercept: {model.intercept_}")
    print(f"slope: {model.coef_}")
    y_pred = model.predict(x)
    print(f"predicted response:\n{y_pred}")
    # # alternative syntax math
    # # y_pred = model.intercept_ + model.coef_ * x

    pd.set_option('display.max_rows', None)

    # print(pd1)


    fig = px.scatter(pd1,
                  x='cdate', y='price' , trendline='ols')
    return fig
    # return p1
