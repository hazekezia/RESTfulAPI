import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request

# GET		
@app.route('/api')
def api():
	try:
		sql_connect = mysql.connect()
		cursor = sql_connect.cursor(pymysql.cursors.DictCursor)

		cursor.execute("SELECT id,name,harga FROM api_test")

		api_result = cursor.fetchall()
		api_response = jsonify(api_result)
		api_response.status_code = 200
		return api_response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		sql_connect.close()

@app.errorhandler(404)
def NotFound(error=None):
    pesan = {
        "status": 404,
        "NotFound": "Tidak ditemukan : " + request.url,
    }
    api_response = jsonify(pesan)
    api_response.status_code = 404
    return api_response

if __name__ == "__main__":
    app.run()