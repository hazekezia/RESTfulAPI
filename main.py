import pymysql

from flask import jsonify, request
from app import app
from config import mysql

sql_connect = mysql.connect()
cursor = sql_connect.cursor(pymysql.cursors.DictCursor)

# GET - Read Data
@app.route("/api")
def get():
	cursor.execute("SELECT * FROM api1")

	api_result = cursor.fetchall()
	api_response = jsonify(api_result)
	api_response.status_code = 200
	return api_response

@app.route("/api/<int:id>")
def getid(id):
	cursor.execute("SELECT * FROM api1 WHERE id =%s", id)
	
	api_result = cursor.fetchone()
	api_response = jsonify(api_result)
	api_response.status_code = 200
	return api_response

@app.route("/api2")
def getapi2():
	cursor.execute("SELECT * FROM api2")

	api_result = cursor.fetchall()
	api_response = jsonify(api_result)
	api_response.status_code = 200
	return api_response

# POST - Create Data
@app.route("/api/create", methods=["POST"])
def create():
	request_json = request.json

	if request.method == "POST":
		name = request_json["nama"]
		umur = request_json["umur"]

		for item in request_json["items"]:
			id_api1 = item["id_api1"]
			desc = item["deskripsi"]
			SQLCommand = "INSERT INTO api2(id_api1, deskripsi) VALUES(%s, %s)"
			Values = (id_api1, desc)

			cursor.execute(SQLCommand, Values)
			sql_connect.commit()

		SQLCommand = "INSERT INTO api1(nama, umur) VALUES(%s, %s)"
		Values = (name, umur)

		cursor.execute(SQLCommand, Values)
		sql_connect.commit()

		message = 	{
					"status":"S",
					"message":"Your data has been added."
					}	

		api_response = jsonify(message)
		api_response.status_code = 200
		return api_response
	else:
		return NotFound()

# PUT - Update Data
@app.route("/api/update", methods=["PUT"])
def update():
	request_json = request.json
	id = request_json["id"]
	nama = request_json["nama"]
	umur = request_json["umur"]

	if request.method == "PUT":
		SQLCommand = "UPDATE api1 SET nama=%s, umur=%s WHERE id=%s"
		Values = (nama, umur, id)

		cursor.execute(SQLCommand, Values)
		sql_connect.commit()

		message = {
			"status":"S",
			"message":"Your data has been updated."
		}

		api_response = jsonify(message)
		api_response.status_code = 200
		return api_response
	else:
		return NotFound()

# DELETE - Delete Data
@app.route("/api/delete/<int:id>", methods=["DELETE"])
def delete(id):
	cursor.execute("DELETE FROM api1 WHERE id =%s", (id,))
	sql_connect.commit()

	message = {
		"status":"S",
		"message":"Your data has been deleted."
	}

	api_response = jsonify(message)
	api_response.status_code = 200
	return api_response

# Error Handler
@app.errorhandler(404)
def NotFound(error=None):
    message = {
        "status": 404,
        "NotFound": "Tidak ditemukan : " + request.url,
    }
    api_response = jsonify(message)
    api_response.status_code = 404
    return api_response

app.debug = True

if __name__ == "__main__":
    app.run(threaded=True)