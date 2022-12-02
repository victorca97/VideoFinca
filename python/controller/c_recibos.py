from flask import jsonify, request, Response
from re_excel import *
from bson import json_util
from libs.database import conexion
from consolidado import generar_doc_finca
import json

#plantilla es recibos

def generar_recibos():#R1 CREA LOS DOCUMENTOS
    #nombre de la finca, direccion, 
    try:
        id = request.json["_id"]#ide del recibo
        finca= request.json["Finca"]
        #mes = request.json["Mes"]#esto sera un numero
        #year = request.json["Year"]
        tipo = request.json["tipo"]
        fecha_emision = request.json["fecha_emision"]
        #print(fecha_emision)
        fecha_vencimiento = request.json["fecha_vencimiento"]
        tipo_propietario = tipo
        print('TIPO PROPIETARIO >>> ',tipo_propietario)
        #print(fecha_vencimiento)
        borrar_temporal()
        #print('ID >>>',id)
        #print('FINCA >>>',finca)
        #print('Tipo >>>',tipo)
        propietarios = conexion('propietarios').find({'Finca': finca,"estado": "A","tipo_propietario":tipo_propietario})
        #Obtengo el id departamento, estacionamiento, prc participacion,nombre del propeitario
        datos_dpto_estacionamiento = json_util.dumps(propietarios) #STRING
        datos_dpto_estacionamiento = json.loads(datos_dpto_estacionamiento)#LISTA
        #-Direccion,nombre de la finca
        """query_finca=[{ "$match": {"_id": finca }}, 
        {"$lookup": {"from": 'recibos',"localField": '_id',"foreignField": 'Finca',"as": 'recibos'}},  
        {"$lookup": {"from": 'propietarios',"localField": '_id',"foreignField": 'Finca',"as": 'propietarios'}}]"""
        cantidad_propietarios = len(datos_dpto_estacionamiento)
        
        recibos = conexion('recibos').find(
            {"Finca": finca, "tipo": tipo,"_id":id}
        )#.sort( 'Fecha_modificacion', -1 )
        datos_subsecciones=json_util.dumps(recibos) #STRING
        datos_subsecciones = json.loads(datos_subsecciones) #LISTA

        #print('SUBSECCIONES >>> ',datos_subsecciones)

        info_finca = conexion('finca').find({'_id': finca})
        datos_finca = json_util.dumps(info_finca) #string
        datos_finca = json.loads(datos_finca) #lista

        tipo_doc = 'pdf' #xlsx o pdf
        if cantidad_propietarios>0:
            #print('entro al if')
            lista_recibos = generar_doc_finca(tipo_doc,datos_dpto_estacionamiento,datos_subsecciones,datos_finca,finca,cantidad_propietarios,fecha_emision,fecha_vencimiento)
            print('LISTA RECIBOS >>> ',lista_recibos) #tipo lista 
            #lista_recibos_dumps = json_util.dumps(lista_recibos)#tipo string
            return json_util.dumps(lista_recibos)
        else:
            print('ERROR DENTRO DEL TRY')
            response = {"status": 400,"mensaje":"No hay propietarios en la finca "+finca}
        print('FINALIZO LA GENERACION DE DOCUMENTOS')
        return response
        #Obtengo:
        #-Subseeciones, monto,mes
        #print('RESPONSE RECIBOS'+datos_subsecciones+'\n')
        """tipo_doc = 'pdf' #xlsx o pdf
        datos = json.loads(response)
        lista = datos[0]['Propietarios']
        cantidad_propietarios = len(lista)
        if cantidad_propietarios>0:
            lista_recibos,url = generar_doc_finca(tipo_doc,datos,finca)
            return Response(json_util.dumps(lista_recibos),mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
        else:
            print('ERROR DENTRO DEL TRY')
            response = {"status": 400,"mensaje":"No hay propietarios en la finca "+finca}
        return response"""
    except Exception as e:
        print('ERROR TRY', str(e))
        response = {"status": 500,"mensaje":"Hubo error al registrar → "+str(e)}
        return response

