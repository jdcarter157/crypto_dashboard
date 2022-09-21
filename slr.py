import numpy as np
from sklearn.linear_model import LinearRegression

import pandas as pd
import numpy as np
import mysql.connector

mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   password="",
   database="ecoins"
)
# pick a coin
crypto_name = "BITMEX:BLTC"
mycursor = mydb.cursor()
mycursor.execute("SELECT * from coin_data WHERE cname = %s", (crypto_name,))
myresult = mycursor.fetchall()

pd1 = pd.DataFrame(myresult, columns=['crid', 'cname', 'cdate', 'price', 'lows', 'highs'])

# pd1['cdate'] = pd1['cdate'].map(pd1.cdate.toordinal)
pd1['cdate']= pd.to_datetime(pd1['cdate'])
pd1['cdate'] = pd1['cdate'].apply(lambda x: x.toordinal())


x=pd1['cdate'].to_numpy().reshape((-1, 1))
y=pd1['price'].to_numpy()

print(x)
print(y)
# x=np.array([myresult])

# x = np.array([5, 15, 25, 35, 45, 55]).reshape((-1, 1))
# y = np.array([5, 20, 14, 32, 22, 38])
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