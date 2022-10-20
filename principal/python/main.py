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
def obtener_berrios():
    propiedades = json_util.loads(json_util.dumps(mongo.db.propiedades.find()))[0]
    for propiedad in propiedades:
            plantilla2=[
            { 
            "$match": {
                "_id": 'Finca0001' 
            }
            },  
            {
            "$lookup": {
                "from": 'plantilla',
                "localField": '_id',
                "foreignField": 'Finca',
                "as": 'Plantillas'
            }
            },  
            {
            "$lookup": {
                "from": 'propietarios',
                "localField": '_id',
                "foreignField": 'Finca',
                "as": 'Propietarios'
            }
            }
            ]
            resultados2 =mongo.db.propiedades.aggregate(plantilla2)
            response=json_util.dumps(resultados2)
    return Response(response,mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propiedades", methods=["GET"])
def obtener_propiedades():
    propiedades = mongo.db.propiedades.find()
    response = json_util.dumps(propiedades)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/propiedades", methods=["POST"])
def crear_propiedad():
    _id = request.json["_id"]
    Admin_Id = request.json["Admin_Id"]
    Direccion = request.json["Direccion"]
    Nombre = request.json["Nombre"]
    if Admin_Id or Direccion or Nombre:
        id = mongo.db.propiedades.insert_one(
            { "_id":_id,"Admin_Id":Admin_Id, "Direccion":Direccion, "Nombre":Nombre})
        response = {
            "_id":      str(id),
            "Admin_Id":Admin_Id,
            "Direccion":Direccion,
            "Nombre":Nombre
        }
        return response
    else:
        return not_found()

@app.route("/propiedades/<id>", methods=["DELETE"])
def elimiar_propiedad(id):
    mongo.db.propiedades.delete_one({'_id': id})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route("/propiedades", methods=["DELETE"])
def elimiar_propiedades():
    mongo.db.propiedades.drop()
    response = jsonify({'message':' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route("/plantilla", methods=["GET"])
def obtener_plantilla():
    plantilla = mongo.db.plantilla.find()
    response = json_util.dumps(plantilla)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/plantilla/<id>", methods=["GET"])
def obtener_plantilla_one(id):
    plantilla = mongo.db.plantilla.find({'Finca': id, })
    response = json_util.dumps(plantilla)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/plantilla", methods=["POST"])
def crear_plantilla():
    Finca = request.json["Finca"]
    Seccion = request.json["Seccion"]
    if Finca or Seccion:
        id = mongo.db.plantilla.insert_one(
            { "Finca":Finca, "Seccion":Seccion})
        response = {
            "_id":      str(id),
            "Finca":Finca,
            "Seccion":Seccion,
        }
        return response
    else:
        return not_found()

@app.route("/plantilla", methods=["DELETE"])
def elimiar_plantilla():
    mongo.db.plantilla.drop()
    response = jsonify({'message':' Deleted Successfully'})
    response.status_code = 200
    return response

@app.route('/propietarios', methods=['GET'])
def obtener_propietarios():
    propietarios = mongo.db.propietarios.find()
    response = json_util.dumps(propietarios)
    return Response(response, mimetype="application/json")

@app.route("/propietarios", methods=["POST"])
def crear_porpietarios():
    _id = request.json["_id"]
    Finca = request.json["Finca"]
    Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
    Tipo_Documento = request.json["Tipo_Documento"]
    Nro_Documento = request.json["Nro_Documento"]
    Correo = request.json["Correo"]
    Telefono = request.json["Telefono"]
    Departamentos = request.json["Departamentos"]
    Estacionamientos = request.json["Estacionamientos"]
    if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or Departamentos or Estacionamientos:
        id = mongo.db.propietarios.insert_one(
            { "_id":_id,"Finca":Finca, "Nombres_y_Apellidos": Nombres_y_Apellidos, "Tipo_Documento": Tipo_Documento, "Nro_Documento": Nro_Documento, "Correo": Correo, "Telefono": Telefono, "Departamentos": Departamentos, "Estacionamientos": Estacionamientos})
        response = {
            "_id": str(id),
            "_id":                  _id,
            "Finca":                Finca,
            "Nombres_y_Apellidos":  Nombres_y_Apellidos,
            "Tipo_Documento":       Tipo_Documento,
            "Nro_Documento":        Nro_Documento,
            "Correo":               Correo,
            "Telefono":             Telefono,
            "Departamentos":         Departamentos,
            "Estacionamientos":      Estacionamientos
        }
        return response
    else:
        return not_found()

@app.route("/propietarios", methods=["DELETE"])
def elimiar_propietarios():
    mongo.db.propietarios.drop()
    response = jsonify({'message':' Deleted Successfully'})
    response.status_code = 200
    return response

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
    _id = request.json["_id"]
    Finca = request.json["Finca"]
    Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
    Tipo_Documento = request.json["Tipo_Documento"]
    Nro_Documento = request.json["Nro_Documento"]
    Correo = request.json["Correo"]
    Telefono = request.json["Telefono"]
    Departamentos = request.json["Departamentos"]
    Estacionamientos = request.json["Estacionamientos"]
    if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or Departamentos or Estacionamientos:
        mongo.db.propietarios.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {  "_id": _id,
                                                                                            "Finca": Finca,
                                                                                            "Nombres_y_Apellidos": Nombres_y_Apellidos,
                                                                                            "Tipo_Documento": Tipo_Documento,
                                                                                            "Nro_Documento": Nro_Documento,
                                                                                            "Correo": Correo,
                                                                                            "Telefono":Telefono,
                                                                                            "Departamentos":Departamentos,
                                                                                            "Estacionamientos":Estacionamientos}})
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
    app.run(debug=True, port=4000, host="0.0.0.0")