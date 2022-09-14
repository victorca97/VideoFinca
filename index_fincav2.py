from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
import sys
base_datos =MongoClient().ag 
#Leer los datos de la BD
def leer_db(coleccion):
    bd=coleccion.find()
    for r in bd:
        #print(r['Nombre']) para leer un atributo de la BD
        print(r)

if __name__ == "__main__":
    while True:
        MONGO_HOST="localhost"
        MONGO_PUERTO="27017"
        MONGO_TIEMPO_FUERA=1000
        MONGO_URL="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

        client = MongoClient(MONGO_URL)
        db=client["VideoFinca"]
        collection1 = db["Admin"]
        collection2 = db["Finca"]
        cursor = collection2.find()
        lista_prueba=list(cursor)
        i = len(lista_prueba) #sale dos
        print(i)
        """print(lista_prueba)
        finca = ["Finca0001","Finca0002"]
        for f in finca:
            plantilla2=[
        {
        "$match": {
            "_id": f'{f}'
        }
        },  
        {
        "$lookup": {
            "from": 'Plantilla',
            "localField": '_id',
            "foreignField": 'Finca',
            "as": 'Plantillas'
        }
        },  
        {
        "$lookup": {
            "from": 'Propietario',
            "localField": '_id',
            "foreignField": 'Finca',
            "as": 'Propietarios'
        }
        }    
    ]
            resultados2 =collection2.aggregate(plantilla2)
            #cursor = resultados2.find()
            list_cur = list(resultados2) #esto es una lista

            direccion=list_cur[0]['Direccion']
            print(direccion)"""
        
        sys.exit()