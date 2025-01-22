import os
import json
import requests
import sys
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# *******************************************************************
# ------------        Funciones PROCESOS DE DATOS      --------------
# *******************************************************************
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
        messagebox.showinfo("Error en tiempo de ejecucion!!!", f"Path: {ruta}\nó\nArchivo: {archivo}\nNO EXISTE.")
        exit()                                              # Si la ruta o al archivo no existe CORTO LA EJECUCION del programa  
# -------------------------------------------------------------------
def ValidarUsuario():
    """
    Parámetros:
        parametros: None
    Valor de retorno:
        None:  
    Notas:
        Fn que al ser invocada VALIDA el ingreso a la APP. 
    Referencias: None
    """
    diccionarioUsuarios = AbrirArchivoJson(carpetaRaizAplicacion,usuariosJson)
    
    usuario=AccesoTkUsuario.get()
    contraseña=AccesoTkContraseña.get()
    
    for i in diccionarioUsuarios:
        if i['usuario'] == usuario and i['password'] == contraseña:
            validacion = True
            break
        elif i['usuario'] == usuario:    
            validacion= False
            falla = "contraseña"
            break
        else:
            validacion= False
            falla = "usuario"

    if validacion:
        messagebox.showinfo("Acceso",f"Validacion exitosa!!!. \n\nBienvenido  {usuario}")
        AccesoTk.withdraw()  # Ocultar el contenedor AccesoTk
        CargarMenuTk()
    elif falla == "usuario":          
        messagebox.showinfo("Acceso", f"Usuario:  {usuario}  no Valido.")
    else:
        messagebox.showinfo("Acceso", f"Contraseña no Valida.")    
# -------------------------------------------------------------------
def CargarDatosEnFormulario(fechaHora, cotizacionOficialCompra, producto, precio):
    """
    Parámetros:
        String: fechaHora
        Float: cotizacionOficialCompra
        String: producto
        Float: precio 
    Valor de retorno:
        None:  
    Notas:
        CARGA LOS DATOS procesados en el FORMULARIO. 
    Referencias: None
    """
    ListaPreciosTkFecha.config(state="normal")  # Desbloquear el ingreso de datos
    ListaPreciosTkFecha.delete(0, tk.END)  # Borrar cualquier valor previo
    ListaPreciosTkFecha.insert(tk.END, fechaHora)  # Cargar la fecha actual
    ListaPreciosTkFecha.config(state="disabled")  # Bloquear el ingreso de datos

    ListaPreciosTkCotizacion.config(state="normal")  # Desbloquear el ingreso de datos
    ListaPreciosTkCotizacion.delete(0, tk.END)  # Borrar cualquier valor previo
    ListaPreciosTkCotizacion.insert(tk.END, cotizacionOficialCompra)  # Cargar la cotización del dólar
    ListaPreciosTkCotizacion.config(state="disabled")  # Bloquear el ingreso de datos

    ListaPreciosTkMonitor1.config(state="normal")  # Desbloquear el ingreso de datos
    ListaPreciosTkMonitor1.insert(tk.END, f"{producto} {precio * cotizacionOficialCompra}")  # Cargar los valores leidos en el ciclo for
    ListaPreciosTkMonitor1.config(state="disabled")  # Bloquear el ingreso de datos
