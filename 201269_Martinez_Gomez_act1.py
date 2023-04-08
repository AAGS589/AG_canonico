import random
from random import sample
import math
import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib import pyplot
from tkinter import *
from tkinter import ttk


ventana = Tk()
ventana.title('Algoritmo genetico canonico')
ventana.geometry('380x400')
ventana.config(bg='white')

etiqueta = Label(ventana, text="Intervalo", font=12, bg="white").place(x=10, y=20)
etiqueta1 = Label(ventana, text="Xmin         Xmax", font=5, bg="white").place(x=80, y=42)
intervalo1 = ttk.Entry(ventana, font=14)
intervalo1.place(x=80, y=20, width=50, height=30)
intervalo1.insert(0,12)
intervalo2 = ttk.Entry(ventana, font=14)
intervalo2.place(x=150, y=20, width=50, height=30)
intervalo2.insert(0,22)

etiqueta2 = Label(ventana, text="Numero de generaciones", font=12, bg="white").place(x=10, y=60)
num_generaciones_txt = ttk.Entry(ventana, font=14)
num_generaciones_txt.place(x=200, y=60, width=50, height=30)
num_generaciones_txt.insert(0,5)

etiqueta3 = Label(ventana, text="Poblacion Inicial", font=12, bg="white").place(x=10, y=100)
poblacion_inicial_txt = ttk.Entry(ventana, font=14)
poblacion_inicial_txt.place(x=140, y=100, width=50, height=30)
poblacion_inicial_txt.insert(0,3)

etiqueta4 = Label(ventana, text="Precision", font=12, bg="white").place(x=10, y=140)
precision_txt = ttk.Entry(ventana, font=14)
precision_txt.place(x=140, y=140, width=50, height=30)
precision_txt.insert(0,0.30)

etiqueta5 = Label(ventana, text="Probabilidad de cruza", font=12, bg="white").place(x=10, y=180)
probabilidad_cruza_txt = ttk.Entry(ventana, font=14)
probabilidad_cruza_txt.place(x=180, y=180, width=50, height=30)
probabilidad_cruza_txt.insert(0,0.60)


etiqueta6 = Label(ventana, text="Probabilidad de mutacion Individuo", font=12, bg="white").place(x=10, y=220)
probabilidad_mutacion_individuo_txt = ttk.Entry(ventana, font=14)
probabilidad_mutacion_individuo_txt.place(x=280, y=220, width=50, height=30)
probabilidad_mutacion_individuo_txt.insert(0,0.25)


etiqueta7 = Label(ventana, text="Probabilidad de mutacion Gen", font=12, bg="white").place(x=10, y=260)
probabilidad_mutacion_gen_txt = ttk.Entry(ventana, font=14)
probabilidad_mutacion_gen_txt.place(x=280, y=260, width=50, height=30)
probabilidad_mutacion_gen_txt.insert(0,0.40)

etiqueta8 = Label(ventana, text="Poblacion maxima", font=12, bg="white").place(x=10, y=300)
poblacion_maxima_txt = ttk.Entry(ventana, font=14)
poblacion_maxima_txt.place(x=280, y=300, width=50, height=30)
poblacion_maxima_txt.insert(0,5)



generaciones = []
mejor_x_generacion = []
generacion = 0
poblacion = []
poblacion_generacion = []
id_individuo=0

"""Para empezar"""
intervalo = []
num_generaciones = 0
poblacion_inicial = 0
precision_deta_dex = 0.00
"""Generar individuos"""
num_bits = 0
rango= 0
individuos = []
"""Cruza"""
parejas = []
probabilidad_de_cruza = 0.00
hijos = []

"""Mutacion"""
seleccion_hijos = []
indice_hijos_seleccionados = []
probabilidad_mutacion_individuo = 0.00
probabilidad_mutacion_gen = 0.00
"""Poda"""
poblacion_maxima = 0




def cantidadDeBits():
    global rango
    rango = intervalo[1] - intervalo[0]
    num_puntos = int(rango/precision_deta_dex + 1)
    potencia = 0
    puntos = 0
    while puntos<num_puntos:
        potencia = potencia + 1
        puntos = pow(2,potencia)
    global num_bits
    num_bits = potencia
    #print("cantidad de puntos", num_puntos)
    #print("cantidad de bits", potencia)
def generarIndiviuos():
    global id_individuo
    #print("EL RANGO ES", rango)
    individuos_en_entero = sample([x for x in range(1,rango+1)],poblacion_inicial)
    for def_individuo in range(poblacion_inicial):
       id_individuo = id_individuo + 1
       individuo_en_entero = individuos_en_entero[def_individuo]
       individuo_en_bin = format(individuo_en_entero,"b")
       individuos.append(individuo_en_bin)
       while len(individuos[def_individuo])<num_bits:
             individuos[def_individuo] = "0"+ individuos[def_individuo]
       insertar_individuos_a_poblacion(def_individuo+1,individuos_en_entero[def_individuo],individuos[def_individuo])

    #print("POBLACION INICIAL: ",poblacion)
   

