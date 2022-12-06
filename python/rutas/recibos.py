from __main__ import app
from flask import jsonify, request, Response
from re_excel import *
from controller.c_recibos import *
#RECIBOS PARA ESTACIONAMIENTO Y DEPARTAMENTO, PONERLE POR TIPO

@app.route("/recibos_generar", methods=["POST"])#"/recibos"
def ruta_generar_recibos():#R1
    response = generar_recibos()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

#CREAR RECIBOS
@app.route("/recibos_crear", methods=["POST"])#"/recibos"
def ruta_crear_recibos():#R1
    response = crear_recibos()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/recibos", methods=["GET"])#RNUEVO1 #/plantilla
def ruta_listar_recibos():
    response = listar_recibos()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/recibo", methods=["POST"])#RNUEVO2
def ruta_listar_recibos_ID():
    response = listar_recibos_ID()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/recibos", methods=["PUT"])#RNUEVO3
def ruta_actualizar_recibos():
    response = actualizar_recibos()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/recibos/<id>", methods=["DELETE"])#RNUEVO5
def ruta_eliminar_recibos_ID(id):
    response = eliminar_recibos_ID(id)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/plantilla", methods=["GET"])#RNUEVO6
def ruta_listar_secciones():
    response = listar_secciones()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    return response
