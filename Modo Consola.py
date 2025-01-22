import os
import json
import Baul
import requests
import logging
import sys
import csv
from datetime import datetime
#import getpass       # no me gusta como funciona

# *******************************************************************
# ------------            Area  de  Funciones          --------------
# *******************************************************************
def ConfigurarMensajeLogging():
    """
    Parámetros: None
    Valor de retorno: None
    Notas:
        Fn que al ser invocada configura el Formato de mensaje a mostrar por logging.error. 
    Referencias: None
    """
    # Configuración de logging:configurará el formato de los mensajes de logging para que incluyan la fecha y hora, _ 
                                                                        #el nivel de logging y el mensaje de logging.
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
# -------------------------------------------------------------------
def DeterminarRutaAcceso():
    """
    Parámetros:
        parametros: None
    Valor de retorno:
        STRING: carpetaRaizAplicacion 
    Notas:
        Fn que al ser invocada devuelve la RUTA DE ACCESO de la CARPETA RAIZ. 
    Referencias: None
    """
    rutaAbsolutaAplicacion = os.path.abspath(__file__)                          # Obtener el path del archivo Python(path absoluta: _
                                                                                    # carpeta + nombre archivo)
    nombreArchivo = os.path.basename(rutaAbsolutaAplicacion)                    # Obtener el nombre del archivo
    rutaAbsolutaAplicacion.replace('\\','\\\\')                                 # convierto en ruta valedera en Py (reemplazo \ por \\)
    carpetaRaizAplicacion = rutaAbsolutaAplicacion.replace(nombreArchivo,"")    # de este string reemplazo el nombreArchivo por "" para que  
                                                                                # quede la _ruta de acceso limpia de nombre de archivo(mail)
    return carpetaRaizAplicacion
# -------------------------------------------------------------------
def AbrirArchivoJson(carpetaRaizAplicacion,archivoJson):
    """
    Parámetros:
        STRING: carpetaRaizAplicacion (RUTA ACCESO de carpeta RAIZ)
        STRING: archivoJson (NOMBRE de archivo a abrir)
    Valor de retorno:
        DICCIONARIO: diccionarioUsuarios 
    Notas:
        Fn que al ser invocada devuelve un DICCIONARIO con todos los DATOS de USUARIOS validados. 
    Referencias: None
    """
    with open(carpetaRaizAplicacion + archivoJson, 'r') as archivo:             # Abrir archivo Json como ARCHIVO
        diccionarioUsuarios = json.load(archivo)                                # Cargar los datos del archivo JSON
        return diccionarioUsuarios                                              # Retorna el diccionario de usuarios _
                                                                                # (al salir del With cierra automaticamente el archivo Json abierto)  
# -------------------------------------------------------------------
def ValidarUsuario(usuario,contraseña,diccionarioUsuarios):
    """
    Parámetros:
        STRING: usuario (dato ingresado por teclado)
        STRING: contraseña (dato ingresado por teclado)
        DICCIONARIO: diccionarioUsuarios (contiene todos los user-pass validados en sistema)
    Valor de retorno:
        BOOLEAN: usuarioCorrecto
        BOOLEAN: contraseñaCorrecta
    Notas:
        Fn que al ser invocada devuelve 2 PARAMETROS para determinar la VALIDACION de USUARIO. 
    Referencias: None
    """        
    usuarioCorrecto, contraseñaCorrecta = False, False                          # Inicializo en false (usando asignacion multiple)
    for llave in diccionarioUsuarios:                                           # Itero en todos los registros de diccionario 
        if usuario == llave['usuario']:                                         # If para determinar los valores (boolean) de _ 
                                                                                    # usuarioCorrecto y contraseñaCorrecta
            usuarioCorrecto = True
            if contraseña == llave['password']:
                contraseñaCorrecta = True
                return usuarioCorrecto, contraseñaCorrecta 
            else:
                contraseñaCorrecta = False
        else:
            contraseñaCorrecta = False
        
    return usuarioCorrecto, contraseñaCorrecta   
