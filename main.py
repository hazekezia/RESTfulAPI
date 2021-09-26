import pymysql

from flask import jsonify, request
from app import app
from config import mysql

sql_connect = mysql.connect()
cursor = sql_connect.cursor(pymysql.cursors.DictCursor)
cursor1 = sql_connect.cursor(pymysql.cursors.DictCursor)

# GET - Read Data
@app.route("/api")
def get():
	cursor.execute("SELECT * FROM api1")
	cursor1.execute("SELECT * FROM api2")
	
	api_result = cursor.fetchall()
	api_result1 = cursor1.fetchall()

	result = []

	for row in api_result:
		items = []
		for item in api_result1:
			if item["id_api1"] == row["id"]:
				items.append(item)
		result.append(
			{
				"id" : row["id"],
				"nama " : row["nama"],
				"umur" : row["umur"],
				"items" : items
			}
		)
				
	api_response = jsonify(result)
	api_response.status_code = 200
	return api_response

@app.route("/api/<int:id>")
def getid(id):
	cursor.execute("SELECT * FROM api1 WHERE id =%s", id)
	cursor1.execute("SELECT * FROM api2 WHERE id_api1 =%s", id)
	
	api_result = cursor.fetchall()
	api_result1 = cursor1.fetchall()

	result = {}
	items = {}

	for item in api_result1:
		items["id_api1"] = item["id_api1"]
		items["deskripsi"] = item["deskripsi"]

	for row in api_result:
		result["id"] = row["id"]
		result["nama"] = row["nama"]
		result["umur"] = row["umur"]
		result["items"] = items

	api_response = jsonify(result)
	api_response.status_code = 200
	return api_response

# POST - Create Data
@app.route("/api/create_object", methods=["POST"])
def create_object():
	request_json = request.json

	if request.method == "POST":
		name = request_json["nama"]
		umur = request_json["umur"]

		SQLCommand = "INSERT INTO api1(nama, umur) VALUES(%s, %s)"
		Values = (name, umur)

		cursor.execute(SQLCommand, Values)
		sql_connect.commit()

		id_api1 = cursor.lastrowid

		for item in request_json["items"]:
			desc = item["deskripsi"]
			SQLCommand = "INSERT INTO api2(id_api1, deskripsi) VALUES(%s, %s)"
			Values = (id_api1, desc)

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

#TESTINGTESTING
@app.route("/api/create_array", methods=["POST"])
def create_array():
	request_json = request.json
	counter = len(request.json)

	if request.method == "POST":
		for i in range(counter):
			name = request_json[i]["nama"]
			umur = request_json[i]["umur"]

			cursor.execute("SELECT id FROM api1 where nama=%s", (name))
			data = cursor.fetchone()
			print(data)

			if (cursor.rowcount >= 1):
				id_fetch = data["id"]
				SQLCommand = "UPDATE api1 SET nama=%s, umur=%s WHERE id=%s"
				Values = (name, umur, id_fetch)

				cursor.execute(SQLCommand, Values)
				sql_connect.commit()
				id_api1 = id_fetch
				print(id_fetch)	

			elif (cursor.rowcount == 0):
				SQLCommand = "INSERT INTO api1(nama, umur) VALUES(%s, %s)"
				Values = (name, umur)

				cursor.execute(SQLCommand, Values)
				sql_connect.commit()
				id_api1 = cursor.lastrowid

			cursor.execute("DELETE FROM api2 WHERE id_api1 =%s", (id_api1,))

			for item in request_json[i]["items"]:
				desc = item["deskripsi"]
				SQLCommand = "INSERT INTO api2(id_api1, deskripsi) VALUES(%s, %s)"
				Values = (id_api1, desc)

				cursor.execute(SQLCommand, Values)
				sql_connect.commit()
		
		message = 	{
						"status":"S",
						"message":"Your data has been updated."
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

		cursor.execute("DELETE FROM api2 WHERE id_api1 =%s", (id,))

		for item in request_json["items"]:
			desc = item["deskripsi"]
			SQLCommand = "INSERT INTO api2(id_api1, deskripsi) VALUES(%s, %s)"
			Values = (id, desc)

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
	cursor.execute("DELETE FROM api2 WHERE id_api1 =%s", (id,))
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