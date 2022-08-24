#!/usr/bin/python
# -*- coding:utf-8 -*-

from ast import Return
from pydoc import doc
from turtle import clear
from numpy import NaN
#from pymongo import MongoClient
from os import system
from datetime import date
from datetime import datetime
import PySimpleGUI27 as sg
now = datetime.now()
import firebase_admin
from firebase_admin import credentials, firestore
#simulacion entrada de Huella
gx_ref_buffer = [
    245,
    3,
    0,
    0,
    0,
    0,
    4,
    245
  ]

#conectar a la base de datos
'''
client = MongoClient("mongodb+srv://tecnoacademiaADMIN:bBTWBBnFDG2aReok@tecnoacademia.mjfzz.mongodb.net/estudiantes?retryWrites=true&w=majority") 
baseDeDatos = client["Tecnoacademia"] #Selecciona la base de datos
collection = baseDeDatos["estudiantes"] #Selecciona la coleccion
'''
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

def registroBD(Huella):
    layout = [[sg.Text('Ingrese su documento de identidad')],
          [sg.Input(size=(15, 1), justification='center', key='input')],
          [sg.Button('1'), sg.Button('2'), sg.Button('3')],
          [sg.Button('4'), sg.Button('5'), sg.Button('6')],
          [sg.Button('7'), sg.Button('8'), sg.Button('9')],
          [sg.Button('Enviar'), sg.Button('0'), sg.Button('Limpiar')]]

    window = sg.Window('Keypad', layout, default_button_element_size=(15,2), auto_size_buttons=False, element_justification='c', no_titlebar=True, location=(0,0), size=(1024,600), keep_on_top=True).Finalize()

    # Loop forever reading the window's values, updating the Input field
    keys_entered = ''
    while True:
        event, values = window.read()  # read the window
        if event == 'Volver': 
            window.close()
        if event == 'Limpiar':  # clear keys if clear button
            keys_entered = ''
        elif event in '1234567890':
            keys_entered = values['input']  # get what's been entered so far
            keys_entered += event  # add the new digit
        elif event == 'Enviar':
            keys_entered = values['input']
            window.close()
            mensaje1 = "El documento de identidad: ", keys_entered, "ha sido registrado"
            sg.popup_ok(mensaje1, no_titlebar=True, location=(0,0), size=(1024,600), keep_on_top=True)
            break
        window['input'].update(keys_entered)  # change the window to reflect current key string   

    '''
    documentoId = keys_entered
        #update_one
    documento= collection.find_one(
            {
                "Numero de identificacion": str(documentoId)
            }
        )
    '''

    docs = firestore_db.collection(u'Datos_Estudiantes').where(u'Número de identificación', u'==', str(keys_entered).replace(".", "").replace(" ", "") ).stream()

    nombre = ""

    for doc in docs:
        #print(f'{doc.id} => {doc.to_dict()}')
        year, month, day, hour, minute = now.year, now.month, now.day, now.hour, now.minute
        dateAndHour = str(day) + "/" + str(month) + "/" + str(year) + ", " + str(hour) + ":" + str(minute)


        nombre_completo = u'{}'.format(doc.to_dict()['Nombre Completo'])
        grado = u'{}'.format(doc.to_dict()['Grado que cursa'])
        institucion = u'{}'.format(doc.to_dict()['Institución Educativa donde estudia (No poner siglas)'])
        documentoIdentidad = u'{}'.format(doc.to_dict()['Número de identificación'])
        tipoID = u'{}'.format(doc.to_dict()['Tipo de identificación'])
        celular = u'{}'.format(doc.to_dict()['Teléfono celular'])
        email = u'{}'.format(doc.to_dict()['Correo electrónico personal (gmail)'])

        nombre = nombre_completo

        firestore_db.collection(u'Asistencia').add({'Nombre completo': nombre_completo, 'No. Identificacion': documentoIdentidad, 'Tipo ID': tipoID, 'Grado': grado, 'Institucion': institucion, 'Celular': celular, 'Email': email, 'FechaYHora': dateAndHour})

    mensaje2 = "Bienvenido, " + nombre + ". Has sido registrado en la base de datos, vuelve a verificar para enviar tu asistencia"
    sg.popup_ok(mensaje2, no_titlebar=True, location=(0,0), size=(1024,600), keep_on_top=True)

    '''
    collection.update_one(
                {"_id": documento["_id"]},
                {
                    "$set": {
                        "Huella": Huella
                    }
                }
            )
    '''
    #print(documentoId)
    #print("aqui deberia ir la huellita")
    #print(Huella)



def validacion(Huella):

    if Huella == []:
        return

    if Huella != []:
        documento= collection.find_one(
            {
                "Huella": Huella
            }
        )

    print(documento, "hola soy el documento")

    if documento == None:
        sg.popup_ok("Huella no registrada", no_titlebar=True, location=(0,0), size=(1024,600), keep_on_top=True)
        print("Huella no registrada")
        print(documento)
        registroBD(Huella)
    if documento != None:
        Fecha = now.strftime('%d-%m-%Y')
        Hora = now.strftime('%H:%M:%S')
        HoraYFecha = [Fecha, Hora]
        print(str(documento["asistencia"]))
        if str(documento["asistencia"]) == "None":
            print("siiuuu")
            collection.update_one(
             {"_id": documento["_id"]},
             {"$set": {
                 "asistencia": [HoraYFecha],
                 "registroDelDia": True
                }
                }
            )
            
            
        if documento["asistencia"] != None:
            collection.update_one(
                {"_id": documento["_id"]},
                {"$set": {
                    "asistencia": documento["asistencia"] + [HoraYFecha],
                    "registroDelDia": True
                }
                }
            )

        sg.popup_ok("Bienvenido " + documento["Nombre Completo "] + " tu asistencia ha sido registrada", no_titlebar=True, location=(0,0), size=(1024,600), keep_on_top=True)


# validacion(gx_ref_buffer)
