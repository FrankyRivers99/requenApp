#funciones.py
import random
import os
import shutil
from OpenSSL import crypto

import gui


#Función para obtener un consejo aleatorio secreto de hacienda 
def hack_secreto():
    hacks= ["Si tu contraseña llegara a fallar, al juego del SAT deberas jugar. (Invierte Mayusculas y minusculas de tu contraseña)", "Si no puedes vincular una factura anterior en parcialidades, activa la carta porte", "Si revisar el rfc quieres por CURP, desberas copiar el URL en otra ventana"]
    random_number = random.randint(0, 2)    
    gui.imprimir_alerta(hacks[random_number])


def buscar_keys():
    ruta_principal = gui.seleccionar_carpeta()    
    ruta_destino = gui.seleccionar_carpeta()
    if not ruta_principal or not ruta_destino:
        gui.imprimir_alerta("No se selecciono la carpeta de busqueda o para guardar el archivo")    
        return
    # Recorrer todos los archivos y subdirectorios de la carpeta principal
    for ruta_actual, directorios, archivos in os.walk(ruta_principal):
        # Filtrar solo los archivos con extensión .Key en la ruta actual
        archivos_key = [archivo for archivo in archivos if archivo.endswith('.key')]

        # Copiar cada archivo .Key encontrado a la carpeta destino
        for archivo in archivos_key:
            ruta_origen = os.path.join(ruta_actual, archivo)
            
            ruta_copia = os.path.join(ruta_destino, archivo)

            # Si el archivo ya existe en la carpeta destino, agregar un contador al nombre
            contador = 1
            while os.path.exists(ruta_copia):
                nombre_sin_extension, extension = os.path.splitext(archivo)
                nombre_modificado = f'{nombre_sin_extension}_{contador}{extension}'
                ruta_copia = os.path.join(ruta_destino, nombre_modificado)
                contador += 1

            shutil.copyfile(ruta_origen, ruta_copia)
    # Imprimir un mensaje para confirmar que se copiaron los archivos
    gui.imprimir_alerta(f"Se copiaron todos los archivos .Key de {ruta_principal} y sus subcarpetas a {ruta_destino}.")    


def buscar_cer_vigentes():
    ruta_base = gui.seleccionar_carpeta()
    ruta_destino = gui.seleccionar_carpeta()
    if not ruta_base or not ruta_destino:
        gui.imprimir_alerta("No se selecciono la carpeta de busqueda o para guardar el archivo")    
        return

    # Recorremos todos los archivos de la carpeta base y sus subcarpetas
    for dirpath, dirnames, filenames in os.walk(ruta_base):
        for filename in filenames:
            # Comprobamos que el archivo sea un certificado en formato .cer
            if filename.endswith(".cer"):
                print("Analizando certificado: " + filename)
                ruta_certificado = os.path.join(dirpath, filename)            
                # Leemos el certificado y comprobamos si está vigente
                try:
                    with open(ruta_certificado, "rb") as f:
                        certificado = crypto.load_certificate(crypto.FILETYPE_ASN1, f.read())
                        print(certificado.has_expired())
                        if certificado.has_expired():
                            continue  # Si ha caducado, pasamos al siguiente archivo
                        # Obtenemos el UniqueIdentifier(RFC) del certificado
                        rfc = certificado.get_subject().x500UniqueIdentifier                        
                        # Creamos la ruta y el nombre del archivo de destino
                        nombre_destino = f"{rfc}.cer"                        
                        ruta_destino_completa = os.path.join(ruta_destino, nombre_destino)
                        # Copiamos el archivo a la carpeta de destino con el nuevo nombre
                        shutil.copy(ruta_certificado, ruta_destino_completa)
                except Exception as e:
                    gui.imprimir_alerta(f"Error al procesar el certificado {filename}: {e}")
                    continue  # Si se genera un error, pasamos al siguiente archivo
    gui.imprimir_alerta("Se buscaron y recolectaron los certificados vigentes")