from flask import Flask, jsonify, request, Response,send_file
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from flask_cors import CORS
from consolidado import generar_doc_finca
from re_excel import *
import json
app = Flask(__name__)
#app.secret_key = 'myawesomesecretkey'
app.config['MONGO_URI'] = 'mongodb+srv://Paino:sistemasMONGO@cluster0.awnp8gy.mongodb.net/videosession?retryWrites=true&w=majority'
mongo = PyMongo(app)
CORS(app)
cors=CORS(app,resource={
    r"/*":{
        "origins":"*"
    }
})

#FILE_CONTAINER = 'C:/Users/DELL/Desktop/flask_videofinca/excels/pruebas/'
FILE_CONTAINER = '../excels/Finca0001/Edu_Be/2022/'

import rutas.finca
import rutas.propietarios
import rutas.recibos

#ORIGINAL
@app.route("/recibosOriginal", methods=["GET"])###NO VA
def recibos_generarOriginal():
    #propiedades = json_util.loads(json_util.dumps(mongo.db.propiedades.find()))[0]
    fincas = json_util.loads(json_util.dumps(mongo.db.finca.find({},{"_id"}))) #es una lista
    print('FINCAS>>>>',fincas)
    len_finca= len(fincas)
    lista_finca=[]
    lista_datos_leidos=[]
    for i in range(len_finca):
        print(fincas[i]["_id"])
        lista_finca.append(fincas[i]["_id"])
    borrar_temporal()

    condicion = 0

    while condicion == 0:

        for finca in lista_finca:
            plantilla2=[
            { 
            "$match": {
                "_id": f'{finca}' 
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
            resultados2 =mongo.db.finca.aggregate(plantilla2)
            # print("RESULTADOS ", resultados2)
            response=json_util.dumps(resultados2)
            # print("RESPONSE ", response)
            tipo = 'pdf' #xlsx o pdf
            datos = json.loads(response)
            print('Leyendo la '+finca)
            #print('COMO SE LEE EL JSON >>>>>>>>>>>',leerlo)
            buffer,url = generar_doc_finca(tipo,datos)
            print(buffer)
            lista_datos_leidos.append(buffer)

        condicion = 1 #para q finalize
    print(lista_datos_leidos) 
    print('URL → ',url)   
    datos_mostrar=[lista_datos_leidos,url]
    #return Response(json_util.dumps(buffer),mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
    return Response(json_util.dumps(datos_mostrar),mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
#response = requests.request("POST", url, headers=headers, data=user)

#VERSION POST (ACTUAL EN USO)
#para enviar parametros a un get, ponerlo en el link
#YA ESTA 
@app.route("/recibos", methods=["POST"])#R1
def recibos_generar():
    try:
        finca= request.json["_id"]
        borrar_temporal()
        query_finca=[
        { 
        "$match": {
            "_id": f'{finca}' 
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
        resultados =mongo.db.finca.aggregate(query_finca)
        
        #print("RESULTADOS ", resultados)
        response=json_util.dumps(resultados)
        #print('RESPONSE >>>>>>',response)
        # print("RESPONSE ", response)
        tipo = 'pdf' #xlsx o pdf
        datos = json.loads(response)
        lista = datos[0]['Propietarios']
        cantidad_propietarios = len(lista)
        print(cantidad_propietarios)
        if cantidad_propietarios>0:
            print('Leyendo la '+finca)
            #print('COMO SE LEE EL JSON >>>>>>>>>>>',leerlo)
            lista_recibos,url = generar_doc_finca(tipo,datos,finca)
            #return Response(json_util.dumps(lista),mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
            return Response(json_util.dumps(lista_recibos),mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
        else:
            response = {
                "status": 400,
                "mensaje":"No hay propietarios en la finca"}
        return response

    except Exception as e:
        response = {
                "status": 500,
                "code": e.code,
                "mensaje":"Hubo error al registrar"}
        return response
#response = requests.request("POST", url, headers=headers, data=user)

#YA NO VA
@app.route('/recibos/<filename>')#para poder descargar los archivos poniendo /{nombre_archivo}.{extension}
def return_files_tut(filename):
    file_path = FILE_CONTAINER + filename
    return send_file(file_path, as_attachment=True)
    #return send_file(file_path, as_attachment=True, attachment_filename='')
    
#YA ESTA
@app.route("/finca/<id>", methods=["DELETE"])#F3
def eliminar_finca_id(id):
    mongo.db.finca.delete_one({'_id': id})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response
#YA ESTA
@app.route("/finca", methods=["DELETE"])#F2
def eliminar_finca():
    mongo.db.finca.drop()
    response = jsonify({'message':' Deleted Successfully'})
    response.status_code = 200
    return response
#YA ESTA
@app.route("/plantilla", methods=["GET"])#F1
def obtener_plantilla():
    plantilla = mongo.db.plantilla.find()
    response = json_util.dumps(plantilla)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
#YA ESTA
@app.route("/plantilla/<id>", methods=["GET"])#F4
def obtener_plantilla_one(id):
    plantilla = mongo.db.plantilla.find({'Finca': id, })
    response = json_util.dumps(plantilla)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

#ESTE NO APARECE EN OTRO LADO. A OBSERVAR SI SE BORRA O SE DEJA NOMAS, JEAN Q HACE ESTO?
@app.route("/plantilla", methods=["POST"])
def crear_plantilla():
    try:
        Finca = request.json["Finca"]
        Seccion = request.json["Seccion"]
        if Finca or Seccion:
            #id=generar_id()
            id = mongo.db.plantilla.insert_one(
                { "_id":Finca, "Finca":Finca, "Seccion":Seccion})
            response = {
                "_id": Finca,
                "Finca":Finca,
                "Seccion":Seccion,
            }
            return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
        else:
            return not_found()
    except Exception as e:
        print('ENTRO A AEXCEPCION')
        print(e)
        response = {
                "status": 400,
                "code": e.code,
                "mensaje":"Hubo error al registrar"}
        #setear el estado de respuesta
        return response


#YA ESTA
@app.route('/propietarios', methods=['GET'])#P1
def obtener_propietarios():
    propietarios = mongo.db.propietarios.find()
    response = json_util.dumps(propietarios)
    return Response(response, mimetype="application/json")
#YA ESTA
@app.route("/propietarios", methods=["POST"])#P2
def crear_porpietarios():
    try:
        print('ENTRO AL TRY')
        print('REQUEST',request.json)
        _id = request.json["_id"]
        
        Finca = request.json["Finca"]
        Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
        Tipo_Documento = request.json["Tipo_Documento"]
        Nro_Documento = request.json["Nro_Documento"]
        Correo = request.json["Correo"]
        Telefono = request.json["Telefono"]
        array_departamentos = request.json["Departamentos"]
        
        """array_departamentos = [
            {
                "ID_Departamentos": 703,
                "Porcentaje_Participacion": 2.4
            }
        ]"""
    
        Estacionamientos = request.json["Estacionamientos"]
        #Participacion = request.json["Participacion"]
        if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or array_departamentos or Estacionamientos :
            fecha=agregar_fecha()
            id = mongo.db.propietarios.insert_one(
                { "_id":_id,"Finca":Finca, "Nombres_y_Apellidos": Nombres_y_Apellidos, "Tipo_Documento": Tipo_Documento, "Nro_Documento": Nro_Documento, "Correo": Correo, "Telefono": Telefono, "Departamentos": array_departamentos, "Estacionamientos": Estacionamientos,"Fecha_creacion":fecha})
            
            response = {
                "status": 201,
                "mensaje":                  "SE REGISTRO SATISFACTORIAMENTE",
                "_id": str(id),
                "_id":                  _id,
                "Finca":                Finca,
                "Nombres_y_Apellidos":  Nombres_y_Apellidos,
                "Tipo_Documento":       Tipo_Documento,
                "Nro_Documento":        Nro_Documento,
                "Correo":               Correo,
                "Telefono":             Telefono,
                "Departamentos":         array_departamentos,
                "Estacionamientos":      Estacionamientos,
                "Fecha_creacion":       fecha
                #"Participacion":         Participacion
            }
            #Response.status('201')
            print('SATISDACTORIO')
            print('id>>>>>>',id)
            #response.status_code = 201
            return response
        else:
            print('ENTRO AL ELSE')
            #return not_found()
            print(Response.status_code)
            return response
    except Exception as e:
        print('ENTRO A AEXCEPCION')
        print(e)
        response = {
                "status": 400,
                "code": e.code,
                "mensaje":"Hubo error al registrar"}
        return response
#YA ESTA
@app.route("/propietarios", methods=["DELETE"])#P3
def elimiar_propietarios():
    mongo.db.propietarios.drop()
    response = jsonify({'message':' Deleted Successfully'})
    #response.status_code = 200
    return response
#YA ESTA
@app.route('/propietarios/<id>', methods=['GET'])#P4
def obtener_propietario(id):
    propietario = mongo.db.propietarios.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(propietario)
    return Response(response, mimetype="application/json")
#YA ESTA
@app.route('/propietarios/<id>', methods=['DELETE'])#P5
def eliminar_propietario(id):
    mongo.db.propietarios.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + ' Deleted Successfully'})
    #response.status_code = 200
    return response
#YA ESTA
@app.route('/propietarios/<_id>', methods=['PUT'])#P6
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

@app.route("/codificado/<id>", methods=["GET"])#el id sera la finca
def obtener_codificado(id):
    plantilla = mongo.db.plantilla.find({'Finca': id, })
    response = json_util.dumps(plantilla)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

#YA ESTA
@app.route("/plantilla", methods=["PUT"])#R2
def actualizar_plantilla():
    print(request.json)
    id= request.json["_id"]
    Finca = request.json["Finca"]
    Seccion = request.json["Seccion"]
    if Finca or Seccion:
        response = {"$set":{
            "_id": str(id),
            "Finca":Finca,
            "Seccion":Seccion,
            }
        }
        filter={
            "_id": str(id), 
        }
        id = mongo.db.plantilla.update_one(filter, response)
        return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
    else:
        return not_found()

#YA ESTA
@app.route("/plantilla", methods=["DELETE"])#R3
def elimiar_plantilla():
    mongo.db.plantilla.drop()
    response = jsonify({'message':' Deleted Successfully'})
    response.status_code = 200
    return response

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 200
    
    return response

if __name__ == "__main__":
    app.run(debug=True, port=4000, host="0.0.0.0")