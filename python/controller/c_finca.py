from flask import jsonify, request
from re_excel import *
from bson import json_util
from bson.objectid import ObjectId
from libs.database import conexion
#FALTA ACTUALIZAR FINCA
def listar_finca():#F1
    finca = conexion('finca').find()
    response = json_util.dumps(finca)
    return response

def eliminar_finca():#F2
    conexion('finca').drop()
    response = jsonify({"status": 201,'message':' se elimino satisfactoriamente'})
    return response

def eliminar_finca_ID(id):#F3
    conexion('finca').delete_one({'_id': id})
    response = jsonify({"status": 201,'message': 'El usuario ' + id + ' se elimino satisfactoriamente'})
    return response

def listar_finca_ID(id):#F4
    plantilla = conexion('finca').find({'Finca': id, })
    response = json_util.dumps(plantilla)
    return response

def crear_finca():
    try:
        Admin_Id = request.json["Admin_Id"]
        Direccion = request.json["direccion"]
        Nombre = request.json["Nombre"]
        if Admin_Id or Direccion or Nombre:
            _id = generar_id()
            now = agregar_fecha()
            db = conexion('finca')
            respuesta = db.insert_one({ "_id":_id,"Admin_Id":Admin_Id, 
            "Direccion":Direccion, "Nombre":Nombre, "Fecha_creacion":now})
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
                "code": e.code,
                "mensaje":"Hubo error al registrar"}
        return response

def actualizar_finca_ID(id):
    Admin_Id = request.json["Admin_Id"]
    Direccion = request.json["direccion"]
    Nombre = request.json["Nombre"]
    if Admin_Id or Direccion or Nombre:
        conexion('finca').update_one(
            {'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {  
                "_id": id,
                "Admin_Id":Admin_Id,
                "Direccion":Direccion,
                "Nombre":Nombre}}
        )
    response = jsonify({"status": 201,'message': 'El usuario ' + id + ' ha sido actualizado satisfactoriamente'})
    return response

def not_found(mensaje):
    message = {
        'mensaje': mensaje,
        'status': 404
    }
    response = jsonify(message)
    
    return response