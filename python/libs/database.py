from pymongo import MongoClient

def conexion(tabla):
    url_conexion = 'mongodb+srv://Paino:sistemasMONGO@cluster0.awnp8gy.mongodb.net/videosession?retryWrites=true&w=majority'
    client = MongoClient(url_conexion)
    db = client['videosession']
    colection = db[tabla]
    return colection

"""def conexion(bd,tabla):
    url_conexion = 'mongodb+srv://Paino:sistemasMONGO@cluster0.awnp8gy.mongodb.net/videosession?retryWrites=true&w=majority'
    client = MongoClient(url_conexion)
    db = client[bd]
    colection = db[tabla]
    return colection

conexion(admin1,fincas)"""