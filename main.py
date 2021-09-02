import pymysql

from flask import jsonify, flash, request
from app import app
from config import mysql

# GET - Read Data
@app.route("/api")
def get():
	try:
		sql_connect = mysql.connect()
		cursor = sql_connect.cursor(pymysql.cursors.DictCursor)

		cursor.execute("SELECT id,nama,email,umur,gaji FROM karyawan")

		api_result = cursor.fetchall()
		api_response = jsonify(api_result)
		api_response.status_code = 200
		return api_response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		sql_connect.close()

@app.route("/api/<int:id>")
def getid(id):
	try:
		sql_connect = mysql.connect()
		cursor = sql_connect.cursor(pymysql.cursors.DictCursor)

		cursor.execute("SELECT * FROM karyawan WHERE id =%s", id)
		
		api_result = cursor.fetchone()
		api_response = jsonify(api_result)
		api_response.status_code = 200
		return api_response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		sql_connect.close()

# POST - Create Data
@app.route("/create", methods=["POST"])
def create():
	try:
		request_json = request.json
		nama = request_json["nama"]
		email = request_json["email"]
		umur = request_json["umur"]
		gaji = request_json["gaji"]

		if request.method == "POST":
			SQLCommand = "INSERT INTO karyawan(nama, email, umur, gaji) VALUES( %s, %s, %s, %s)"
			Values = (nama, email, umur, gaji)

			sql_connect = mysql.connect()
			cursor = sql_connect.cursor()
			cursor.execute(SQLCommand, Values)
			sql_connect.commit()

			api_response = jsonify('Data telah ditambahkan!')
			api_response.status_code = 200
			return api_response
		else:
			return NotFound()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		sql_connect.close()

# PUT - Update Data
@app.route("/update", methods=["PUT"])
def update():
	try:
		request_json = request.json
		id = request_json["id"]
		nama = request_json["nama"]
		email = request_json["email"]
		umur = request_json["umur"]
		gaji = request_json["gaji"]

		if request.method == "PUT":
			SQLCommand = "UPDATE karyawan SET nama=%s, email=%s, umur=%s, gaji=%s WHERE id=%s"
			Values = (nama, email, umur, gaji, id)

			sql_connect = mysql.connect()
			cursor = sql_connect.cursor()
			cursor.execute(SQLCommand, Values)
			sql_connect.commit()

			api_response = jsonify("Data telah diperbarui!")
			api_response.status_code = 200
			return api_response
		else:
			return NotFound()
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		sql_connect.close()

# DELETE - Delete Data
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
	try:
		sql_connect = mysql.connect()
		cursor = sql_connect.cursor()
		cursor.execute("DELETE FROM karyawan WHERE id =%s", (id,))
		sql_connect.commit()

		message = {
			"status":"S",
			"message":"Your data has been updated."
		}

		api_response = jsonify(message)
		api_response.status_code = 200
		return api_response

	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		sql_connect.close()

# Error Handler
@app.errorhandler(404)
def NotFound(error=None):
    pesan = {
        "status": 404,
        "NotFound": "Tidak ditemukan : " + request.url,
    }
    api_response = jsonify(pesan)
    api_response.status_code = 404
    return api_response

app.debug = True

if __name__ == "__main__":
    app.run()
	