def generarParejas():
    for i in range(0, len(poblacion)-1):
        
        for j in range(i, len(poblacion)-1):
            individuo = poblacion[i]
            individuo_skip = poblacion[j+1]
            parejas.append([[individuo[3]],[individuo_skip[3]]])
    #print("PAREJAS GENERADAS: ",parejas)

def seleccionar_parejas():
    probabilidades_aletorio = []

    for i in range(len(parejas)):
        aleatorio_decimal = random.uniform(0.01, 1.0)
        aleatorio_decimal_redondeado = round(aleatorio_decimal, 2)
        probabilidades_aletorio.append(aleatorio_decimal_redondeado)

    posicion=0
    while posicion<len(parejas):
       if probabilidades_aletorio[posicion]>probabilidad_de_cruza:
          parejas.pop(posicion)
       else:
          posicion=posicion+1

    
    #print("PAREJAS SELECCIONADAS: ",parejas)
    
def insertar_individuos_a_poblacion(numero_individuo, numero_asignado, numero_en_binario):
    poblacion.append(["Individuo ",numero_individuo,numero_asignado,numero_en_binario, calcular_x(numero_asignado), calcular_aptitud(calcular_x(numero_asignado))])
    
def calcular_x(numero_rand_asignado):
    x = intervalo[0] + numero_rand_asignado * precision_deta_dex   
    return x

def calcular_aptitud(x):
    fx= 1-(x-0.5)**2/(1.5)**2+(x-1)**3/(1.6)**2
    return fx
def cruza():
    global parejas, hijos, num_bits, id_individuo
    punto_cruza = int(num_bits/2)

    for p in parejas:
      id_individuo = id_individuo + 1 
      pareja = p
      individuo_pareja = pareja[0]
      individuo_parejaa = individuo_pareja[0]
      individuo_pareja2 =pareja[1]
      individuo_parejaa2 = individuo_pareja2[0]
      hijos.append(["Individuo",id_individuo,binario_a_decimal(individuo_parejaa[:punto_cruza]+individuo_parejaa2[punto_cruza:]), individuo_parejaa[:punto_cruza]+individuo_parejaa2[punto_cruza:]])
      
      id_individuo = id_individuo + 1 
      hijos.append(["Individuo",id_individuo,binario_a_decimal(individuo_parejaa2[:punto_cruza]+individuo_parejaa[punto_cruza:]), individuo_parejaa2[:punto_cruza]+individuo_parejaa[punto_cruza:]])
    
    #print("HIJOS: ",hijos)
    
def verificar_hijos():
    hijos_aceptados = []
    for h in hijos:
        hijo =h
        num_entero = hijo[2]
        if num_entero > 0 and calcular_x(num_entero)>=intervalo[0] and calcular_x(num_entero)<=intervalo[1] :
           hijos_aceptados.append(hijo) 
    hijos.clear()

    for i in hijos_aceptados:
        hijos.append(i)
        hijo = i
        num_individuo = hijo[1]
        num_entero = hijo[2]
        num_binario = hijo[3]
        insertar_individuos_a_poblacion(num_individuo, num_entero, num_binario)

    #print("HIJOS DESPUES DE LA VERIFICACION:", hijos) 
    
def binario_a_decimal(numero_binario):
	numero_decimal = 0 

	for posicion, digito_string in enumerate(numero_binario[::-1]):
		numero_decimal += int(digito_string) * 2 ** posicion

	return numero_decimal
def seleccion_hijos_mutacion():
    global  seleccion_hijos, indice_hijos_seleccionados
    probabilidades_aletorio = []
    
    for i in range(len(hijos)):
        aleatorio_decimal = random.uniform(0.01, 1.0)
        aleatorio_decimal_redondeado = round(aleatorio_decimal, 2)
        probabilidades_aletorio.append(aleatorio_decimal_redondeado)

    
    posicion=0
    while posicion<len(hijos):
        if probabilidades_aletorio[posicion]<probabilidad_mutacion_individuo:
           seleccion_hijos.append(hijos[posicion])   
           indice_hijos_seleccionados.append(posicion)
           hijos.pop(posicion)
        else:
           posicion=posicion+1
    
    #print("HIJOS SELECCIONADAS",seleccion_hijos)
    

def mutacion():
    probabilidades_aletorio = []
    global seleccion_hijos,hijos
    cont = 0
    for h in seleccion_hijos:
        probabilidades_aletorio.clear()
        hijo =h
        parte_hijo = hijo[3]
        parte_hijoo = parte_hijo
        for i in range(len(parte_hijoo)):
           aleatorio_decimal = random.uniform(0.01, 1.0)
           aleatorio_decimal_redondeado = round(aleatorio_decimal, 2)
           probabilidades_aletorio.append(aleatorio_decimal_redondeado)
    
        for j in range(len(parte_hijoo)):
            if probabilidades_aletorio[j]<probabilidad_mutacion_gen:
               if parte_hijoo[j] =="0":
                  l = list(parte_hijoo)
                  l[j] = '1'
                  parte_hijoo = "".join(l)
               else:
                  l = list(parte_hijoo)
                  l[j] = '0'
                  parte_hijoo = "".join(l)
         
        hijo.pop()
        hijo.pop(2)
        hijo.append(parte_hijoo)
        hijo.insert(2,binario_a_decimal(parte_hijoo))

        hijos.insert(indice_hijos_seleccionados[cont],hijo)
        cont = cont + 1

    #print("HIJOS DESPUES DE LA MUTACION: ", hijos)    
    verificar_hijos()   


