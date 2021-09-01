import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

# GET		
@app.route('/api')
def api():
	try:
		connect = mysql.connect()
		cursor = connect.cursor(pymysql.cursors.DictCursor)

		cursor.execute("SELECT id,name,harga FROM api_test")

		api_result = cursor.fetchall()
		respone = jsonify(api_result)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		connect.close()

if __name__ == "__main__":
    app.run()