from flask import Flask, jsonify, request, Response,send_file
from re_excel import *
from bson import json_util
from libs.database import conexion
from bson.objectid import ObjectId
import json

def listar_propietario():#P1
    propietarios = conexion('finca').find()
    response = json_util.dumps(propietarios)
    return response

def registrar_propietario():#P2
    try:
        _id = request.json["_id"]
        Finca = request.json["Finca"]
        Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
        Tipo_Documento = request.json["Tipo_Documento"]
        Nro_Documento = request.json["Nro_Documento"]
        Correo = request.json["Correo"]
        Telefono = request.json["Telefono"]
        array_departamentos = request.json["Departamentos"]
        Estacionamientos = request.json["Estacionamientos"]
        if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or array_departamentos or Estacionamientos :
            fecha=agregar_fecha()
            db = conexion('finca')
            id = db.insert_one(
                { "_id":_id,"Finca":Finca, "Nombres_y_Apellidos": Nombres_y_Apellidos, "Tipo_Documento": Tipo_Documento, "Nro_Documento": Nro_Documento, "Correo": Correo, "Telefono": Telefono, "Departamentos": array_departamentos, "Estacionamientos": Estacionamientos,"Fecha_creacion":fecha})
            
            response = {
                "status": 201,
                "mensaje":                  "SE REGISTRO SATISFACTORIAMENTE",
                #"_id": str(id),
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
            }
            return response
        else:
            print(Response.status_code)
            return response
    except Exception as e:
        print(e)
        response = {
                "status": 400,
                "code": e.code,
                "mensaje":"Hubo error al registrar"}
        return response

def eliminar_propietario():#P3
    conexion('finca').drop()
    response = jsonify({"status": 201,'message':' se elimino satisfactoriamente '})
    return response

def listar_propietario_ID(id):#P4
    propietario = conexion('finca').find_one({'_id': ObjectId(id), })
    response = json_util.dumps(propietario)
    return response

def eliminar_propietario_ID(id):#P5
    conexion('finca').delete_one({'_id': ObjectId(id)})
    response = jsonify({"status": 201,'message': 'El usuario ' + id + ' se elimino satisfactoriamente '})
    return response

def actualizar_propietario_ID(_id):#P6
    #_id = request.json["_id"]
    Finca = request.json["Finca"]
    Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
    Tipo_Documento = request.json["Tipo_Documento"]
    Nro_Documento = request.json["Nro_Documento"]
    Correo = request.json["Correo"]
    Telefono = request.json["Telefono"]
    Departamentos = request.json["Departamentos"]
    Estacionamientos = request.json["Estacionamientos"]
    if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or Departamentos or Estacionamientos:
        conexion('finca').update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {  "_id": _id,
                                                                                            "Finca": Finca,
                                                                                            "Nombres_y_Apellidos": Nombres_y_Apellidos,
                                                                                            "Tipo_Documento": Tipo_Documento,
                                                                                            "Nro_Documento": Nro_Documento,
                                                                                            "Correo": Correo,
                                                                                            "Telefono":Telefono,
                                                                                            "Departamentos":Departamentos,
                                                                                            "Estacionamientos":Estacionamientos}})
        response = jsonify({"status": 201,'message': 'El usuario ' + _id + ' ha sido actualizado satisfactoriamente'})
        return response