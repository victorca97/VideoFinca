from __main__ import app
from flask import jsonify, request, Response
from re_excel import *
from controller.c_recibos import *


@app.route("/recibos", methods=["POST"])
def ruta_generar_recibos():#R1
    response = generar_recibos()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca", methods=["GET"])#RNUEVO1 #/plantilla
def ruta_listar_recibos():
    response = listar_recibos()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/plantilla/<id>", methods=["GET"])#RNUEVO2
def ruta_listar_recibos_ID(id):
    response = listar_recibos_ID(id)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/recibos", methods=["PUT"])#RNUEVO3
def ruta_actualizar_recibos():
    response = actualizar_recibos()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}
    
@app.route("/recibos", methods=["DELETE"])#RNUEVO4
def ruta_eliminar_recibos():
    response = eliminar_recibos()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/recibos", methods=["DELETE"])#RNUEVO5
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
