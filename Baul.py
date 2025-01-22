import platform                                #con esta libreria puedo a traves del metodo system saber que sistema operativo estoy usando
import os                                      #para determinar que Sistema Operativo estoy usando
import time                                    #para fijar un retardo de tanto segundos
import msvcrt                                   #para ingresar un caracter por teclado sin eco en pantalla y sin enter (el viejo keypress)
#------------------------------------------------------------------------------------------------------------------------
def LimpiarPantalla():
    """
        LIMPIA la consola (funciona solo para WIN o LINUX)
    Parámetros:
        parametros: SIN PARAMETROS REQUERIDOS
    Valor de retorno:
        tipo: NINGUNO. 
    Notas:
        Fn que LIMPIA la pantalla al ser invocada. 
    Referencias:
        FUNCION de mi libreria BAUL
    """
    time.sleep(0.05)                        #delay en segundos
    if platform.system()=="Windows":     #platform.system() devuelve el Sistema Operativo sobre el cual esta corriendo Python
        os.system('cls')                 #para windows limpia pantalla
    else:
        os.system('clear')                      #para linux limpia pantalla
    
    return
#------------------------------------------------------------------------------------------------------------------------
def Pausa():
    """
        Genera una PAUSA en la ejecucion del programa hasta que se presiona cualquier tecla
    Parámetros:
        parametros: SIN PARAMETROS REQUERIDOS
    Valor de retorno:
        tipo: NINGUNO. 
    Notas:
        Fn PAUSA la ejecucion del PROGRAMA 
    Referencias:
        FUNCION de mi libreria BAUL
    """
    print("\n\033[93m                                  Presione una tecla para continuar...\033[0m")
    n=msvcrt.getch()     #lee 1 tecla del buffer y lo borra directamente
    time.sleep(0.1)
    
    return
#------------------------------------------------------------------------------------------------------------------------
def Reintentar(reintentar):
    """
        Reintentar?
    Parámetros:
        parametros: Tipo BOOLEAN
    Valor de retorno:
        tipo: Tipo BOOLEAN 
    Notas:
        Fn que al ser invocada DA LA POSIBILIDAD al usuario de REINTENTAR o VOLVER AL MENU. 
    Referencias:
        FUNCION de mi libreria BAUL
    """
    print("\033[93m\n\nReintentar   ( y / n )  ??? \n\n\033[0m")
    tecla = None                                  # vacio para forzar el primer ingreso al while
    while tecla!='y' or tecla!='n' or tecla!='Y' or tecla!='N':
        tecla = msvcrt.getwch()                   #lee 1 tecla del buffer de teclado SIN MOSTRARLO en pantala y sin esperar INTRO
        if tecla=='y' or tecla=='Y':
            reintentar=True
            break
        elif tecla=='n' or tecla=='N':
            reintentar=False
            break
    
    return reintentar    
#------------------------------------------------------------------------------------------------------------------------
def ValidarReal(num,mensaje="Ingrese un NUMERO REAL"):  #valida el ingreso de un numero, donde NUM es el numero a evaluar y MENSAJE es el mostrador en el input previo a la invocacion de la funcion
    """
        CONVIERTE dato ingresado por parametro en NUMERO REAL
    Parámetros:
        parametros1: Valor a ser convertirdo
        parametros2: String correspondiente al mensaje de reintento
    Valor de retorno:
        tipo: VALOR DEL TIPO FLOAT. 
    Notas:
        Fn que al ser invocada ITERA hasta que se ingresa un valor numerico el cual ES CONVERTIDO EN REAL . 
    Referencias:
        FUNCION de mi libreria BAUL
    """
    invalido=True               #asumo por defecto que el dato ingresado no es valido
    primeravez=True             #para controlar que la primera vez trate de validar el valor que ingreso como parametro de la funcion sino va a tratar de validar el input del except
    while invalido:
        try:
            if primeravez:
                num=float(num)
            else:
                num=float(input(mensaje))
            invalido=False
            return num
        except:
            primeravez=False
            print("\n            ERROR: \033[93mEl valor ingresado NO ES NUMERO REAL. Intente nuevamente.\n\033[0m")
     
    return        
#------------------------------------------------------------------------------------------------------------------------
def ValidarEntero(num,mensaje="Ingrese un NUMERO ENTERO"):  #valida el ingreso de un numero, donde NUM es el numero a evaluar y MENSAJE es el mostrador en el input previo a la invocacion de la funcion
    """
        CONVIERTE dato ingresado por parametro en NUMERO ENTERO
    Parámetros:
        parametros1: Valor a ser convertirdo
        parametros2: String correspondiente al mensaje del input
    Valor de retorno:
        tipo: VALOR DEL TIPO INT. 
    Notas:
        Fn que al ser invocada ITERA hasta que se ingresa un valor numerico el cual ES CONVERTIDO EN ENTERO . 
    Referencias:
        FUNCION de mi libreria BAUL
    """
    invalido=True         #asumo por defecto que el dato ingresado no es valido
    primeravez=True       #para controlar que la primera vez trate de validar el valor que ingreso como parametro de la funcion sino va a tratar de validar el input del except        
    while invalido:    
        try:
            if primeravez:
                num=int(num)
            else:
                num=int(input(mensaje))
            invalido=False
            return num
        except:
            primeravez=False
            print("\n            ERROR: \033[93mEl valor ingresado NO ES NUMERO ENTERO. Intente nuevamente.\n\033[0m")

    return
#------------------------------------------------------------------------------------------------------------------------
def Repetir(repetirEjercicio):
    """
        REPETIR el ejercicio?
    Parámetros:
        parametros: Tipo BOOLEAN
    Valor de retorno:
        tipo: Tipo BOOLEAN 
    Notas:
        Fn que al ser invocada DA LA POSIBILIDAD al usuario de repetir el ejercicio o VOLVER AL MENU. 
    Referencias:
        FUNCION de mi libreria BAUL
    """
#    global repetirEjercicio
    print("\n\n\n\033[93mDesea repetir EL EJERCICIO   ( y / n )  ??? \033[0m")
    tecla = None                                  # vacio para forzar el primer ingreso al while
    while tecla!='y' or tecla!='n' or tecla!='Y' or tecla!='N':
        tecla = msvcrt.getwch()                   #lee 1 tecla del buffer de teclado SIN MOSTRARLO en pantala y sin esperar INTRO
        if tecla=='y' or tecla=='Y':
            repetirEjercicio=True
            break
        elif tecla=='n' or tecla=='N':
            repetirEjercicio=False
            break
    return repetirEjercicio  