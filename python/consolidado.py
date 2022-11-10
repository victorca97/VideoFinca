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
    varbuffer,cantidad_propietarios,lista_json_excel,año,mes = generar_excel(json,finca) #devuelve la lista con estado,propietario,excel codificado
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
#tipo = 'pdf' #'xlsx' o 'pdf'       
#matriz = generar_doc_finca(tipo)
#print(matriz)