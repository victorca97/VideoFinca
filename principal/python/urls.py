from tkinter import E
import requests

def urls():
    try:
        url_propietarios='http://192.168.195.12:4000/propietarios'

        d = requests.get(url_propietarios)
        json=d.json()
        #print(type(json[0]))
        return json
    except  Exception as e:
        print('error: ',e)

json =urls()
print(json)