# -------------------------------------------------------------------
def IngresoUserPass():
    """
    Parámetros:
        None
    Valor de retorno:
        String: usuario
        String: contraseña
    Notas:
        Fn que al ser invocada pide el ingreso por teclado de Usuario y Contraseña. 
    Referencias: None
    """ 
    usuario = input("Ingrese \033[92mNombre de Usuario:  \033[0m")
#    contraseña = getpass.getpass("Ingrese \033[92mContraseña:  \033[0m")        # get.pass.getpass no muestra los caracteres ingresado
                                                                                            # (no me gusta la forma de interactuar en consola)
    contraseña = input("Ingrese \033[92mContraseña:  \033[0m")
    return usuario, contraseña
# -------------------------------------------------------------------
def ValidarAcceso(usuarioCorrecto, contraseñaCorrecta):
    """
    Parámetros:
        Boolean: usuarioCorrecto 
        Boolean: contraseñaCorrecta
    Valor de retorno:
        Boolean: accesoValido
    Notas:
        Fn que al ser invocada devuelve 1 PARAMETRO para VALIDAR O NO el ACCESO. 
    Referencias: Usa variables globales (usuario, contraseña, reintentar)
    """ 
    global usuario, contraseña, reintentar

    if usuarioCorrecto and contraseñaCorrecta:                                  # acceso exitoso
        accesoValido = True
        reintentar = False                                                     
    elif usuarioCorrecto:                                                       # acceso fallido (fallo la contraseña)
        print(f"Contraseña incorrecta:  \033[91m{contraseña}\033[0m")
        print("\033[95m\nNo debería mostrarse la contraseña.\nLo hago solo para verificar el flujo de datos\n\n\033[0m")

        accesoValido = False
        reintentar = Baul.Reintentar(reintentar)                                 
    else:                                                                       # acceso fallido (fallo el nombre de usuario)
        print(f"Usuario incorrecto:  \033[91m{usuario}\033[0m")
        accesoValido = False
        reintentar = Baul.Reintentar(reintentar)                                                    
             
    return accesoValido
# -------------------------------------------------------------------
def CotizacionDolarOficial():
    """
    Parámetros: None
    Valor de retorno:
        Float: cambio['compra']
    Notas:
        Fn que al ser invocada devuelve COTIZACION OFICIAL DEL DOLAR COMPRA. 
    Referencias: None
    """
    # Configuración de logging:configurará el formato de los mensajes de logging para que incluyan la fecha y hora, _ 
                                # el nivel de logging y el mensaje de logging.
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

    url = 'https://dolarapi.com/v1/dolares'                                     #
    try:
        enlace = requests.get(url)                                          # envía una solicitud (de solo lectura) HTTP GET a la URL.) 
        if enlace.status_code == 200:                                       # El código 200 indica que la solicitud fue exitosa _
                                                                                        # y que el servidor devolvió los datos solicitados.
            datosDeUrl = enlace.json()                                      # convierte la respuesta del servidor en un objeto JSON _
                                                                                                    #(es una lista de diccionarios).
            for cambio in datosDeUrl:                                       # Itero buscando el diccionario que contenga 'nombre=oficial'
                if cambio['nombre'] == 'Oficial':
                    return float(cambio['compra'])                          # return la cotizacion de 'compra' del dolar 'oficial'.
            return None                                     
        else:
            print("\n\033[91mError al obtener la cotización del dólar.\033[0m")
    except requests.exceptions.HTTPError as errh:                           # se activa si no encuentra el URL
        logging.error(f"\n\033[91mNo se encontró la URL {url}: {errh}\033[0m")
    except requests.exceptions.ConnectionError as errc:                     # se activa si hay error de conexion
        logging.error(f"\n\033[91mError de conexión al intentar acceder a la URL {url}: {errc}\033[0m")
    except Exception as e:                                                  # se activa con otros tipos (distinto de los anteriores) _
                                                                                                    #_de error que pudieran ocurrir
        exc_type, exc_obj, exc_tb = sys.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line_num = exc_tb.tb_lineno
        logging.error(f"\n\033[91mOcurrió un error en el archivo {filename},\nen Línea {line_num}: {e}\033[0m")
    Baul.Pausa()
