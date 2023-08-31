import qrcode
import requests
import os
from flask import Flask, request, render_template
from whatsapp_api_client_python import API

#greenapi
greenAPI = API.GreenApi(
    "yourinstance", "yourapikey"
)

# Flask constructor
app = Flask(__name__)

img = os.path.join('static', 'images')

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    ## Display the HTML form template
    return render_template('index.html')

def MakeQR(codigo, nombre):
    obj = qrcode.make(
        "CODIGO QR de ACCESO a la fiesta UDG"+"\n"+
        "valida que la persona con"+"\n"+
        "codigo: "+codigo+"\n"+"&"+"\n"+
        "nombre: "+nombre+"\n"
        "fue  REGISTRADA CORRECTAMENTE")
        #/home/angelaguayo1993/mysite/static/images
    imgQR = open("/home/angelaguayo1993/mysite/static/images/QR-"+codigo.replace(" ", "")+"-"+nombre.replace(" ", "")+".png", "wb")
    obj.save(imgQR)

    imgQR.close()
    return "QR-"+codigo.replace(" ", "")+"-"+nombre.replace(" ", "")+".png"

def SendMSG(numero,ruta,countrycode,nombre):
    if countrycode == "52":
        countrycode = "521"

    print(countrycode)
    greenAPI = API.GreenApi("instance", "yourapikey")
    response = greenAPI.sending.sendMessage(countrycode+numero+"@c.us", "su registroha sido efectuado satisfactoriamente: "+nombre)
    ########################################################################################


    #######################################################################################
    url = "https://api.green-api.com/waInstance"yourinstance"/sendFileByUpload/yourapikey"
    payload = {'chatId': countrycode+numero+'@c.us',
    'caption': 'QR code'}
    files = [
    ('file', (ruta, open('/home/angelaguayo1993/mysite/static/images/'+ruta,'rb'),'image/png'))
    ]
    headers= {}

    response1 = requests.request("POST", url, headers = headers, data = payload, files = files)

    print(response1.text.encode('utf8'))
    ########################################################################################

# `read-form` endpoint
@app.route('/read-form', methods=['POST'])
def read_form():
    data = request.form
    nombre=data['usernombre']
    codigo=data['usercodigo']
    numero=data['usernumero']
    countrycode = data['countryCode']
    ruta = MakeQR(codigo,nombre)
    SendMSG(numero,ruta,countrycode,nombre)
    cadena = "CODIGO QR de ACCESO a la fiesta UDG \n valida que la persona con codigo: "+codigo+"\n  &\n nombre: "+nombre+"\n fue  REGISTRADA CORRECTAMENTE"
    #cadena ="hola muchachos"
    file = os.path.join(img,ruta)
    return render_template('greeting.html', nombre = nombre, codigo = codigo,cadena = cadena,ruta=ruta, file=file,numero=numero)


# Main Driver Function
if __name__ == '__main__':
    # Run the application on the local development server
    app.run()
