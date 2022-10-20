import requests

def get_informacion():
    try:
        url_propietarios=f'http://192.168.195.12:4000/berrios'

        d = requests.get(url_propietarios)
        json=d.json()
        #print(type(json[0]))
        return json
    except  Exception as e:
        print('error: ',e)