def listar_recibos():#RNUEVO1
    plantilla = conexion('recibos').find()
    response = json_util.dumps(plantilla)
    return response

def listar_recibos_ID():#RNUEVO2
    print('ENTRANDO A RECIBOS')
    #TIPO 1 → DPTO
    #TIPO 2 → ESTACIONAMIENTO
    finca = request.json["_id"]
    mes = request.json["mes"]#esto sera un numero
    anno = request.json["anno"]
    tipo = request.json["tipo"] 
    try:
        plantilla = conexion('recibos').find({'Finca': finca ,'tipo':tipo}).sort( 'Fecha_modificacion', -1 ).limit(1)
        #plantilla = conexion('recibos').find({'Finca': finca,'Mes':mes,'Year': anno ,'tipo':tipo})
        response = json_util.dumps(plantilla)
        print(plantilla)
        return response
    
    except Exception as e:
        print('ERROR:', str(e))
        response = {"status": 500,"mensaje":"Hubo error al registrar → "+str(e)}
        return response

def crear_recibos():#A TRABAJAR ACA!!
    #TIPO 1 → DPTO
    #TIPO 2 → ESTACIONAMIENTO
    try:
        print('JSON >>> ',request.json)
        finca= request.json["Finca"]
        mes = request.json["Mes"]#esto sera un numero
        year = request.json["Year"]#tipo datetime
        seccion = request.json["Seccion"]
        tipo = request.json["tipo"]
        print('FINCA >>> ',finca)
        print('MES >>> ',mes)
        print('YEAR >>> ',year)
        print('SECCION >>> ',seccion)
        print('TIPO >>>',tipo)
        print(type(seccion))# tipo lista
        #print(lon)
        modificacion = datetime.now()
        _id = generar_id()
        db = conexion('recibos')
        db.insert_one(
                    {"_id": _id,
                    "Finca":finca,
                    "Year":year,
                    "Mes":mes,
                    "tipo":tipo,
                    "Seccion":seccion,
                    #"Seccion.ID_Departamentos":seccion,
                    "Fecha_modificacion":modificacion}
                    
                            )
        """conexion('recibos').insert_one(
            {'_id': id}, {'$set': {"_id": id,
                            "Finca":finca,
                            "Seccion":seccion,
                            "Seccion.ID_Departamentos":seccion,
                            "Fecha_modificacion":modificacion}
                            })"""
        response = {"status": 201,'mensaje': 'Se ha creado satisfactoriamente el recibo del ' + str(mes) + ' del año '+str(year)}
        
        return json_util.dumps(response)
    
    except Exception as e:
        response = {
                "status": 500,
                "mensaje":"Hubo error al actualizar → "+str(e)}
        print('ERROR → '+ str(e))
        return response
       

def actualizar_recibos():#R2
    try:
        print('JSON >>> ',request.json)
        finca= request.json["Finca"]
        mes = request.json["Mes"]#esto sera un numero
        year = request.json["Year"]
        seccion = request.json["Seccion"]
        tipo = request.json["tipo"]

        print('FINCA >>> ',finca)
        print('MES >>> ',mes)
        print('YEAR >>> ',year)
        print('SECCION >>> ',seccion)
        print('TIPO >>>',tipo)
        print(type(seccion))# tipo lista
        #print(lon)
        

        modificacion = agregar_fecha()
        conexion('propietarios').update_one(
            {'_id': id}, {'$set': {"_id": id,
                            "Finca":finca,
                            "Seccion":seccion,
                            "Seccion.ID_Departamentos":seccion,
                            "Fecha_modificacion":modificacion}
                            })
        response = {"status": 201,'mensaje': 'El propietario ' + finca + ' ha sido actualizado satisfactoriamente'}
        
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