# -------------------------------------------------------------------
def AbrirProductosCsv(carpetaRaizAplicacion, productosCsv):
    """
    Parámetros:
        String: carpetaRaizAplicacion 
        String: productosCsv
    Valor de retorno:
        Objeto: archivoProductos del tipo file
        Objeto: objetoProductos del tipo _csv.reader
    Notas:
        Fn que al ser invocada devuelve 2 Objetos (abiertos) para su proceso. 
    Referencias: None
    """ 
    # Abrir el producto.csv (cada fila de este ARCHIVO (objeto) es una LISTA DE VALORES)
    archivoProductos = open(carpetaRaizAplicacion + productosCsv, 'r')
    # Crear un objeto CSV 
    objetoProductos = csv.reader(archivoProductos)                          # Creo un objeto de clase _csv.reader. Es iterador. _
                                                                                    # En cada iteración de 1 bucle, el objeto_
                                                                                    # objetoProductos devuelve _
                                                                                    # la siguiente fila del archivo CSV.
#    print(objetoProductos.__class__)                                                                        

   # archivoProductos queda abierto por necesidad (por eso no uso with que cierra automaticamente)
   # archivoProductos lo cierro en cuerpo principal                                                                              
    return archivoProductos, objetoProductos 
# -------------------------------------------------------------------
def AbrirHistorialCsv(carpetaRaizAplicacion, historialPrecioCsv):
    """
    Parámetros:
        String: carpetaRaizAplicacion 
        String: historialPrecioCsv
    Valor de retorno:
        Objeto: archivoHistorial del tipo file
        Objeto: objetoHistorial del tipo _csv.reader
    Notas:
        Fn que al ser invocada devuelve 2 Objetos (abiertos) para su proceso. 
    Referencias: None
    """ 
    # Abrir el historial.csv (cada fila de este ARCHIVO (objeto) es una LISTA DE VALORES)
    archivoHistorial = open(carpetaRaizAplicacion + historialPrecioCsv, 'a', newline='')
    # Crear un objeto CSV 
    objetoHistorial = csv.reader(archivoHistorial)                          # Creo un objeto de clase _csv.reader. Es iterador. _
                                                                                   # En cada iteración de 1 bucle, el objeto_
                                                                                   # objetoHistorial devuelve _
                                                                                   # la siguiente fila del archivo CSV.
#    print(objetoHistorial.__class__)                                                                        

    # archivoProductos queda abierto por necesidad (por eso no uso with que cierra automaticamente)
    # archivoProductos lo cierro en cuerpo principal                                                                              
        
    return archivoHistorial, objetoHistorial
# -------------------------------------------------------------------
def CargarHistorialPrecio(archivoProductos, objetoProductos, archivoHistorial, objetoHistorial, cotizacionOficialCompra):
    """
    Parámetros:
        Objeto: archivoProductos del tipo file 
        Objeto: objetoProductos del tipo _csv.reader
        Objeto: archivoHistorial del tipo file
        Objeto: objetoHistorial del tipo _csv.reader
         Float: cotizacionOficialCompra
    Valor de retorno:
        None
    Notas:
        Fn que al ser invocada procesa los datos, carga en archivo "historial_precios.csv"
        y muestra los resultados en consola(a travez de la invocacion de fn Monitor).
    """ 
    global fechaHora, fechaHora
    
    # Saltar la primera fila (encabezados)
    next(objetoProductos)
    # Crear una lista con fecha y hora actual
    fechaHora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nuevoRegistroHistorico = [fechaHora]

    Monitor()

    # Acceder a los datos
    for fila in objetoProductos:
        producto=fila[0]
        precio = float(fila[1])
        print(f"{producto}   -   {precio * cotizacionOficialCompra}")
        nuevoRegistroHistorico.append(precio * cotizacionOficialCompra)

