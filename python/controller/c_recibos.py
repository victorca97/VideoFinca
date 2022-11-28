from flask import jsonify, request, Response
from re_excel import *
from bson import json_util
from libs.database import conexion
from consolidado import generar_doc_finca
import json

#plantilla es recibos

def generar_recibos():#R1
    #nombre de la finca, direccion, 
    try:
        finca= request.json["_id"]
        mes = request.json["Mes"]#esto sera un numero
        year = request.json["Year"]
        borrar_temporal()
        query_finca=[{ "$match": {"_id": f'{finca}' }}, 
        {"$lookup": {"from": 'recibos',"localField": '_id',"foreignField": 'Finca',"as": 'recibos'}},  
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
    return response

def listar_recibos_ID():#RNUEVO2
    finca = request.json["_id"]
    mes = request.json["mes"]#esto sera un numero
    anno = request.json["anno"]
    try:
        plantilla = conexion('recibos').find({'Finca': finca,'Mes':mes,'Year': anno })
        response = json_util.dumps(plantilla)
        return response
    except Exception as e:
        response = {"status": 500,"mensaje":"Hubo error al registrar → "+str(e)}
        return response
    
def actualizar_recibos():#R2
    try:
        finca= request.json["Finca"]
        mes = request.json["Mes"]#esto sera un numero
        year = request.json["Year"]
        seccion = request.json["Seccion"]
        print('FINCA >>> ',finca)
        print('MES >>> ',mes)
        print('YEAR >>> ',year)
        print('SECCION >>> ',seccion)
        print(type(seccion))
        #print(lon)

        modificacion = agregar_fecha()
        conexion('propietarios').update_one(
            {'_id': id}, {'$set': {"_id": id,
                            "Finca":finca,
                            "Seccion":seccion,
                            "Seccion.ID_Departamentos":seccion,
                            "Fecha_modificacion":modificacion}
                            })
        response = {"status": 201,'mensaje': 'El propietario ' + Nombres_y_Apellidos + ' ha sido actualizado satisfactoriamente'}
        return json_util.dumps(response)

        """for i in range(lon): 
            if Finca or Seccion:
                response = {"$set":{"_id": id,"Finca":Finca,"Seccion":Seccion,"Seccion.ID_Departamentos":seccion}}
                filter={
                    "_id": id, 
                }
                id = conexion('plantilla').update_one(filter, response)
                print('RESPONSE >>>>> ',response)
                return response
        else:
            return not_found()"""
    except Exception as e:
        print('ERROR → ',e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar → "+str(e)}
        return response

def eliminar_recibos():#R3
    conexion('recibos').drop()
    response = jsonify({'mensaje':' se elimino satisfactoriamente'})
    return response

def eliminar_recibos_ID(id):#RNUEVO3
    conexion('finca').delete_one({'_id': id})
    response = jsonify({'mensaje': 'El usuario' + id + ' se elimino satisfactoriamente'})
    return json_util.dumps(response)

def listar_secciones():
    plantilla = conexion('plantilla').find()
    response = json_util.dumps(plantilla)
    print(response)
    return response

#FUNCIONES AUXILIARES
def modificar_subsecciones(id_subseccion,nombre,monto,descripcion):
    resultado = {   
                    "ID_Subseccion": "{}".format(id_subseccion),
                    "nombre": "{}".format(nombre),
                    "monto": "{}".format(monto),
                    "descripcion": "{}".format(descripcion)
                }
    return resultado


def not_found(mensaje):
    mensaje = {
        'mensaje': mensaje,
        'status': 404
    }
    response = jsonify(mensaje)
    
    return response