# -------------------------------------------------------------------
def AgregarRegistroHistorico(archivoHistorial, nuevoRegistroHistorico):
    """
    Parámetros:
        String: archivoHistorial
        String: nuevoRegistroHistorico
    Valor de retorno:
        None:  
    Notas:
        MUESTRA EN LISTBOX los registros del ARCHIVO 'historial_precios.csv'. 
    Referencias: None
    """
    ListaPreciosTkMonitor2.config(state="normal")  # Desbloquear el ingreso de datos
    ListaPreciosTkMonitor2.delete(0, tk.END)  # Borrar cualquier valor previo
    
    # Cerrar el archivo y volver a abrirlo en modo 'r'  (estaba en modo'a')
    archivoHistorial.close()
    archivoHistorial = open(carpetaRaizAplicacion + historialPrecioCsv, 'r')
    
    # Cargar el archivo historial_precios.csv en ListaPreciosTkMonitor2
    objetoHistorial = csv.reader(archivoHistorial)
    for fila in objetoHistorial:
        ListaPreciosTkMonitor2.insert(tk.END, ' - '.join(map(str, fila)))
    archivoHistorial.close()
    
    # Volver a abrir el archivo en modo 'a'
    archivoHistorial = open(carpetaRaizAplicacion + historialPrecioCsv, 'a', newline='')
        
    ListaPreciosTkMonitor2.config(state="disabled")  # Bloquear el ingreso de datos
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
    global mensajeError

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
            mensajeError = "Error al obtener la cotización del dólar."
    except requests.exceptions.HTTPError as errh:                           # se activa si no encuentra el URL
        mensajeError = f"No se encontró la URL {url}: {errh}."
    except requests.exceptions.ConnectionError as errc:                     # se activa si hay error de conexion
        mensajeError = f"Error de conexión al intentar acceder a la URL {url}: {errc}."
    except Exception as e:                                                  # se activa con otros tipos (distinto de los anteriores) _
                                                                                                    #_de error que pudieran ocurrir
        mensajeError = "Error al obtener la cotización del dólar."
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
        Fn que al ser invocada devuelve 2 Objetos para su proceso. 
    Referencias: None
    """ 
    
    # Abrir el producto.csv (cada fila de este ARCHIVO (objeto) es una LISTA DE VALORES)
    archivoProductos = open(carpetaRaizAplicacion + productosCsv, 'r')      # solo lectura
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
        Fn que al ser invocada devuelve 2 Objetos para su proceso. 
    Referencias: None
    """ 
    global archivoHistorial
    # Abrir el historial.csv (cada fila de este ARCHIVO (objeto) es una LISTA DE VALORES)
    archivoHistorial = open(carpetaRaizAplicacion + historialPrecioCsv, 'a', newline='') # abro modo escritura (al final) sin salto de linea
    # Crear un objeto CSV 
    objetoHistorial = csv.reader(archivoHistorial)                          # Creo un objeto de clase _csv.reader. Es iterador. _
                                                                                   # En cada iteración de 1 bucle, el objeto_
                                                                                   # objetoHistorial devuelve _
                                                                                   # la siguiente fila del archivo CSV.