#    print(nuevoRegistroHistorico) 
    # Crear un objeto writer
    writer = csv.writer(archivoHistorial)
    # Escribir el nuevo registro
    writer.writerow(nuevoRegistroHistorico)
    print('Registro agregado correctamente')  
#    print(archivoProductos.closed)                         # Verifico si esta cerradp el archivo
# -------------------------------------------------------------------
def VerificarExistenciaArchivo(ruta, archivo):
    """
    Parámetros:
        String: ruta 
        String: archivo
    Valor de retorno:
        None
    Notas:
        Fn que al ser invocada verifica la existencia del archivo en la ruta (recibidas por parametros).
    """
    if not(os.path.exists(ruta + archivo)):
        print(f"\nEl archivo --> \033[95m{ruta}\033[0m\033[92m{archivo}\033[0m \n\033[91mNO EXISTE EN ESTE DIRECTORIO.\033[0m\n")
        print(f"\033[93mError en tiempo de ejecucion!!!. \nVerifique existencia del archivo REQUERIDO.\033[0m\n")
        exit()    

# -------------------------------------------------------------------
def Monitor():
    global usuario, fechaHora, cotizacionOficialCompra
    Baul.LimpiarPantalla()
    print(f"\n   \033[4m\033[92mUsuario:\033[0m {usuario}         \033[4m\033[92mFecha:\033[0m {fechaHora}         \033[4m\033[92mCotizacion Dolar:\033[0m {cotizacionOficialCompra}\n")
    print("\033[4m\033[94mNomProducto\033[0m      \033[4m\033[94mNomPrecio\033[0m  ")

# *******************************************************************
# ------------            CUERPO PRINCIPAL             --------------
# *******************************************************************
Baul.LimpiarPantalla()
       
usuariosJson = "auth_usuarios.json"
productosCsv = "productos.csv"
historialPrecioCsv = "historial_precios.csv"

carpetaRaizAplicacion = DeterminarRutaAcceso()
    
# antes que nada verifico que los 3 archivos requeridos se encuentren en el directorio raiz
VerificarExistenciaArchivo(carpetaRaizAplicacion, usuariosJson)         # Verifico si "auth_usuarios.json" esta en el directorio raiz
VerificarExistenciaArchivo(carpetaRaizAplicacion, productosCsv)         # Verifico si "productos.csv" esta en el directorio raiz
VerificarExistenciaArchivo(carpetaRaizAplicacion, historialPrecioCsv)   # Verifico si "historial_precios.csv" esta en el directorio raiz

diccionarioUsuarios = AbrirArchivoJson(carpetaRaizAplicacion,usuariosJson)

reintentar = True
while reintentar:
    usuario, contraseña = IngresoUserPass()
    
    usuarioCorrecto, contraseñaCorrecta = ValidarUsuario(usuario,contraseña,diccionarioUsuarios)
    
    accesoValido = ValidarAcceso(usuarioCorrecto, contraseñaCorrecta)

# ***  Acá deberia evaluar los permisos concedidos al Usuario logueado  ***    

if accesoValido:                                                                
    #funcionalidad ACTUALIZAR PRECIOS            ****  Acá deberia evaluar los permisos concedidos al Usuario logueado  ****
    cotizacionOficialCompra = CotizacionDolarOficial()
    if cotizacionOficialCompra:
        print(f"\nCotización del dólar oficial: \033[92m{cotizacionOficialCompra}\033[0m\n")
        archivoProductos, objetoProductos = AbrirProductosCsv(carpetaRaizAplicacion, productosCsv)
        archivoHistorial, objetoHistorial = AbrirHistorialCsv(carpetaRaizAplicacion, historialPrecioCsv)
        CargarHistorialPrecio(archivoProductos, objetoProductos, archivoHistorial, objetoHistorial, cotizacionOficialCompra)
        # Cerrar el archivos abiertos
        archivoProductos.close()
        archivoHistorial.close()
    else:
        print("\n\033[91mNo se encontró la cotización del dólar oficial.\033[0m")
else:
    print("\n\033[91mAl CAMPITO man\n\033[91m")
  
Baul.Pausa()
