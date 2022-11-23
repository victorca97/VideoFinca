from flask import jsonify, request, Response
from re_excel import *
from bson import json_util
from libs.database import conexion
from consolidado import generar_doc_finca
import json

def generar_recibos():#R1
    try:
        finca= request.json["_id"]
        borrar_temporal()
        query_finca=[{ "$match": {"_id": f'{finca}' }}, 
        {"$lookup": {"from": 'plantilla',"localField": '_id',"foreignField": 'Finca',"as": 'Plantillas'}},  
        {"$lookup": {"from": 'propietarios',"localField": '_id',"foreignField": 'Finca',"as": 'Propietarios'}}]
        resultados =conexion('finca').aggregate(query_finca)
        response=json_util.dumps(resultados)
        tipo = 'pdf' #xlsx o pdf
        datos = json.loads(response)
        lista = datos[0]['Propietarios']
        cantidad_propietarios = len(lista)
        if cantidad_propietarios>0:
            lista_recibos,url = generar_doc_finca(tipo,datos,finca)
            return Response(json_util.dumps(lista_recibos),mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
        else:
            response = {"status": 400,"mensaje":"No hay propietarios en la finca "+finca}
        return response
    except Exception as e:
        response = {"status": 500,"mensaje":"Hubo error al registrar → "+str(e)}
        return response

def listar_recibos():#RNUEVO1
    plantilla = conexion('finca').find()
    response = json_util.dumps(plantilla)

    #response = jsonify({'message':' se elimino satisfactoriamente'}) tiene que devovler un mensaje
    return response

def listar_recibos_ID(id):#RNUEVO2
    plantilla = conexion('finca').find({'finca': id, })
    response = json_util.dumps(plantilla)
    return response

def actualizar_recibos(id):#R2
    try:
        #id= request.json["_id"]
        Finca = request.json["Finca"]
        Seccion = request.json["Seccion"]
        if Finca or Seccion:
            response = {"$set":{"_id": id,"Finca":Finca,"Seccion":Seccion,}
            }
            filter={
                "_id": id, 
            }
            id = conexion('recibos').update_one(filter, response)
            return response
            #return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
        else:
            return not_found()
    except Exception as e:
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar → "+str(e)}
        return response

def eliminar_recibos():#R3
    conexion('recibos').drop()
    response = jsonify({'message':' se elimino satisfactoriamente'})
    return response

def eliminar_recibos_ID(id):#RNUEVO3
    conexion('finca').delete_one({'_id': id})
    response = jsonify({'message': 'El usuario' + id + ' se elimino satisfactoriamente'})
    return json_util.dumps(response)

def listar_secciones():
    plantilla = conexion('plantilla').find()
    response = json_util.dumps(plantilla)
    print(response)
    return response

def not_found(mensaje):
    message = {
        'mensaje': mensaje,
        'status': 404
    }
    response = jsonify(message)
    
    return response
