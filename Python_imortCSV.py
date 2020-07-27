#引用CSV套件
import csv
#引用SQLITE 資料庫套件
import sqlite3

from flask import Flask

# #引用API
# import flask

#連結資料庫、若沒有存在會自行建立新的資料庫
conn=sqlite3.connect('python.db')
sql=conn.cursor()
#執行SQL語法建立Table，先檢查是否已存在
sql.execute('''Create Table if not exists BILLSTMASTR (PayerAccountId  NUMERIC ,UnblendedCost  FLOAT ,UnblendedRate  REAL ,UsageAccountId  NUMERIC ,UsageAmount  REAL ,UsageStartDate  Text ,UsageEndDate  Text ,ProductName  nvarchar PRIMARY KEY)''')

sql.execute('''CREATE INDEX if not exists index_name on BILLSTMASTR (PayerAccountId, UsageAccountId)''')

#所需要之欄位名稱

cols = ["bill/PayerAccountId", "lineItem/UnblendedCost", "lineItem/UnblendedCost", "lineItem/UsageAccountId","lineItem/UsageAmount","lineItem/UsageStartDate","lineItem/UsageEndDate","product/ProductName"]
    #開啟指定路徑CSV檔
    #讀取CSV檔案
with open('C:\\Users\\user\\Desktop\\Python\\output2_N.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sql.execute("INSERT INTO BILLSTMASTR VALUES("+row[cols[0]]+", "+row[cols[1]]+", "+row[cols[2]]+", "+row[cols[3]]+", "+row[cols[4]]+", '"+row[cols[5]]+"', '"+row[cols[6]]+"','"+row[cols[7]]+"')")
    

conn.commit()
conn.close()