def poda():
    global poblacion_generacion, generacion, mejor_x_generacion
    poblacion_generacion = sorted( poblacion, key=lambda aptitud : aptitud[5], reverse=True) 
    #print(poblacion_generacion)
    while len(poblacion_generacion)>poblacion_maxima:
         poblacion_generacion.pop() 
    #print("POBLACION DE LA GENERACION",poblacion_generacion) 
    poblacion.clear()
    for po in poblacion_generacion:
        poblacion.append(po)
    
    
    generacion = generacion +1
    generaciones.append(generacion)
    mejor_individuo = poblacion[0]
    aptitud_mejor_individuo = mejor_individuo[5]
    mejor_x_generacion.append(aptitud_mejor_individuo)
    
    poblacion_generacion.clear()  
def limpiar():
    global individuos, parejas, hijos, seleccion_hijos, indice_hijos_seleccionados
    individuos.clear()
    parejas.clear()
    hijos.clear()
    seleccion_hijos.clear()
    indice_hijos_seleccionados.clear()
def graficar():
    #print("POBLACIONA A GRAFICAR", poblacion)
    #print("Mejores de cada Generacion", mejor_x_generacion)
    mejor_indiviuo= poblacion[0]
    print("EL MEJOR INDIVIDUO FUE: ", mejor_indiviuo[0], mejor_indiviuo[1],"CON APTITUD DE :",mejor_indiviuo[5])
    label_mejor_individuo = "EL MEJOR INDIVIDUO FUE: " + str(mejor_indiviuo[0]) + str(mejor_indiviuo[1]) + "CON APTITUD DE :" + str(mejor_indiviuo[5])
    fig, ax = plt.subplots()
    ax.plot(generaciones, mejor_x_generacion, label = 'Mejores', linestyle = 'dotted', color = 'tab:blue',  marker = 'o')
    ax.set_xlabel("Generaciones", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:red'})
    ax.set_ylabel("Aptitud", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:green'})
    ax.set_title('Mejores aptitudes %s' %label_mejor_individuo , loc = "left", fontdict = {'fontsize':12, 'fontweight':'bold'})
    ax.legend(loc = 'upper left')
    ax.set_xlim([1,len(generaciones)])
    ax.set_xticks(range(1, len(generaciones)+1))
    plt.show()

def grafica_individuos():
        global intervalo, poblacion
        x = []
        y = []
        for p in poblacion:
            y.append(p[5])
            x.append(p[4])

        pyplot.scatter(x,y)
        pyplot.xlim(intervalo[0],intervalo[1])
        pyplot.xlabel("X", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:red'})
        pyplot.ylabel("Y", fontdict = {'fontsize':12, 'fontweight':'bold', 'color':'tab:green'})
        pyplot.title(f"Generacion {generacion}")
        pyplot.savefig(f"img/i{generacion}.png")
        pyplot.close()
        pass

def limpiar_poblacion():
    global poblacion, generaciones, mejor_x_generacion, intervalo
    poblacion.clear()
    generaciones.clear()
    mejor_x_generacion.clear()
    intervalo.clear()

    
def iniciar_poblacion():
   limpiar_poblacion()
   global intervalo, num_generaciones, poblacion_inicial, precision_deta_dex, probabilidad_de_cruza, probabilidad_mutacion_individuo, probabilidad_mutacion_gen, poblacion_maxima
   intervalo.append(int(intervalo1.get()))
   intervalo.append(int(intervalo2.get()))
   num_generaciones = int(num_generaciones_txt.get())
   poblacion_inicial = int(poblacion_inicial_txt.get())
   precision_deta_dex = float(precision_txt.get())
   probabilidad_de_cruza = float(probabilidad_cruza_txt.get())
   probabilidad_mutacion_individuo = float(probabilidad_mutacion_individuo_txt.get())
   probabilidad_mutacion_gen = float(probabilidad_mutacion_gen_txt.get())
   poblacion_maxima = int(poblacion_maxima_txt.get())

   cantidadDeBits()
   generarIndiviuos()
   
   for i in range(num_generaciones):
      generarParejas()
      seleccionar_parejas()
      cruza()
      seleccion_hijos_mutacion()
      mutacion()
      poda()
      grafica_individuos()
      #print("POBLACION DE LA GENERACION",poblacion)
      limpiar() 
   
   graficar()
   
Button(text="Maximizar", bg="#9D2449", fg="#fff",  command=iniciar_poblacion, font=12).place(x=120, y=340, width=120, height=30)

ventana.mainloop()




   