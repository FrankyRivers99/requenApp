import os
import filecmp

# Definir la ruta de la carpeta a revisar
ruta_carpeta = "C:\\Users\\frank.DESKTOP-JV56D1V\\Desktop\\Certificados\\Llaves"

# Recorrer todos los archivos en la carpeta
archivos = os.listdir(ruta_carpeta)

# Comparar cada archivo con los archivos restantes para eliminar duplicados
for i in range(len(archivos)):
    archivo1 = archivos[i]
    ruta1 = os.path.join(ruta_carpeta, archivo1)

    for j in range(i+1, len(archivos)):
        archivo2 = archivos[j]
        ruta2 = os.path.join(ruta_carpeta, archivo2)

        # Intentar comparar los archivos
        try:
            # Si los archivos son iguales, eliminar el segundo archivo
            if filecmp.cmp(ruta1, ruta2):
                os.remove(ruta2)
                print(f'Se eliminó el archivo {ruta2} por ser una copia de {ruta1}.')
        except Exception as e:
            print(f'Error al comparar los archivos {ruta1} y {ruta2}: {e}')
            continue

# Imprimir un mensaje para confirmar que se eliminaron los archivos duplicados
print(f'Se eliminaron los archivos duplicados en {ruta_carpeta}.')