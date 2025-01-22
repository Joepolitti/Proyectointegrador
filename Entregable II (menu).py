import os
import subprocess
import Baul
# *******************************************************************
# ------------            Area  de  Funciones          --------------
# *******************************************************************
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
        print(f"\nEl archivo --> \033[95m{ruta}\033[0m\033[92m{archivo}\033[0m \n\033[91mNO EXISTE EN ESTE DIRECTORIO.\033[0m\n")
        print(f"\033[93mError en tiempo de ejecucion!!!. \nVerifique existencia del archivo REQUERIDO.\033[0m\n")
        exit() 
# -------------------------------------------------------------------
def Modo_1():
    """
    Parámetros:
        parametros: None
    Valor de retorno:
        None:  
    Notas:
        Fn que al ser invocada EJECUTA la APP en modo CONSOLA. 
    Referencias: None
    """
    carpetaRaizAplicacion = DeterminarRutaAcceso()
    archivo="Modo Consola.py"
    ruta = carpetaRaizAplicacion + archivo
    VerificarExistenciaArchivo(carpetaRaizAplicacion,archivo)
    
    subprocess.run(["python", ruta])
# -------------------------------------------------------------------
def Modo_2():
    """
    Parámetros:
        parametros: None
    Valor de retorno:
        None:  
    Notas:
        Fn que al ser invocada EJECUTA la APP en modo INTERFACE GRAFICA. 
    Referencias: None
    """
    carpetaRaizAplicacion = DeterminarRutaAcceso()
    archivo="Modo Interface Grafica.py"
    ruta = carpetaRaizAplicacion + archivo
    VerificarExistenciaArchivo(carpetaRaizAplicacion,archivo)
    
    subprocess.run(["python", ruta])
# *******************************************************************
# ------------             CUERPO PRINCIPAL            --------------
# *******************************************************************
Baul.LimpiarPantalla()

listaArchivos = ("Entregable II (menu).py", "Modo Interface Grafica.py", "Modo Consola.py",
                "Baul.py", "auth_usuarios.json", "productos.csv", "historial_precios.csv")

print("-"*140)
print("Observacion:El programa fue desarrollado en base a \033[94mUN MENU GENERADO automaticamente(en CONSOLA)\033[0m en UN DICCIONARIO y combinado con una TUPLA.")
print("            Cada \033[92mOPCION del menu EJECUTA el PROGRAMA en el MODO requerido\033[0m (Modo: CONSOLA ó Modo: INTERFACE GRAFICA).")
print("            Para optimizar la presentacion en pantalla, \033[95mla TERMINAL de VSC debe estar en MODO PANTALLA COMPLETA\033[0m.") 
print("-"*140)

Baul.Pausa()

i=0
for valor in listaArchivos:
    if i==0:
        print(f"               Archivos Necesarios: \033[92m{valor}\033[0m")
    else:       
        print(f"                                    \033[92m{valor}\033[0m")
    i+=1    

print("\n                     Deben estar \033[4m\033[95mEN LA MISMA CARPETA\033[0m")
print("\nNota: El sistema chequea \033[92mla existencia de estos archivos (y su ubicacion) antes de lanzar los procesos\033[0m")
Baul.Pausa()

interfaceGrafica = {}   #diccionario del practico (almaceno como llave la opcion del menu y como valor el nombre de la _ \
                                # funcion asociada a un determinado MODO de ejecucion)

titulos = ("Ejecutar app EN CONSOLA.", # titulos es una tupla que almacena una breve reseña de lo que hace un ejercicio
           "Ejecutar app EN INTERFACE GRAFICA (tkinter).",
            )

cant_modo=len(titulos)     #definir cuanto ITEM  tiene el MENU

cartel="\033[94m   M E N U    P R I N C I P A L   \033[0m"
largo_cartel=130     #cantidad de caracteres del cartel 

menu=""              #para forzar el primer ingreso al while
while menu!="0":     #while que controla el MENU
    Baul.LimpiarPantalla()
    print("\n\n" + "*" * (largo_cartel-9))
    print(cartel.center(largo_cartel,"*"))    #muestro cartel MENU PRINCIPAL (convertido en str de 130 caracteres centrado y autorrelenado con *) 
    print("*" * (largo_cartel-9) + "\n\n")

    #lleno mi diccionario en base al MODO de EJECUCION  de la APP y a la vez voy mostrando en pantalla el menu del programa 
    for i in range(1,cant_modo+1,1):
        llave=str(i)                               #utilizo de key un string solo porque el while esta armado para que _ 
                                                                #controle string y olvidarme del control de dato numerico.
        interfaceGrafica[llave]='Modo_' + llave
        print(f"\033[95m{llave}\033[0m >>> {interfaceGrafica[llave]} :  \033[95m{titulos[i-1]}\033[0m")

    print("\n\033[95m0\033[0m >>> \033[95mTerminar\033[0m")    #imprimo la llave para salir del programa
    
    menu=input("\n\n         Elija una Opcion: ")  #por defecto lo ingresa como string para olvidarme del control de datos numerico y rango
    
    Baul.LimpiarPantalla()
    
    #ejecuto la opcion indicada
    if menu!="0":
        modo=interfaceGrafica.get(menu,None) #busco el valor de la opcion ingresada pero con el cuidado de que me _
                                                        # devuelva None en caso de no encontrar la key en el diccionario
        if modo:
            exec(modo + "()")       # ejecuta el codigo de la funcion indicado por la cadena de texto _
                                                # (Python no reconoce STR como instruccion o invocacion a funcion, por eso uso la instruccion EXEC)

             