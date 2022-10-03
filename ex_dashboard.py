
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
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="ecoins"
)
# ADDING TO PAGES FOR FLASK

dash.register_page(__name__,)
def update_city_selected(input_value):
    return f'You selected: {input_value}'

# HTML COMPONENTS
layout = html.Div([
    html.H4('continents!!!!!!!!'),
    dcc.Graph(id="graph3", figure={"layout": {"height": 300, "width": 700}, }),


    html.Div(dcc.Input(id='input-box3', type='text')),
    html.Button('Submit', id='button-example-3'),
    html.Div(id='output-container-button3',
             children='Enter a value and press submit'),
])
# DASH CALLBACK
@dash.callback(
    dash.dependencies.Output('graph3', 'figure'),
    [dash.dependencies.Input('button-example-3', 'n_clicks')],
    [dash.dependencies.State('input-box3', 'value')])

def update_output(n_clicks, value):
    # print(" number of clicks", n_clicks)
    # print(" value-->", value)
    # VALUE IS FROM HTML FORM INPUT
    crypto_name = value
    mycursor = mydb.cursor()
    # QUERY DATA FROM DB
    mycursor.execute("SELECT * from coin_data WHERE cname = %s", (crypto_name,))
    myresult = mycursor.fetchall()
    # print(myresult)
    # SETTING COLLUMNS FOR DF
    pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])


    # line
    pd1['cdate'] = pd.to_datetime(pd1['cdate'])
    # print(pd1['cdate'])
    # CHANGING DATES FROM STRINGS TO ORDINAL INTS
    pd1['cdate_ord'] = pd1['cdate'].apply(lambda x: x.toordinal())
    # RESHAPING FOR LINEAR REG
    x = pd1['cdate_ord'].to_numpy().reshape((-1, 1))
    y = pd1['price'].to_numpy()
    #
    print("x",x)
    print("y",y)
    # CHOOSING A MODEL TYPE
    model = LinearRegression()
    # FITTING THE MODEL

    model.fit(x, y)
    # # 2 in one
    # # model = LinearRegression().fit(x, y)

    r_sq = model.score(x, y)
    print("r_sq",r_sq)
    # PRINTING STATS
    print(f"coefficient of determination: {r_sq}")
    print(f"intercept: {model.intercept_}")
    print(f"slope: {model.coef_}")
    y_pred = model.predict(x)
    print(f"predicted response:\n{y_pred}")
    # # alternative syntax math
    # # y_pred = model.intercept_ + model.coef_ * x

    pd.set_option('display.max_rows', None)

    # print(pd1)
    # CREATING FIGURE FOR WEB DISPLAY
    fig = px.scatter(pd1,
                  x='cdate', y='price' , trendline='ols')
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_color='black'
    )
    return fig
    # return p1
