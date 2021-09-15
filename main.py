import pymysql

from flask import jsonify, flash, request
from app import app
from config import mysql

sql_connect = mysql.connect()
cursor = sql_connect.cursor(pymysql.cursors.DictCursor)

# GET - Read Data
@app.route("/api")
def get():
	cursor.execute("SELECT * FROM one")

	api_result = cursor.fetchall()
	api_response = jsonify(api_result)
	api_response.status_code = 200
	return api_response

@app.route("/api/<int:id>")
def getid(id):
	cursor.execute("SELECT * FROM one WHERE id =%s", id)
	
	api_result = cursor.fetchone()
	api_response = jsonify(api_result)
	api_response.status_code = 200
	return api_response

# POST - Create Data
@app.route("/create", methods=["POST"])
def create():
	request_json = request.json
	name = request_json["nama"]
	nomor = request_json["nomor"]

	if request.method == "POST":
		SQLCommand = "INSERT INTO one(nama, nomor) VALUES(%s, %s)"
		Values = (name, nomor)

		cursor.execute(SQLCommand, Values)
		sql_connect.commit()

		message = {
			"status":"S",
			"message":"Your data has been added."
		}

		api_response = jsonify(message)
		api_response.status_code = 200
		return api_response
	else:
		return NotFound()

# PUT - Update Data
@app.route("/update", methods=["PUT"])
def update():
	request_json = request.json
	id = request_json["id"]
	nama = request_json["nama"]
	nomor = request_json["nomor"]

	if request.method == "PUT":
		SQLCommand = "UPDATE one SET nama=%s, nomor=%s WHERE id=%s"
		Values = (nama, nomor, id)

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
@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
	cursor.execute("DELETE FROM one WHERE id =%s", (id,))
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
	