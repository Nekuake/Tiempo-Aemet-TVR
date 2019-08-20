import requests
import urllib.request
import pprint
import json
import os
import ssl


webcams = ['logrono', 'haroo', 'calahorra']
urlprediccionhoy = "https://opendata.aemet.es/opendata/api/prediccion/ccaa/hoy/rio"



def descargarwebcams(nombrepoblacion):
    archivopoblacion = open(nombrepoblacion + '.jpg', 'wb')
    urldewebcam = ('https://actualidad.larioja.org/images/webcam/' + nombrepoblacion + '.jpg')
    print('Descargando imagen de webcam desde ' + urldewebcam)
    archivopoblacion.write(requests.get(urldewebcam).content)
    archivopoblacion.close()

def llamadaapi(urldellamada, claveapi):
    payload = ""
    headers = {
        'accept': "application/json",
        'api_key': "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhaHVydGFkb0B0dnJpb2phLmNvbSIsImp0aSI6IjBiYzQxMGQyLTc1NjAtNDYyMS05ZjgxLTEwOWE4N2YxZDE2YSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTY1Njk1OTk2LCJ1c2VySWQiOiIwYmM0MTBkMi03NTYwLTQ2MjEtOWY4MS0xMDlhODdmMWQxNmEiLCJyb2xlIjoiIn0.kykNwBojwUwqO8r16SZ1NfdLxV2Bv-PR1PJUpBhxBMM"
    }
    respuesdeapi = requests.request("GET", urldellamada, data=payload, headers=headers)
    diccionarioderespuesta = json.loads(respuesdeapi.text)
    urlrespuesta = diccionarioderespuesta.get('datos', None)
    print(urlrespuesta)
    leerurl = urllib.request.urlopen(urlrespuesta)
    textoderespuesta = leerurl.read()

    return textoderespuesta
#Hay que hacer esto porque da error al intentar parsear el html por utilizar https y no detectar los certificados bien
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# Utilizando la función, descarga las imágenes de las webcam
for poblaciones in webcams:
    descargarwebcams(poblaciones)
# Ahora descargaremos en un archivo de texto las predicciones utilizando la API Open Data de AEMET
print(llamadaapi('https://opendata.aemet.es/opendata/api/prediccion/ccaa/hoy/rio', ''))
print(llamadaapi('https://opendata.aemet.es/opendata/api/prediccion/ccaa/hoy/rio', ''))

