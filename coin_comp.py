

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

#
mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="ecoins"
)
#
dash.register_page(__name__,)
# def update_city_selected(input_value):
    # return f'You selected: {input_value}'

layout = html.Div([
    html.H4('VERSUS'),
    dcc.Graph(id="graph4", figure={"layout": {"height": 300, "width": 700}, }),


    html.Div(
            # [dcc.Input(id='input-box4', type='text'),
             # dcc.Input(id='input-box5', type='text'),
             html.Button('Submit', id='button-example-4')
             # ]
),

    html.Div(id='output-container-button4',
             children='Enter a value and press submit'),
])
#
@dash.callback(
    dash.dependencies.Output('graph4', 'figure'),
    [dash.dependencies.Input('button-example-4', 'n_clicks')],
    # [dash.dependencies.Input('input-box5', 'value')],
    # [dash.dependencies.State('input-box4', 'value')],
    # [dash.dependencies.State('input-box5', 'value')]
# ]
)
#
def update_output(n_clicks,):
    print(" number of clicks", n_clicks)


#
#
#     fig = px.scatter(pd1,
#                   x='cdate', y='price' , trendline='ols')
#     px.add_scatter(x=pd2['cdate'], y=pd2['price'], trendline='ols',color_discrete_sequence=['red'] )
    # return fig

#
# mydb = mysql.connector.connect(
#    host="localhost",
#    user="root",
#    password="",
#    database="ecoins"
# )


# crypto_name ='BITMEX:LTCUSD'
    mycursor = mydb.cursor(buffered=True)

    mycursor.execute("SELECT * from coin_data limit 10")

    myresult = mycursor.fetchall()

    pd1 = pd.DataFrame(myresult, columns=['id', 'cname', 'cdate', 'price', 'lows', 'highs'])
    print(pd1)
    pd1['cdate'] = pd.to_datetime(pd1['cdate'])
    pd1['cdate'] = pd1['cdate'].apply(lambda x: x.toordinal())


# df = pd.DataFrame({'Machine': ['K2K01', 'K2K01', 'K2K01', 'K2K02', 'K2K02', 'K2K02', 'K2K03', 'K2K03', 'K2K03'],
#                   'Units': [100, 200, 400, 400, 300, 100, 500, 700, 500],
#                   'Time': [11, 12, 13, 11, 12, 13, 11, 12, 13]})

    groups = pd1.groupby(by='cname')
    data = []
    colors = ['red', 'blue', 'green']

    for group, dataframe in groups:
        dataframe = dataframe.sort_values(by=['cdate'])
        print(dataframe)
        trace = go.Scatter(x=dataframe.cdate.tolist(),
                       y=dataframe.price.tolist(),
                       marker=dict(color=colors[len(data)]),
                       name=group)
        data.append(trace)
        print(data)

    layout = go.Layout(xaxis={'title': 'Time'},
                   yaxis={'title': 'Price'},
                   margin={'l': 40, 'b': 40, 't': 50, 'r': 50},
                   hovermode='closest')

    figure = go.Figure(data=data, layout=layout)
    print('processing figure...')
    return figure
# figure.show()
    print('after .show')