#    print(objetoHistorial.__class__)                                                                        

    # archivoProductos queda abierto por necesidad (por eso no uso with que cierra automaticamente)
    # archivoProductos lo cierro en ProcesarListaPrecio                                                                              
        
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
        y muestra los resultados en Interface Grafica.
    """ 
    global fechaHora, fechaHora
    
    # Saltar la primera fila (encabezados)
    next(objetoProductos)
    # Crear una lista con fecha y hora actual
    fechaHora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nuevoRegistroHistorico = [fechaHora]
    # Acceder a los datos
    for fila in objetoProductos:
        producto=fila[0]
        precio = float(fila[1])
        CargarDatosEnFormulario(fechaHora, cotizacionOficialCompra, producto, precio)  
        nuevoRegistroHistorico.append(precio * cotizacionOficialCompra)

    # Crear un objeto writer
    writer = csv.writer(archivoHistorial)
    # Escribir el nuevo registro
    writer.writerow(nuevoRegistroHistorico)
    nuevoRegistroHistorico.append(precio * cotizacionOficialCompra)
    AgregarRegistroHistorico(archivoHistorial, nuevoRegistroHistorico)  
# -------------------------------------------------------------------
def ProcesarListaPrecios():
    """
    Parámetros:
        None: 
    Valor de retorno:
        None
    Notas:
        Fn principal que maneja el PROCESAMIENTO de DATOS.
    """
    global mensajeError
    mensajeError=""        
    #obtener Codtizacion del Dolar
    cotizacionOficialCompra = CotizacionDolarOficial()
    if cotizacionOficialCompra:
        #abrir archivo Productos.csv
        archivoProductos, objetoProductos = AbrirProductosCsv(carpetaRaizAplicacion, productosCsv)
        #abrir archivo HistorialPrecios.csv
        archivoHistorial, objetoHistorial = AbrirHistorialCsv(carpetaRaizAplicacion, historialPrecioCsv)
        #Actualizar archivo HistorialPrecio.csv
        CargarHistorialPrecio(archivoProductos, objetoProductos, archivoHistorial, objetoHistorial, cotizacionOficialCompra)
        # Cerrar el archivos abiertos
        archivoProductos.close()
        archivoHistorial.close()
    else:
        mensajeError = "No se encontró la cotización del dólar oficial."
    if mensajeError != "":
        messagebox.showinfo("Control de Datos", mensajeError)
      
# *******************************************************************
# ---------------        Funciones de ENTRY MENU      ---------------
# *******************************************************************
def ActualizarTarifas(MenuTk):
    """
    Parámetros:
        MenuTk: Objeto Class 'tkinter.Tk' 
    Valor de retorno:
        None
    Notas:
        Fn asociada a button MenuTkTarifas".
    """
    MenuTk.withdraw()  # Ocultar el contenedor AccesoTk
    CargarListaPreciosTk()
    #ProcesarListaPrecios()
# -------------------------------------------------------------------    
def ReporteEvolucionTarifas():
    """
    Parámetros:
        MenuTk: Objeto Class 'tkinter.Tk' 
    Valor de retorno:
        None
    Notas:
        Fn asociada a button MenuTkReporteTarifas".
    """
    messagebox.showinfo("Info","Reporte Evolucion Tarifas:\n\n         a DESARROLLAR.")
# -------------------------------------------------------------------   
def ReporteVentas():
    """
    Parámetros:
        MenuTk: Objeto Class 'tkinter.Tk' 
    Valor de retorno:
        None
    Notas:
        Fn asociada a button MenuTkVentas".
    """
    messagebox.showinfo("Info","Reporte de Ventas:\n\n         a DESARROLLAR.") 
# -------------------------------------------------------------------           
def CambiarContraseña():
    """
    Parámetros:
        MenuTk: Objeto Class 'tkinter.Tk' 
    Valor de retorno:
        None
    Notas:
        Fn asociada a button MenuTkContraseñas".
    """
    messagebox.showinfo("Info","Cambiar Contraseña:\n\n         a DESARROLLAR.")
# -------------------------------------------------------------------   
def PerfilUsuario():
    """
    Parámetros:
        MenuTk: Objeto Class 'tkinter.Tk' 
    Valor de retorno:
        None
    Notas:
        Fn asociada a button MenuTkPerfil".
    """
    messagebox.showinfo("Info","Perfil de Usuarios:\n\n         a DESARROLLAR.") 

# *******************************************************************
# ------------         Funciones de FORMULARIOS TK      -------------
# *******************************************************************
def CentrarFormulario(Formulario,anchoFormulario,altoFormulario):
    """
    Notas:
        Fn para CENTRAR FORMULARIO EN PANTALLA.
    """
    anchoPantalla = Formulario.winfo_screenwidth()# obtengo el ancho de pantalla
    altoPantalla = Formulario.winfo_screenheight()# obtengo el alto de pantalla
    Formulario.geometry(f"{anchoFormulario}x{altoFormulario}")# Establece el ancho y alto de la formulario
    # Calcula la posición para centrar la ventana
    x = (anchoPantalla - anchoFormulario) // 2
    y = (altoPantalla - altoFormulario) // 2
    Formulario.geometry(f"+{x}+{y}")# Establece la posición de la ventana
# ------------------------------------------------------------------- 
def CargarListaPreciosTk():
    """
    Notas:
        Fn para CREAR e INICIALIZAR formulario ListaPreciosTk.
    """
    def InicializarListaPreciosTk():
        global ListaPreciosTkFecha, ListaPreciosTkCotizacion, ListaPreciosTkMonitor1, ListaPreciosTkMonitor2
        # Centrar Formulario
        anchoFormulario = 505
        altoFormulario = 430
        CentrarFormulario(ListaPreciosTk,anchoFormulario,altoFormulario)
        
        ListaPreciosTk.resizable(False, False)                      # No permito redimensionar la ventana

        # Fila 1
        ListaPreciosTkLabel1 = tk.Label(ListaPreciosTk, text="Fecha_Hora:")
        ListaPreciosTkLabel1.grid(row=0, column=0, padx=10, pady=10)

        ListaPreciosTkFecha = tk.Entry(ListaPreciosTk, width=20)
        ListaPreciosTkFecha.grid(row=0, column=1, padx=10, pady=10)
        ListaPreciosTkFecha.config(state="disabled")  # Bloquear el ingreso de datos

        ListaPreciosTkLabel2 = tk.Label(ListaPreciosTk, text="Cotiz. Dólar Oficial:")
        ListaPreciosTkLabel2.grid(row=0, column=2, padx=10, pady=10)

        ListaPreciosTkCotizacion = tk.Entry(ListaPreciosTk, width=20)
        ListaPreciosTkCotizacion.grid(row=0, column=3, padx=10, pady=10)
        ListaPreciosTkCotizacion.config(state="disabled")  # Bloquear el ingreso de datos

        # Fila 2
        ListaPreciosTkLabel3 = tk.Label(ListaPreciosTk, text="Lista de Precio Actualizada.")
        ListaPreciosTkLabel3.grid(row=1, column=0, columnspan=8, padx=10, pady=0)

        # Fila 3
        ListaPreciosTkMonitor1 = tk.Listbox(ListaPreciosTk, width=60)
        ListaPreciosTkMonitor1.grid(row=2, column=0, columnspan=8, padx=10, pady=0)
        ListaPreciosTkMonitor1.config(state="disabled")  # Bloquftrear el ingreso de datos

        # Fila 4
        ListaPreciosTkLabel4 = tk.Label(ListaPreciosTk, text="Historico de Precios")
        ListaPreciosTkLabel4.grid(row=3, column=0, columnspan=8, padx=10, pady=0)

        # Fila 5
        ListaPreciosTkMonitor2 = tk.Listbox(ListaPreciosTk, width=75)
        ListaPreciosTkMonitor2.grid(row=4, column=0, columnspan=8, padx=10, pady=0)
        ListaPreciosTkMonitor2.config(state="disabled")  # Bloquear el ingreso de datos
    #-----------------------------
    ListaPreciosTk = tk.Tk()
    ListaPreciosTk.title("Lista de Precios")
    # Ordeno el evento de cierre hecho al hacer click en cerrar ventana con el mouse
    def on_closing():                                
        ListaPreciosTk.destroy()                            # desturyo MenuTk
        sys.exit()                                  # cerrar el programa
   
    ListaPreciosTk.protocol("WM_DELETE_WINDOW", on_closing) #Asociar la fn on_closing con el evento de cierre de la ventana MenuTk
    
    ListaPreciosTk.after(0, InicializarListaPreciosTk())
    
    ProcesarListaPrecios()
    
    ListaPreciosTk.mainloop()
   
# ------------------------------------------------------------------- 
def CargarMenuTk():
    """
    Notas:
        Fn para CREAR e INICIALIZAR formulario MenuTk.
    """
    def InicializarMenuTk():
        # Centrar Formulario
        anchoFormulario = 280
        altoFormulario = 230
        CentrarFormulario(MenuTk,anchoFormulario,altoFormulario)
    
        MenuTk.resizable(False, False)                      # No permito redimensionar la ventana
        
        # Configurar las filas y columnas de la ventana para que se expandan horizontal y verticalmente
        MenuTk.grid_columnconfigure(0, weight=1)
        MenuTk.grid_rowconfigure(0, weight=1)
        MenuTk.grid_rowconfigure(1, weight=1)
        MenuTk.grid_rowconfigure(2, weight=1)
        MenuTk.grid_rowconfigure(3, weight=1)
        MenuTk.grid_rowconfigure(4, weight=1)

        # Creo los Botones y los coloco. Utilizo el método grid, con el parámetro sticky="nsew" \
        # para que se centren horizontal y verticalmente en la ventana.
        
        MenuTkTarifas = tk.Button(MenuTk, text="Actualizar Tarifas", command=lambda:ActualizarTarifas(MenuTk))  # OJAZO: si no uso Lambda se ejecutara_
                                                                                                                # sin esperar al click del boton
        MenuTkTarifas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        MenuTkReporteTarifas = tk.Button(MenuTk, text="Reporte: Evolucion de Tarifas", command=ReporteEvolucionTarifas)
        MenuTkReporteTarifas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        MenuTkReporteVentas = tk.Button(MenuTk, text="Reporte: Ventas", command=ReporteVentas)
        MenuTkReporteVentas.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        MenuTkContraseñas = tk.Button(MenuTk, text="Cambiar Contraseñas", command=CambiarContraseña)
        MenuTkContraseñas.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        MenuTkPerfil = tk.Button(MenuTk, text="Perfil de Usuarios", command=PerfilUsuario)
        MenuTkPerfil.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
    #-----------------------------
    MenuTk = tk.Tk()
    MenuTk.title("Menú Principal")

    # Ordeno el evento de cierre hecho al hacer click en cerrar ventana con el mouse
    def on_closing():                                
        MenuTk.destroy()                            # desturyo MenuTk
        sys.exit()                                  # cerrar el programa
    MenuTk.protocol("WM_DELETE_WINDOW", on_closing) #Asociar la fn on_closing con el evento de cierre de la ventana MenuTk

    MenuTk.after(0, InicializarMenuTk())
    MenuTk.mainloop()    
# ------------------------------------------------------------------- 
def InicializarAccesoTk():
    """
    Notas:
        Fn para CREAR e INICIALIZAR formulario AccesoTk.
    """
    global usuariosJson, productosCsv, historialPrecioCsv, carpetaRaizAplicacion, \
           AccesoTkUsuario, AccesoTkContraseña
    
    def focus_AccesoContraseña(event):
        AccesoTkContraseña.focus_set()            # Mando el foco a AccesoContraseña

    def focus_AccesoAceptar(event):
        AccesoTkAceptar.focus_set()               # Mando el foco a AccesoAceptar

    # Verificar existencia de archivos (la carpeta y los 3 archivos deben existir, sino paro)
    VerificarExistenciaArchivo(carpetaRaizAplicacion, usuariosJson)
    VerificarExistenciaArchivo(carpetaRaizAplicacion, productosCsv)
    VerificarExistenciaArchivo(carpetaRaizAplicacion, historialPrecioCsv)

    # Centrar Formulario
    anchoFormulario = 280
    altoFormulario = 120
    CentrarFormulario(AccesoTk,anchoFormulario,altoFormulario)

    # Crear el campo de texto para el usuario
    AccesoTkRotuloUsuario = tk.Label(AccesoTk, text="Usuario:")
    AccesoTkRotuloUsuario.grid(row=0, column=3, padx=5, pady=5)
    AccesoTkUsuario = tk.Entry(AccesoTk)
    AccesoTkUsuario.grid(row=0, column=4, padx=5, pady=5)
    AccesoTkUsuario.bind("<Return>", focus_AccesoContraseña)          # Evento Enter: dispara fn focus_AccesoContraseña

    # Crear el campo de texto para la contraseña
    AccesoTkRotuloContraseña = tk.Label(AccesoTk, text="Contraseña:")
    AccesoTkRotuloContraseña.grid(row=1, column=3, padx=5, pady=5)
    AccesoTkContraseña = tk.Entry(AccesoTk, show="*")                 # Show reeempla caracter tipeado por "*"  
    AccesoTkContraseña.grid(row=1, column=4, padx=5, pady=5)
    AccesoTkContraseña.bind("<Return>", focus_AccesoAceptar)          # Evento Enter: dispara fn focus_AccesoAceptar
   
    # Crear el botón para aceptar
    AccesoTkAceptar = tk.Button(AccesoTk, text="Aceptar", command=ValidarUsuario)   # command define la Fn que se ejecuta al hacer click en Aceptar
    AccesoTkAceptar.grid(row=2, column=4, columnspan=2, padx=5, pady=5)

# *******************************************************************
# ----------------          CUERPO PRINCIPAL        -----------------
# *******************************************************************
usuariosJson = "auth_usuarios.json"
productosCsv = "productos.csv"
historialPrecioCsv = "historial_precios.csv"
carpetaRaizAplicacion=DeterminarRutaAcceso()
# creo AccesoTk
AccesoTk = tk.Tk()
AccesoTk.title("Proyecto Integrador")
AccesoTk.after(0, InicializarAccesoTk())                    # Metodo after ejecutar una funcion ANTES de mostrar AccesoTk \ 
                                                                        # (inicializo en esta funcion)
AccesoTk.mainloop()                                         # Muestro AccesoTk

    
        
       




