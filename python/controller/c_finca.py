from flask import jsonify, request
from re_excel import *
from bson import json_util
from bson.objectid import ObjectId
from libs.database import conexion

#LISTAR
def listar_finca():#F1
    try:
        finca = conexion('finca').find()
        response = json_util.dumps(finca)
        return response
    except Exception as e:
        print(e)
        response =  json_util.dumps({"status":500, 'message':'Sucedio un error al conseguir datos de la finca → '+e})
        return response

#ELIMINAR
def eliminar_finca_ID():#F3 
    try:
        id = request.json["_id"]
        Nombre = request.json["Nombre"]
        conexion('finca').delete_one({'_id': id})
        response = json_util.dumps({"status": 201,'message': 'La finca ' + Nombre + ' se elimino satisfactoriamente'})
        return response
    except Exception as e:
        print(e)
        response =  json_util.dumps({"status":500, 'message':'Sucedio un error al tratar de eliminar la finca → '+str(e)})
        return response


def listar_finca_ID(id):#F4
    plantilla = conexion('finca').find({'Finca': id, })
    response = json_util.dumps(plantilla)
    return response

def crear_finca():
    try:
        Admin_Id = request.json["Admin_Id"]
        Direccion = request.json["Direccion"]
        Nombre = request.json["Nombre"]
        if Admin_Id or Direccion or Nombre:
            modificacion = ''
            _id = generar_id()
            now = agregar_fecha()
            db = conexion('finca')
            db.insert_one({ "_id":_id,"Admin_Id":Admin_Id,"Direccion":Direccion, "Nombre":Nombre, "Fecha_creacion":now,"Fecha_modificacion":modificacion})
            #print('RESPUESTA',respuesta)
            response = {
                "status": 201,
                "_id":     _id,
                "Admin_Id":Admin_Id,
                "Direccion":Direccion,
                "Nombre":Nombre,
                "Fecha_creacion": now,
                "Mensaje" : 'Se registro satisfactoriamente la finca '+Nombre
            }
            return response
        else:
            return not_found('No se registro')
    except Exception as e:
        response = {
                "status": 500,
                "mensaje":"Hubo error al registrar → "+str(e)}
        return  json_util.dumps(response)

def actualizar_finca_ID():
    try:
        id = request.json["_id"]
        Admin_Id = request.json["Admin_Id"]
        Direccion = request.json["Direccion"]
        Nombre = request.json["Nombre"]
        if Admin_Id or Direccion or Nombre:
            fecha_modificacion = agregar_fecha()
            conexion('finca').update_one(
                #{'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {  
                {'_id': id}, {'$set': {  
                    #"_id": id,
                    "Admin_Id":Admin_Id,
                    "Direccion":Direccion,
                    "Nombre":Nombre,
                    "Fecha_modificacion": fecha_modificacion}}
            )
        response = json_util.dumps({"status": 201,'message': 'La Finca ' + Nombre + ' ha sido actualizado satisfactoriamente'})
        return response
    except Exception as e:
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar → " + str(e)}
        return json_util.dumps(response)

def not_found(mensaje):
    message = {
        'mensaje': mensaje,
        'status': 404
    }
    response = jsonify(message)
    
    return response