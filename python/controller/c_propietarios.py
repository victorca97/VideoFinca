from flask import Flask, jsonify, request, Response,send_file
from re_excel import *
from bson import json_util
from libs.database import conexion
from bson.objectid import ObjectId

"""def listar_propietario(P):#P1 idea de filtro 
    if P== 'T' :
        busqueda = ''
    else:
        busqueda = {"estado":P}

    propietarios = conexion('propietarios').find(busqueda)#{"estado":"A"}
    response = json_util.dumps(propietarios)
    return response"""
#LISTAR
def listar_propietario():
    propietarios = conexion('propietarios').find({"estado":"A"})#{"estado":"A"} → ACTIVOS , {"estado":"N"} → INACTIVOS 
    response = json_util.dumps(propietarios)
    return response

def listar_propietario_ID(id):#P4
    propietario = conexion('finca').find_one({'_id': ObjectId(id)})
    response = json_util.dumps(propietario)
    return response

#REGISTRAR
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
        ID_Departamentos = request.json["Departamentos"][0]['ID_Departamentos']
        Porcentaje_Participacion = request.json["Departamentos"][0]['Porcentaje_Participacion']
        Estacionamientos = request.json["Estacionamientos"]
        Numero_Estacionamiento = request.json["Estacionamientos"][0]['Numero_Estacionamiento']
        estado = 'A'#activo por defecto
        if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or array_departamentos or Estacionamientos :
            fecha=agregar_fecha()
            modificacion = ''
            db = conexion('propietarios')
            db.insert_one(
                { "_id":_id,"Finca":Finca, "Nombres_y_Apellidos": Nombres_y_Apellidos, "Tipo_Documento": Tipo_Documento,
                "Nro_Documento": Nro_Documento, "Correo": Correo, "Telefono": Telefono, "Departamentos": array_departamentos,
                "Estacionamientos": Estacionamientos,"Fecha_creacion":fecha,"Fecha_modificacion":modificacion,"estado":estado})
            response = {
                "status": 201,
                "mensaje": "El usuario "+ Nombres_y_Apellidos+ " se registro satisfactoriamente",
                "_id":                  _id,
                "Finca":                Finca,
                "Nombres_y_Apellidos":  Nombres_y_Apellidos,
                "Tipo_Documento":       Tipo_Documento,
                "Nro_Documento":        Nro_Documento,
                "Correo":               Correo,
                "Telefono":             Telefono,
                "Departamentos":         [{
                    'ID_Departamentos': ID_Departamentos, 'Porcentaje_Participacion': Porcentaje_Participacion}],
                "Estacionamientos":      [{
                    'Numero_Estacionamiento': Numero_Estacionamiento}],
                "Fecha_creacion":       fecha,
                "Fecha_modificacion": modificacion
            }
            return response
        else:
            print(Response.status_code)
            response ={
                "status": 400,
                "mensaje":"Uno o mas datos a registrar son incorrectos"}
            return json_util.dumps(response)
    except Exception as e:
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al registrar → "+str(e)}
        return json_util.dumps(response)

#ELIMINAR
def eliminar_propietario_ID():#P5
    try:
        _id = request.json["_id"]
        conexion('propietarios').update_one(
                {'_id': _id}, 
                {'$set': {"estado":'N'}})
        response = json_util.dumps({"status": 201,'message': 'El propietario ha sido eliminado satisfactoriamente'})
        return response
    except Exception as e:    
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar los datos → "+str(e)}
        return json_util.dumps(response)

#ACTUALIZAR
def actualizar_propietario_ID(_id):#P6
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
        if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or array_departamentos or Estacionamientos:
            #fehca mdoiifaa = agregar_fecha
            modificacion = agregar_fecha()
            conexion('propietarios').update_one(
                {'_id': _id}, {'$set': {
                                        "_id": _id,
                                        "Finca": Finca,
                                        "Nombres_y_Apellidos": Nombres_y_Apellidos,
                                        "Tipo_Documento": Tipo_Documento,
                                        "Nro_Documento": Nro_Documento,
                                        "Correo": Correo,
                                        "Telefono":Telefono,
                                        "Departamentos":array_departamentos,
                                        "Estacionamientos":Estacionamientos,
                                        "Fecha_modificacion": modificacion}})
            response = json_util.dumps({"status": 201,'message': 'El propietario ' + Nombres_y_Apellidos + ' ha sido actualizado satisfactoriamente'})
            return response
        else:
            print(Response.status_code)
            response ={
                "status": 400,
                "mensaje":"Uno o mas datos a actualizar son incorrectos"}
            return json_util.dumps(response)

    except Exception as e:
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar los datos → "+str(e)}
        return json_util.dumps(response)