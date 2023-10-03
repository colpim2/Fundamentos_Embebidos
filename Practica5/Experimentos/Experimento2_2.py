# Reproduce un video durante 10 segundos y luego muestra imágenes en bucle.
# Detiene la reproducción al insertar una USB y muestra imágenes desde el medio USB.
# Autor: Mauricio Matamoros
# Licencia: MIT

# Modificado por:
#   - Castillo Montes Pamela
#   - Cruz Cedillo Daniel Alejandro
#   - Hernández Jaimes Rogelio Yael
# Fecha: 2023.09.26

# Importación de librerías
import os
import pyudev
import vlc
from time import sleep
import subprocess as sp
import threading

# Definición de hilo global
thread = threading.Thread()

# Bandera de evento de parada
wait_event = threading.Event()

# Definición del reproductor de medios
player = vlc.MediaPlayer()

# Arreglos que contienen las imágenes a reproducir
pics = []
photos = []
usbPath = ""

# Función de finalización de hilos. Cualquier hilo en ejecución se detendrá utilizando la bandera de evento.
# La función join se utilizará si el hilo no ha concluido su ejecución (thread.is_alive()=True) para esperar a que concluya. 
# Luego, se restablece la bandera de evento para habilitar la ejecución de nuevos hilos.
def thread_finalize():
    global wait_event
    global thread
    wait_event.clear()  		# Desactiva la bandera de evento (bloqueo)
    if thread.is_alive():  	# Verifica si el hilo está en ejecución
        thread.join()  				# Espera a que el hilo termine
    wait_event.set()  			# Restablece la bandera de evento.

# Función para imprimir estadísticas de dispositivos
def print_dev_stats(path):
    global photos
    photos = []
    for file in os.listdir(path):
        if file.endswith(".jpg") or file.endswith(".png"):
            photos.append(file)
            print("Imagen encontrada: " + file)
    print("{} tiene {} fotos.".format(path, len(photos)))

# Función para imprimir información de dispositivos
def print_dev_info(device):
    print("Device sys_path: {}".format(device.sys_path))
    print("Device sys_name: {}".format(device.sys_name))
    print("Device sys_number: {}".format(device.sys_number))
    print("Device subsystem: {}".format(device.subsystem))
    print("Device device_type: {}".format(device.device_type))
    print("Device is_initialized: {}".format(device.is_initialized))

# Función para montar automáticamente una USB
def auto_mount(path):
    args = ["udisksctl", "mount", "-b", path]
    sp.run(args)

# Función para obtener el punto de montaje de un dispositivo
def get_mount_point(path):
    args = ["findmnt", "-unl", "-S", path]
    cp = sp.run(args, capture_output=True, text=True)
    out = cp.stdout.split(" ")[0]
    return out

# Función para cargar imágenes desde una USB
def load_usb():
    global usbPath
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem="block", device_type="disk")
    while True:
        action, device = monitor.receive_device()
        if action != "add":
            continue
        print_dev_info(device)
        auto_mount("/dev/" + device.sys_name)
        mp = get_mount_point("/dev/" + device.sys_name)
        print("Mount point: {}".format(mp))
        print_dev_stats(mp)
        usbPath = mp  			# Guardamos la ruta donde está asignada la USB
        thread_finalize()  	# Concluimos el hilo activo (reproducción de fotos base)
        break

# Función para buscar fotos en un directorio
def search_photos(path):
    global photos
    photos = []
    for file in os.listdir(path):
        if file.endswith(".jpg"):
            photos.append(file)

# Función para cargar fotos desde un directorio
def load_photos(path):
    global pics
    global photos
    # Definición de imágenes
    pics = []
    for i in photos:
        print("Foto: " + i)
        pics.append(vlc.Media(f'{path}/{i}'))

# Función para reproducir fotos en bucle
def play_photos():
    global pics
    global wait_event
    while wait_event.is_set():
        for i in pics:
            player.set_media(i)
            player.play()
            sleep(3)
            if wait_event.is_set() == False:  # Si se desactiva la bandera, se suspende la reproducción
                break

# Función MAIN
path = home + "/pictures"
search_photos(path)
load_photos(path)
wait_event.set()

# Crear dos objetos de subproceso
thread = threading.Thread(target=play_photos)
thread.start()
thread2 = threading.Thread(target=load_usb)
thread2.start()
thread2.join()
search_photos(usbPath)
load_photos(usbPath)
thread = threading.Thread(target=play_photos)
thread.start()
thread.join()