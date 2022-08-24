import PySimpleGUI27 as sg
from Lector_huella import VerifyUser
from funcionesBD import registroBD
        
 
def verificar():
    layout = [[sg
    .Text("Dale click a Enviar y coloca tu huella en el lector")],
          [sg.Image(filename='/home/pi/Desktop/codigo de pruebas/pysimplegui-master/correcta.png')],
        #   [sg.Button("Volver", font=('Helvetica', 18))],
          [sg.Button("Enviar", font=('Helvetica', 18))]]
    window = sg.Window('Keypad', layout, default_button_element_size=(15,2), auto_size_buttons=False, element_justification='c', no_titlebar=True, location=(0,0), size=(1024,600), keep_on_top=True).Finalize()
    event, values = window.read()  # read the window
    if event == "Enviar":
        VerifyUser()
        window.close()
    if event == 'Volver': 
        window.close()
        ventanaPrincipal()
    sg.popup_ok("No se pudo verificar, intenta nuevamente", no_titlebar=True, location=(0,0), size=(1024,600), keep_on_top=True)
    window.close()
    #ventanaPrincipal()

def ventanaPrincipal():
    layout = [
        [sg.Image(filename='/home/pi/Desktop/codigo de pruebas/pysimplegui-master/logo.png')],
        [sg.Text('Bienvenido', font=('Helvetica', 25), justification='center')],
        [sg.Text("*Haz click en Verificar para comenzar el registro de asistencia", font=('Helvetica', 12), text_color='blue')],
        [sg.Button('Verificar', font=('Helvetica', 18))]]

    window = sg.Window('Tecnoacademia', layout, default_button_element_size=(
        15, 2), auto_size_buttons=False, element_justification='c', no_titlebar=True, location=(0,0), size=(1024,600), keep_on_top=True).Finalize()

    event, values = window.read()
    if event == "Verificar":
        window.close()
        verificar()

ventanaPrincipal()