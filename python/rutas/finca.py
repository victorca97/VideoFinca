from __main__ import app
from flask import jsonify, request, Response
from re_excel import *
from controller.c_finca import *

@app.route("/finca", methods=["GET"])#F1
def ruta_listar_finca():
    response =listar_finca()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca", methods=["DELETE"])#F2
def ruta_eliminar_finca():
    response = eliminar_finca()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca/<id>", methods=["DELETE"])#F3
def ruta_eliminar_finca_ID(id):
    response = eliminar_finca_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca/<id>", methods=["GET"])#F4
def ruta_listar_finca_ID(id):
    response = listar_finca_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca", methods=["POST"])#???
def ruta_crear_finca():
    response = crear_finca()
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/finca/<id>", methods=["PUT"])#P6
def ruta_actualizar_finca_ID(id):
    response = actualizar_finca_ID(id)
    return Response(response , mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    return response