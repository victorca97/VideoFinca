from re_mongoDB import*
from re_excel import convertir_pdf,borrar_temporal,get_url_api

"""if __name__ == "__main__":
    while True:
        json = urls()
        principalv2(json)
        sys.exit()"""
        #crear una funcion asincrona

def generar_doc_finca(tipo,json): #devuelve una matriz con los sgtes datos
    # estado: si se genero correctamente el excel
    # propietario: nombre del propietario
    #path = '../excels/pruebas'#ruta donde se guardaran los excels y pdfs
    #json = get_informacion()#jala el JSON con toda la informacion
    #borrar_temporal()#borra los archivos de la carpeta temporal, dodne estaran los excels y pdfs
    #esto para no llenar la carpeta y q solo se genere cuando lo desee el usuario/cliente
    varbuffer,cantidad_propietarios,lista_json_excel = generar_excel(json) #devuelve la lista con estado,propietario,excel codificado
    if (tipo == 'xlsx'):
        #convertir_pdf(path,tipo)#genera los pdfs
        ruta_url = get_url_api()
        return lista_json_excel,ruta_url
    elif (tipo == 'pdf'):
        lista_json_pdf = convertir_pdf(varbuffer,cantidad_propietarios)
        #retornar el status
        ruta_url = get_url_api()
        return lista_json_pdf,ruta_url
    else:
        print('tipo de extension incorrecto (poner xlsx o pdf)')

#PRUEBA
#tipo = 'pdf' #'xlsx' o 'pdf'       
#matriz = generar_doc_finca(tipo)
#print(matriz)