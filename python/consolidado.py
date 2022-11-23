from re_mongoDB import*
from re_excel import convertir_pdf,get_url_api

#crear una funcion asincrona
#NOTAS
# validar si existe el año de la carpeta, sino crearla (2022 → enero, febrero ,....)
# nombre del archivo : recibo_mes_nombrepropietario (solo PDF)

# fincas
# --nombrepropietario
#   -- año
#       -- recibo_mes_nombrepropietario

def generar_doc_finca(tipo,json,finca): #devuelve una matriz con los sgtes datos
    # estado: si se genero correctamente el excel
    # propietario: nombre del propietario
    # path = '../excels/pruebas'#ruta donde se guardaran los excels y pdfs
    # json = get_informacion()#jala el JSON con toda la informacion
    # esto para no llenar la carpeta y q solo se genere cuando lo desee el usuario/cliente
    varbuffer,cantidad_propietarios,lista_json_excel,año,mes = generar_excel_propietarios(json,finca) #devuelve la lista con estado,propietario,excel codificado
    if cantidad_propietarios!=0:
        if (tipo == 'xlsx'):
            #convertir_pdf(path,tipo)#genera los pdfs
            ruta_url = get_url_api()
            return lista_json_excel,ruta_url
        elif (tipo == 'pdf'):
            lista_json_pdf = convertir_pdf(varbuffer,cantidad_propietarios,finca,año,mes)
            #retornar el status
            ruta_url = get_url_api()
            return lista_json_pdf,ruta_url
        else:
            print('tipo de extension incorrecto (poner xlsx o pdf)')
    else:
        print('No hay propietarios en la finca ',finca)
#PRUEBA
#finca= "20c2a823-0646-4397-ba7e-5f8797e6223d"  #deberia haber 3 propietarios ( al 21/11/2022)
#borrar_temporal()
#query_finca=[{ "$match": {"_id": f'{finca}' }}, 
#{"$lookup": {"from": 'plantilla',"localField": '_id',"foreignField": 'Finca',"as": 'Plantillas'}},  
#{"$lookup": {"from": 'propietarios',"localField": '_id',"foreignField": 'Finca',"as": 'Propietarios'}}]
#resultados =conexion('finca').aggregate(query_finca)
#print('RESULTADOS >>>>>>>>>>', resultados)
#response=json_util.dumps(resultados)
#print('response >>>>>>>>', response)
#tipo = 'pdf' #xlsx o pdf
#datos = json.loads(response)
#print('datos>>>>>>>>', datos)
#lista = datos[0]['Propietarios']
#cantidad_propietarios = len(lista)
#if cantidad_propietarios>0:
    #lista_recibos,url = generar_doc_finca(tipo,datos,finca)
