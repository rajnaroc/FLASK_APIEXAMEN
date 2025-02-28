from email import message
from flask import Flask,jsonify, request
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL

app = Flask(__name__)

# cuando lo hago en .env me da problemas Render por eso lo hago de esta forma y Docker

app.config["MYSQL_URI"] = "mongodb+srv://rajnaroc:12345@cluster0.r5gm8.mongodb.net"

app.config["MYSQL_HOST"] = "bpg29qpszsnrjasj7qkn-mysql.services.clever-cloud.com"
app.config["MYSQL_USER"] = "unwsd1t63zdgzubu"
app.config["MYSQL_PASSWORD"] = "2mse9FtX9bOu82e9hWiC"
app.config["MYSQL_DB"] = "bpg29qpszsnrjasj7qkn"


mongo = PyMongo()

mysql = MySQL(app)


# mostrar todos los usuarios de mi api mysql
@app.route('/get_mysqlusers', methods=["GET"])
def getmysqlusers():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users")
    datos = cursor.fetchall()

    if datos:

        return jsonify(datos)
    else:
        return jsonify({"message":"error al encontrar usuarios"})


# Buscar usuario por id en la base de datos
@app.route('/get_mysqluser/<id>', methods=["GET"])
def getmysqluser(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s ",(id,))
    datos = cursor.fetchall()

    if datos:

        return jsonify(datos)
    else:
        return jsonify({"message":"error al encontrar usuarios"})


# Insertart usuarios en mi api de mysql todos
@app.route('/add_mysqlusers',methods=["POST"])
def addmysqlusers():
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    numero = request.json["numero"]
    genero = request.json["genero"]

    if nombre and edad and numero and genero:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users VALUES (NULL,%s,%s,%s,%s)",(nombre,edad,numero,genero))
        mysql.connection.commit()

        return jsonify({"messgae": "insertado correctamente el" + nombre})
    else:
        return jsonify({"message": "faltan datos"})

# con esto modificas los datos del usuario en la base de datos
@app.route('/updatemysqluser/<id>', methods=["PUT"])
def updatemysqluser(id):
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    numero = request.json["numero"]
    genero = request.json["genero"]
    
    print(nombre,edad,numero,genero)

    if nombre and edad and numero and genero:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET nombre = %s, edad = %s, numero = %s, genero = %s WHERE id = %s",(nombre,edad,numero,genero,id))
        mysql.connection.commit()

        return jsonify({"message": "actulizado los datos"})
    else:
        return jsonify({message: "faltan datos"})
    
@app.route('/deletemysql/<id>')
def deletemysqluser(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE users WHERE id = %s",(id))
        mysql.connection.commit()

        return jsonify({"message":" elimando el" + id})

########################################################################
# Empieza la api de mongo

@app.route('/get_mongousers', methods=["GET"])
def getusersmongo():
    user = mongo.db.user.find()
    return jsonify(user)


@app.route('/add_mongousers', methods=["POST"])
def method_name():
    nombre = request.json["nombre"]
    edad = request.json["edad"]
    numero = request.json["numero"]
    genero = request.json["genero"]

    if nombre and genero and numero and edad:
        id = mongo.db.user.insert_one({
            "nombre": nombre,
            "edad": edad,
            "numero" : numero,
            "genero" : genero
            })
        valor = {
            "id": str(id),
            "nombre": nombre,
            "edad": edad,
            "numero": numero,
            "genero" : genero
        }
        return jsonify(valor)
    else:
        return jsonify({ "message": "falta un campo"})


def error_404(error):
    return jsonify({"message": "Pagina no encontrada"})

if __name__ == "__main__":
    app.run()