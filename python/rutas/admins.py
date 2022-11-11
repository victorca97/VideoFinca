from __main__ import app
from flask import jsonify, request, Response
from re_excel import *
from controller.c_admins import *

@app.route("/admins", methods=["GET"])#F1
def ruta_listar_admins():
    response =listar_admins()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/admins", methods=["DELETE"]) 
def ruta_eliminar_admins():
    response = eliminar_admins()
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/admins/<id>", methods=["DELETE"])
def ruta_eliminar_admins_ID(id):
    response = eliminar_admins_ID(id)
    return Response(response, mimetype="application/json"),{"Access-Control-Allow-Origin": "*"}

@app.route("/admins/<id>", methods=["PUT"])
def ruta_actualizar_admins_ID(id):
    response = actualizar_admins_ID(id)

def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    return response