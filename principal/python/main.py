from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
#app.secret_key = 'myawesomesecretkey'
app.config['MONGO_URI'] = 'mongodb://localhost/videofincaDB'
mongo = PyMongo(app)

@app.route("/berrios", methods=["GET"])
def obtener_berrios():#aparece vacio []
    propiedades = json_util.dumps(mongo.db.propiedades.find())
    #print(json_util.dumps(propiedades)) #[]
    #print(type(json_util.dumps(propiedades))) #es string
    propiedades = list(propiedades)
    #print(propiedades)
    for propiedad in propiedades:
                plantilla2=[
                {
                "$match": {
                    "_id": f'{propiedad}'
                }
                },  
                {
                "$lookup": {
                    "from": 'plantilla',
                    "localField": '_id',
                    "foreignField": 'propiedad',
                    "as": 'Plantillas'
                }
                },  
                {
                "$lookup": {
                    "from": 'propietario',
                    "localField": '_id',
                    "foreignField": 'propiedad',
                    "as": 'Propietarios'
                }
                }
                ]
                resultados2 =mongo.db.berrios.aggregate(plantilla2)
    return resultados2

@app.route("/propiedades", methods=["GET"])
def obtener_propiedades():
    propiedades = mongo.db.propiedades.find()
    response = json_util.dumps(propiedades)
    return Response(response, mimetype="application/json")

@app.route("/propiedades", methods=["POST"])
def crear_propiedad():
    id_admin = request.json["id_admin"]
    direccion = request.json["direccion"]
    nombre = request.json["nombre"]
    if id_admin or direccion or nombre:
        id = mongo.db.propiedades.insert_one(
            { "id_admin":id_admin, "direccion":direccion, "nombre":nombre})
        response = {
            "_id":      str(id),
            "id_admin":id_admin,
            "direccion":direccion,
            "nombre":nombre
        }
        return response
    else:
        return not_found()
    
@app.route("/propiedades", methods=["POST"])
def crear_propiedades():
    id_propiedad = request.json["id_propiedad"]
    seccion = request.json["seccion"]
    if id_propiedad or seccion:
        id = mongo.db.propiedades.insert_one(
            { "id_propiedad":id_propiedad, "seccion":seccion})
        response = {
            "_id":      str(id),
            "seccion":  seccion
        }
        return response
    else:
        return not_found()

@app.route("/propiedades", methods=["DELETE"])
def elimiar_propiedad():
    mongo.db.propiedades.drop()
    response = jsonify({'message':' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route("/plantilla", methods=["DELETE"])
def elimiar_plantilla():
    mongo.db.plantilla.drop()
    response = jsonify({'message':' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route("/plantilla", methods=["GET"])
def obtener_plantilla():
    plantilla = mongo.db.plantilla.find()
    response = json_util.dumps(plantilla)
    return Response(response, mimetype="application/json")

@app.route("/propietarios", methods=["POST"])
def crear_porpietarios():
    id_propiedad = request.json["id_propiedad"]
    nombres_y_apellidos = request.json["nombres_y_apellidos"]
    tipo_documento = request.json["tipo_documento"]
    nro_documento = request.json["nro_documento"]
    correo_electronico = request.json["correo_electronico"]
    nro_celular = request.json["nro_celular"]
    departamento = request.json["departamento"]
    estacionamiento = request.json["estacionamiento"]
    if id_propiedad or nombres_y_apellidos or tipo_documento or nro_documento or correo_electronico or nro_celular or departamento or estacionamiento:
        id = mongo.db.propietarios.insert_one(
            { "id_propiedad":id_propiedad, "nombres_y_apellidos": nombres_y_apellidos, "tipo_documento": tipo_documento, "nro_documento": nro_documento, "correo_electronico": correo_electronico, "nro_celular": nro_celular, "departamento": departamento, "estacionamiento": estacionamiento})
        response = {
            "_id": str(id),
            "id_propiedad":             id_propiedad,
            "nombres_y_apellidos":  nombres_y_apellidos,
            "tipo_documento":       tipo_documento,
            "nro_documento":        nro_documento,
            "correo_electronico":   correo_electronico,
            "nro_celular":          nro_celular,
            "departamento":         departamento,
            "estacionamiento":      estacionamiento
        }
        return response
    else:
        return not_found()

@app.route('/propietarios', methods=['GET'])
def obtener_propietarios():
    propietarios = mongo.db.propietarios.find()
    response = json_util.dumps(propietarios)
    return Response(response, mimetype="application/json")

@app.route('/propietarios/<id>', methods=['GET'])
def obtener_propietario(id):
    propietario = mongo.db.propietarios.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(propietario)
    return Response(response, mimetype="application/json")

@app.route('/propietarios/<id>', methods=['DELETE'])
def eliminar_propietario(id):
    mongo.db.propietarios.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/propietarios/<_id>', methods=['PUT'])
def actualizar_porpietario(_id):
    nombres_y_apellidos = request.json["nombres_y_apellidos"]
    tipo_documento = request.json["tipo_documento"]
    nro_documento = request.json["nro_documento"]
    correo_electronico = request.json["correo_electronico"]
    nro_celular = request.json["nro_celular"]
    departamento = request.json["departamento"]
    estacionamiento = request.json["estacionamiento"]
    if nombres_y_apellidos or tipo_documento or nro_documento or correo_electronico or nro_celular or departamento or estacionamiento:
        mongo.db.propietarios.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {"nombres_y_apellidos": nombres_y_apellidos,
                                                                                            "tipo_documento": tipo_documento,
                                                                                            "nro_documento": nro_documento,
                                                                                            "correo_electronico": correo_electronico,
                                                                                            "nro_celular": nro_celular,
                                                                                            "departamento": departamento,
                                                                                            "estacionamiento":estacionamiento}})
        response = jsonify({'message': 'User' + _id + 'Updated Successfuly'})
        response.status_code = 200
        return response
    else:
      return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    #app.run(debug=True, port=4000, host="0.0.0.0")
    resultados = obtener_berrios()
    print(resultados)
