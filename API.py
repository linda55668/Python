import flask
from flask import jsonify, request
import sqlite3
from datetime import timedelta


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["JSON_AS_ASCII"] = False

@app.route('/', methods=['GET'])
def home():
    return '請輸入參數UsageAccountId'

#Get lineItem/UnblendedCost grouping by product/productname
@app.route('/1/<string:id>', methods=['GET'])
def select_data(id):
    con = sqlite3.connect('python.db')
    SQLcmd = ("select ProductName,sum(unblendedcost) from BILLSTMASTR where UsageAccountId='"+id+"' group by productname")
    cursor=con.execute(SQLcmd) 
    data = cursor.fetchall()
    con.commit()
    con.close()
    return jsonify(data)

#not finished yet 
#Get daily lineItem/UsageAmount grouping by product/productname
@app.route('/2/<string:id>', methods=['GET'])
def select_data2(id):
    con = sqlite3.connect('python.db')
    # SQLcmd = ("select ProductName,UsageStartDate,UsageEndDate,usageaccountid,sum(UsageAmount) from BILLSTMASTR where UsageAccountId='"+id+"' group by productname,UsageStartDate")
    SQLcmd = ("select DISTINCT ProductName ,(select Min(b3.UsageStartDate) from BILLSTMASTR b3 join BILLSTMASTR b4 on b3.ProductName=b4.ProductName where b.ProductName=b3.ProductName) as STRDate,")
    SQLcmd += (" (select MAX(b3.UsageEndDate) from BILLSTMASTR b3 join BILLSTMASTR b4 on b3.ProductName=b4.ProductName where b.ProductName=b3.ProductName) as ENDate")
    SQLcmd += (" from BILLSTMASTR as b where UsageAccountId='"+id+"'")	
    cursor=con.execute(SQLcmd) 
    Namedata = cursor.fetchall()
    # detail = []
    for row in Namedata:
        BEGDate = Namedata[0][1]
        ENDDate= Namedata[0][2]
        while BEGDate<=ENDDate :
            SQLcmd2 = ("select sum(UsageAmount) from BILLSTMASTR ")
            SQLcmd2 += ("where UsageAccountId='"+id+"' and substr(UsageStartDate,1,10)='"+Namedata[0][1][:10] +"'and ProductName='"+Namedata[0][0]+"'")
            SQLcmd2 += ("group by ProductName")
            cursor2=con.execute(SQLcmd)
            Datedata2 = cursor2.fetchall()
    


    con.commit()
    con.close()
        
    return jsonify(Datedata2)

app.run()