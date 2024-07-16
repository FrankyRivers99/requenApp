#Programa para simplificación de facturas emitidas a excel

import xml.etree.ElementTree as ET
import pandas as pd
import os
from pathlib import Path

#Importamos herramientas de la interfaz
import gui

#Cremos un set de los atributos que nos interesa tener
conceptos_clave = {'Fecha', 'FormaPago', 'SubTotal', 'Moneda', 'Exportacion', 'Total', 'TipoDeComprobante', 'MetodoPago', 'LugarExpedicion', 'Rfc', 'Nombre', 'RegimenFiscal', 'DomicilioFiscalReceptor', 'RegimenFiscalReceptor', 'UsoCFDI', 'ObjetoImp', 'ClaveProdServ', 'Cantidad', 'ClaveUnidad', 'Unidad', 'Descripcion', 'ValorUnitario', 'Importe', 'Base', 'Impuesto', 'TipoFactor', 'TasaOCuota', 'Importe', 'TotalImpuestosTrasladados', 'Base', 'Impuesto', 'TipoFactor', 'TasaOCuota', 'Importe', 'TotaldeRetenciones', 'TotaldeTraslados', 'ImpLocTrasladado', 'TasadeTraslado'}

def tupla_a_diccionario(tupla):
    diccionario = {}
    for clave, valor in tupla:
        diccionario[clave] = valor
    return diccionario

#Cremos una función que itere a travez de una lista de archivos y nos cree una tupla de cada xml
def obtener_informacion_carpeta(lista_Archivos):
    #Creamos la lista que tendra toda la información de los xml
    informen_XML = []
    folio_CFDI = []
    for archivo_xml in lista_Archivos:        
        #Agregamos la dirección del archivo xml que se este procesando
        folio_CFDI.append(Path(archivo_xml).stem)
        print(f"Analizando archivo: {archivo_xml}")
        archivo = get_xml(archivo_xml)
        #Creamos una lista temporal del archivo xml que se este ejecutando
        temp_data = []
        #Agregamos la información despues de que sea depurada
        informen_XML.append(limpieza_xml(formateo_xml(archivo, temp_data)))
        #print("Se guardo la siguiente información: ", temp_data)
    return informen_XML, folio_CFDI

#Creamos una funcion que depura la información inecesaria de un tupla xml
def limpieza_xml(tupla_xml):
    tupla_limpia = []
    #Revisamos las etiquetas en nuestra tupla xml
    for elemento in tupla_xml:        
        #Si la etiqueta es un concepto clave que esta en la lista entonces lo agregamos si no se desecha 
        if elemento[0] in conceptos_clave:
            tupla_limpia.append(elemento)
        else:
            continue
    #Regresams la tupla solo con la información que nos interesa
    return tupla_limpia

#Creamos una funcion que abrira un archivo xml y regresara un objeto xml
def get_xml(nombre_archivo):
    try:
        # Abrimos el archivo
        with open(nombre_archivo, 'r', encoding='utf-8') as xml_file:
            # Leemos el contenido del archivo
            xml_data = xml_file.read()
            # Convertimos el contenido a un objeto XML
            xml_tree = ET.fromstring(xml_data)
            return xml_tree
    except ET.ParseError as parse_err:
        print(f"Error de parseo: {parse_err}")
    except Exception as err:
        print(f"Error: {err}")

def formateo_xml(element, data, indent=""):    
    # Recorremos los atributos del elemento (si tiene)
    for attr, value in element.attrib.items():
        data.append((attr, value))
    

    # Recorremos los hijos del elemento en caso de llegar a tener mas hijos se usa recursion
    for child in element:
        formateo_xml(child, data, indent + "  ")
    return data


#Obtenemos los nombres de los archivos xml de la carpeta
def obtener_rutas_absolutas_xml(carpeta):
    rutas_absolutas_xml = []
    for archivo in os.listdir(carpeta):
        if archivo.endswith('.xml'):
            ruta_absoluta = os.path.join(carpeta, archivo)
            rutas_absolutas_xml.append(ruta_absoluta)
    return rutas_absolutas_xml



def main():
    # Pedir al usuario que seleccione una carpeta
    print("Por favor, selecciona la carpeta:")
    carpeta = gui.seleccionar_carpeta()
    # Verificar si se ha seleccionado una carpeta
    if not carpeta:
        print("No se ha seleccionado ninguna carpeta.")
        return

    # Obtener la lista de archivos XML dentro de la carpeta
    archivos_xml = obtener_rutas_absolutas_xml(carpeta)
    
    #Ejecutamos la función para obtener la informacion de los xml
    informacion_bruta_xml, folios_CFDI = obtener_informacion_carpeta(archivos_xml)

    #Ahora que se tiene toda la información de las facturas solo falta darle el formato
    informacion_final = []
    x=0
    for tupla_datos in informacion_bruta_xml:
        x += 1        
        diccionario = tupla_a_diccionario(tupla_datos)        
        diccionario.update({"CFDI": folios_CFDI[x-1]})
        informacion_final.append(diccionario)
        #Se necesita agregar al diccionario el folio del CFDI
        print(diccionario)
    
    # Convertir los diccionarios en un DataFrame
    df = pd.DataFrame(informacion_final)

    # Guardar el DataFrame en un archivo Excel
    # Ejemplo de cómo usar la función
    nombre_archivo = gui.solicitar_nombre_archivo_xlsx()
    df.to_excel(nombre_archivo, index=False)

    gui.imprimir_alerta("Archivo xlsx creado correctamente")


if __name__ == "__main__":
    main()

#Notas
#Tags importantes SAT para facturas emitidas
#Emisor - Concepto - Traslado - Impuestos - Comprobante - ImpuestosLocales 


