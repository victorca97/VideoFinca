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
    duplicado_ID_Departamentos = ""
    duplicado_Numero_Estacionamiento = ""
    try:
        ID_Departamentos = request.json["Departamentos"][0]['ID_Departamentos']#validar que no se repita
        _id = request.json["_id"]
        Finca = request.json["Finca"]
        Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
        Tipo_Documento = request.json["Tipo_Documento"]
        Nro_Documento = request.json["Nro_Documento"]
        Correo = request.json["Correo"]
        Telefono = request.json["Telefono"]
        array_departamentos = request.json["Departamentos"]
        ID_Departamentos = request.json["Departamentos"][0]['ID_Departamentos']#validar que no se repita
        Porcentaje_Participacion = request.json["Departamentos"][0]['Porcentaje_Participacion']#habilitar cuando ponga ID_Departamentos
        Estacionamientos = request.json["Estacionamientos"]
        Numero_Estacionamiento = request.json["Estacionamientos"][0]['Numero_Estacionamiento']#validar que no se repita
        estado = 'A'#activo por defecto

        validacion_departamento = False
        validacion_estacionamiento = False
        
        if ID_Departamentos != "" and Numero_Estacionamiento!="":#puso tanto departamento como estacionamiento
            #con esta condicional ya se asegura que ninguno de esos campos estan vacios
            validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            validacion_general = True
            if validacion_departamento ==False or validacion_estacionamiento ==False:
                duplicado_ID_Departamentos = ID_Departamentos
                duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                validacion_general = False

        elif ID_Departamentos!="":#solo puso departamento
            validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
            if validacion_departamento ==False:
                duplicado_ID_Departamentos = ID_Departamentos
            validacion_general = validacion_departamento

        elif Numero_Estacionamiento!="":#solo puso estacionamiento
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            if validacion_estacionamiento ==False:
                duplicado_Numero_Estacionamiento = Numero_Estacionamiento
            validacion_general = validacion_estacionamiento
            validacion_departamento = True

        else:#mensaje en caso los campos Departamentos y Estacionamientos esten vacios
            validacion_general = False
            response = {"status": 400,'mensaje': 'Los campos de Departamento y Estacionamiento no pueden estar ambos vacios'}  
            return response

        if validacion_general:
            if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or array_departamentos or Estacionamientos :
                fecha=agregar_fecha()
                modificacion = ''
                #fecha2 = datetime.now()
                db = conexion('propietarios')
                db.insert_one(
                    { "_id":_id,"Finca":Finca, "Nombres_y_Apellidos": Nombres_y_Apellidos, "Tipo_Documento": Tipo_Documento,
                    "Nro_Documento": Nro_Documento, "Correo": Correo, "Telefono": Telefono, "Departamentos": array_departamentos,
                    "Estacionamientos": Estacionamientos,"Fecha_creacion":fecha,"Fecha_modificacion":modificacion,"estado":estado})
                response = {
                    "status": 201,
                    "mensaje": "El usuario "+ Nombres_y_Apellidos+ " se registro satisfactoriamente"
                }
                return response
            else:
                response = {"status": 400,'mensaje': 'Uno o mas datos a registrar son incorrectos'}  
                return response
        else:
            if  validacion_departamento!=True:
                response = {"status": 400,'mensaje': "El departamento "+duplicado_ID_Departamentos+" ya esta siendo usado"}            
                return response
            else:
                response = {"status": 400,'mensaje': "El estacionamiento "+duplicado_Numero_Estacionamiento+" ya esta siendo usado"}            
                return response

    except Exception as e:
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al registrar → "+str(e)}
        return response

#ACTUALIZAR
def actualizar_propietario_ID():#P6
    duplicado_ID_Departamentos = ""
    duplicado_Numero_Estacionamiento = ""
    _id = request.json["_id"]
    #validacion = False
    try:
        #_id = request.json["_id"]
        Finca = request.json["Finca"]
        Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
        Tipo_Documento = request.json["Tipo_Documento"]
        Nro_Documento = request.json["Nro_Documento"]
        Correo = request.json["Correo"]
        Telefono = request.json["Telefono"]
        array_departamentos = request.json["Departamentos"]
        Estacionamientos = request.json["Estacionamientos"]
        ID_Departamentos = request.json["Departamentos"][0]['ID_Departamentos']#validar que no se repita
        Numero_Estacionamiento = request.json["Estacionamientos"][0]['Numero_Estacionamiento']#validar que no se repita
        
        validacion_departamento = False
        validacion_estacionamiento = False
        
        if ID_Departamentos != "" or Numero_Estacionamiento!="":#puso tanto departamento como estacionamiento
            #con esta condicional ya se asegura que ninguno de esos campos estan vacios
            validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            validacion_general = True
            if validacion_departamento ==False and validacion_estacionamiento ==False:
                duplicado_ID_Departamentos = ID_Departamentos
                duplicado_Numero_Estacionamiento = Numero_Estacionamiento
                validacion_general = False

        elif ID_Departamentos!="":#solo puso departamento
            validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            if validacion_departamento ==False or validacion_estacionamiento ==False:
                duplicado_ID_Departamentos = ID_Departamentos
            validacion_general = validacion_departamento

        elif Numero_Estacionamiento!="":#solo puso estacionamiento
            validacion_departamento = validar_id_departamento(ID_Departamentos,Finca,"A")
            validacion_estacionamiento = validar_id_estacionamiento(Numero_Estacionamiento,Finca,"A")
            if validacion_estacionamiento ==False or validacion_departamento ==False:
                duplicado_Numero_Estacionamiento = Numero_Estacionamiento
            validacion_general = validacion_estacionamiento
            validacion_departamento = True

        else:#mensaje en caso los campos Departamentos y Estacionamientos esten vacios
            validacion_general = False
            response = {"status": 400,'mensaje': 'Los campos de Departamento y Estacionamiento no pueden estar ambos vacios'}  
            return json_util.dumps(response)

        if validacion_general:
            if _id or Finca or Nombres_y_Apellidos or Tipo_Documento or Nro_Documento or Correo or Telefono or array_departamentos or Estacionamientos:
                modificacion = datetime.now()
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
                response = {"status": 201,'mensaje': 'El propietario ' + Nombres_y_Apellidos + ' ha sido actualizado satisfactoriamente'}
                return json_util.dumps(response)
            else:
                response ={
                    "status": 400,
                    "mensaje":"Uno o mas datos a actualizar son incorrectos"}
                return json_util.dumps(response)
                 
        else:
            if  validacion_departamento!=True:
                response = {"status": 400,'mensaje': "El departamento "+duplicado_ID_Departamentos+" ya esta siendo usado"}            
                return json_util.dumps(response)
            else:
                response = {"status": 400,'mensaje': "El estacionamiento "+duplicado_Numero_Estacionamiento+" ya esta siendo usado"}            
                return json_util.dumps(response)

    except Exception as e:
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar los datos → "+str(e)}
        return json_util.dumps(response)

#ELIMINAR
def eliminar_propietario_ID():#P5
    try:
        _id = request.json["_id"]
        Nombres_y_Apellidos = request.json["Nombres_y_Apellidos"]
        conexion('propietarios').update_one(
                {'_id': _id}, 
                {'$set': {"estado":'N'}})
        response = {"status": 201,'mensaje': 'El propietario '+Nombres_y_Apellidos+' ha sido eliminado satisfactoriamente'}
        return json_util.dumps(response)
    except Exception as e:    
        print(e)
        response = {
                "status": 500,
                "mensaje":"Hubo error al eliminar al propietario "+Nombres_y_Apellidos+"  → "+str(e)}
        return json_util.dumps(response)