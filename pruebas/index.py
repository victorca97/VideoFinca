from typing import Collection
import pymongo
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from bson.objectid import ObjectId

MONGO_HOST = 'localhost'
MONGO_PUERTO = '27017'
MONGO_TIEMPO_FUERA = 1000

MONGO_URI = 'mongodb://'+MONGO_HOST+':'+MONGO_PUERTO+'/'

MONGO_BASEDATOS = 'Escuela'
MONGO_COLECCION = 'Alumnos'

cliente = pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos = cliente[MONGO_BASEDATOS]
coleccion = baseDatos[MONGO_COLECCION]

def monstrar_datos():
    try:
        #PARA EVITAR DE SE SOBREESCRIBNA EN LA TABLA
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        for documento in coleccion.find():
            #(registro padre → '' no hay o no tiene,indice,ID,valor)
            tabla.insert('',0,text=documento['_id'],values=documento['nombre'])
        #cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print('Tiempo excedido '+errorTiempo)
    except pymongo.errors.ConnectionFailure as errorConexion:
        print('Fallo al conectarse a mongodb'+errorConexion)
def crearRegistro():
    if len(nombre.get())!=0 and len(calificacion.get())!=0 and len(sexo.get())!=0:
        try:
            documento = {'nombre':nombre.get(),'calificacion':calificacion.get(),'sexo':sexo.get()}
            coleccion.insert_one(documento)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message='Los campos no pueden estar vacios')
    monstrar_datos()
def dobleClickTabla(event):
    global ID_ALUMNO
    ID_ALUMNO = str(tabla.item(tabla.selection())['text'])
    #print(ID_ALUMNO)
    documento = coleccion.find({'_id':ObjectId(ID_ALUMNO)})
    nombre.delete(0,END)
    nombre.insert(0,documento['nombre'])
    sexo.delete(0,END)
    sexo.insert(0,documento['sexo'])
    calificacion.delete(0,END)
    calificacion.insert(0,documento['calificacion'])
    crear['state']='disabled'
    editar['state']='normal'
def editarRegistro():
    pass

ventana = Tk()
tabla=ttk.Treeview(ventana,columns=2)
tabla.grid(row=1,column=0,columnspan=2)#columnspan es abarcar dos columnas
tabla.heading('#0',text='ID')#(numero de cabecera,nombre de la cabecera)
tabla.heading('#1',text='Nombre')
tabla.bind('<Double-Button-1>',dobleClickTabla)#1 es el click izquierdo,2 derecho
#nombre
Label(ventana,text='Nombre').grid(row=2,column=0)
nombre =Entry(ventana)
nombre.grid(row=2,column=1)

#sexo
Label(ventana,text='Sexo').grid(row=3,column=0)
sexo =Entry(ventana)
sexo.grid(row=3,column=1)

#calificacion
Label(ventana,text='Calificacion').grid(row=4,column=0)
calificacion =Entry(ventana)
calificacion.grid(row=4,column=1)

#boton crear
crear = Button(ventana,text='crear alumno',command=crearRegistro,bg='green',fg='white')
crear.grid(row=5,columnspan=2)

#boton editar
editar=Button(ventana,text='editar alumno',command=editarRegistro,bg='yellow',fg='white')
editar.grid(row=6,columnspan=2)
editar['state']='disabled'
monstrar_datos()
ventana.mainloop()