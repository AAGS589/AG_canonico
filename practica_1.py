import random
from random import sample
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib import pyplot
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QRadioButton, QPushButton


class AG(QMainWindow):


    def __init__(self):
        super().__init__()
        uic.loadUi("estilos.ui",self)
        self.inicioIntervalo.setText ("5")
        self.finalIntervalo.setText("15")
        self.pob_inicial.setText("10")
        self.pob_maxima.setText("50")
        self.num_generaciones.setText("100")
        self.presicion_input.setText("0.01")
        self.prob_cruza.setText("0.8")
        self.prob_mutacion_individuo.setText("0.1")
        self.prob_mutacion_gen.setText("0.1")
        #Checkboxes
        self.radio_maximizar = self.findChild(QRadioButton, 'radio_maximizar')
        self.radio_minimizar = self.findChild(QRadioButton, 'radio_minimizar')

        #Botones
        self.btn_iniciarAlgoritmo.clicked.connect(self.iniciarAlgoritmo)
        self.btn_graficar_funcion.clicked.connect(self.graficarFuncion)
        self.btn_graficar_aptitud.clicked.connect(self.GraficarAptitud)
        
        
        self.individuos = []
        self.poblacion = []
        self.id_individuo = 0
        self.generacion = 0
        self.generaciones = []
        self.mejor_x_generacion = []
        self.aptitudes = []
        inicio_intervalo = float(self.inicioIntervalo.text())
        final_intervalo = float(self.finalIntervalo.text())
        self.intervalo = (inicio_intervalo, final_intervalo)
        

    def iniciarAlgoritmo(self):
        self.limpiarDatos()
        inicio_intervalo = float(self.inicioIntervalo.text())
        final_intervalo = float(self.finalIntervalo.text())
        pob_inicial = int(self.pob_inicial.text())
        pob_maxima = int(self.pob_maxima.text())
        num_generaciones = int(self.num_generaciones.text())
        presicion_input = float(self.presicion_input.text())
        prob_cruza = float(self.prob_cruza.text())
        prob_mutacion_individuo = float(self.prob_mutacion_individuo.text())
        prob_mutacion_gen = float(self.prob_mutacion_gen.text())

        num_bits = self.cantidadDeBits(inicio_intervalo, final_intervalo, presicion_input)

        self.generarPoblacionInicial(2 ** num_bits - 1, pob_inicial, num_bits)
        minimizar = self.radio_minimizar.isChecked()
        
        self.mejor_x_generacion = []
        self.generaciones = []
        self.generacion = 0

        for _ in range(num_generaciones):
            parejas = self.seleccionarParejasCruza(prob_cruza)

            hijos = self.realizarCruza(parejas, num_bits)

            self.verificarHijos(hijos, (inicio_intervalo, final_intervalo), presicion_input)
            hijos_mutantes = self.seleccionHijosMutacion(prob_mutacion_individuo)

            self.mutacionHijos(prob_mutacion_gen, inicio_intervalo, final_intervalo, presicion_input)

            self.podaPoblacion(pob_maxima, inicio_intervalo, presicion_input, minimizar)

            mejor_individuo = self.poblacion[0]

            x_mejor = self.calcularValorX(mejor_individuo['entero'], inicio_intervalo, presicion_input)
            self.mejor_x_generacion.append(x_mejor)
            self.generaciones.append(self.generacion)
            self.generacion += 1

        mejor_individuo = self.poblacion[0]
        x_mejor = self.calcularValorX(mejor_individuo['entero'], inicio_intervalo, presicion_input)
        aptitud_mejor = self.calcularAptitud(x_mejor)

        print(f"Mejor individuo: {mejor_individuo}")
        print(f"Mejor x: {x_mejor}")
        print(f"Mejor aptitud: {aptitud_mejor}")

    def cantidadDeBits(self, inicio_intervalo, final_intervalo, presicion_input):
        rango = final_intervalo - inicio_intervalo
        num_valores = rango * (10 ** presicion_input)
        num_bits = math.ceil(math.log2(num_valores))
        print("Cantidad de bits necesarios:", num_bits)
        return num_bits

    def generarPoblacionInicial(self, rango, pob_inicial, num_bits):
        individuos_en_entero = sample([x for x in range(1, rango + 1)], pob_inicial)
        for def_individuo in range(pob_inicial):
            self.id_individuo = self.id_individuo + 1
            individuo_en_entero = individuos_en_entero[def_individuo]
            individuo_en_bin = format(individuo_en_entero, "b")
            self.individuos.append(individuo_en_bin)
            while len(self.individuos[def_individuo]) < num_bits:
                self.individuos[def_individuo] = "0" + self.individuos[def_individuo]
            self.insertar_individuos_a_poblacion(self.id_individuo, individuos_en_entero[def_individuo], self.individuos[def_individuo])

        print("POBLACION INICIAL: ", self.poblacion)

    def insertar_individuos_a_poblacion(self, id_individuo, individuo_en_entero, individuo_en_bin):
        self.poblacion.append({"id": id_individuo, "entero": individuo_en_entero, "binario": individuo_en_bin})

    def generarParejasPoblacion(self):
        parejas = []
        for i in range(0, len(self.poblacion) - 1):
            for j in range(i, len(self.poblacion) - 1):
                individuo = self.poblacion[i]
                individuo_skip = self.poblacion[j + 1]
                parejas.append([[individuo['binario']], [individuo_skip['binario']]])
        #print("PAREJAS GENERADAS: ", parejas)
        return parejas
    
    def seleccionarParejasCruza(self, probabilidad_de_cruza):
        parejas = self.generarParejasPoblacion()
        probabilidades_aletorio = []

        for _ in range(len(parejas)):
            aleatorio_decimal = random.uniform(0.01, 1.0)
            aleatorio_decimal_redondeado = round(aleatorio_decimal, 2)
            probabilidades_aletorio.append(aleatorio_decimal_redondeado)

        posicion = 0
        while posicion < len(parejas):
            if probabilidades_aletorio[posicion] > probabilidad_de_cruza:
                parejas.pop(posicion)
            else:
                posicion = posicion + 1

        #print("PAREJAS SELECCIONADAS: ", parejas)
        return parejas
    
    def calcularValorX(self, numero_rand_asignado, inicio_intervalo, precision_deta_dex):
        x = inicio_intervalo + numero_rand_asignado * precision_deta_dex
        return x
    
    def calcularAptitud(self, x):
        fx = 1 - (x - 0.5)**2 / (1.5)**2 + (x - 1)**3 / (1.6)**2
        self.aptitudes.append(fx) 
        return fx

    def realizarCruza(self, parejas, num_bits):
        hijos = []
        punto_cruza = int(num_bits / 2)

        for pareja in parejas:
            self.id_individuo += 1
            individuo_pareja1 = pareja[0][0]
            individuo_pareja2 = pareja[1][0]

            hijo1 = individuo_pareja1[:punto_cruza] + individuo_pareja2[punto_cruza:]
            hijo2 = individuo_pareja2[:punto_cruza] + individuo_pareja1[punto_cruza:]

            hijos.append(["Individuo", self.id_individuo, self.binarioADecimal(hijo1), hijo1])
            self.id_individuo += 1
            hijos.append(["Individuo", self.id_individuo, self.binarioADecimal(hijo2), hijo2])

        #print("HIJOS: ", hijos)
        return hijos

    def verificarHijos(self, hijos, intervalo, presicion_input):
        hijos_aceptados = []

        for hijo in hijos:
            num_entero = hijo[2]
            # Pasar los argumentos faltantes a la función calcularValorX
            x = self.calcularValorX(num_entero, intervalo[0], presicion_input)
            if num_entero > 0 and x >= intervalo[0] and x <= intervalo[1]:
                hijos_aceptados.append(hijo)
        
        hijos.clear()

        for hijo_aceptado in hijos_aceptados:
            hijos.append(hijo_aceptado)
            num_individuo = hijo_aceptado[1]
            num_entero = hijo_aceptado[2]
            num_binario = hijo_aceptado[3]
            self.insertar_individuos_a_poblacion(num_individuo, num_entero, num_binario)

        #print("HIJOS DESPUES DE LA VERIFICACION:", hijos)
    
    def binarioADecimal(self, binario):
        decimal = int(binario, 2)
        return decimal

    def seleccionHijosMutacion(self, prob_mutacion_individuo):
        hijos_mutantes = []
        for hijo in self.poblacion:
            prob_aleatoria = random.random()
            if prob_aleatoria <= prob_mutacion_individuo:
                hijos_mutantes.append(hijo)
        return hijos_mutantes

    def mutacionHijos(self, prob_mutacion_gen, inicio_intervalo, final_intervalo, presicion_input):
        hijos_mutantes = []
        for hijo in hijos_mutantes:
            nuevo_binario = ""
            for bit in hijo["binario"]:
                prob_aleatoria = random.random()
                if prob_aleatoria <= prob_mutacion_gen:
                    nuevo_bit = "0"
                    if bit == "0":
                        nuevo_bit = "1"
                    nuevo_binario += nuevo_bit
                else:
                    nuevo_binario += bit

            entero_nuevo = int(nuevo_binario, 2)
            hijo["binario"] = nuevo_binario
            hijo["entero"] = entero_nuevo
            hijos_mutantes.append(hijo)

        self.verificarHijos(hijos_mutantes, (inicio_intervalo, final_intervalo), presicion_input)
    
    def podaPoblacion(self, pob_maxima, inicio_intervalo, presicion_input, minimizar):
        if len(self.poblacion) > pob_maxima:
            if minimizar:
                self.poblacion.sort(key=lambda individuo: self.calcularAptitud(self.calcularValorX(individuo["entero"], inicio_intervalo, presicion_input)))
            else:
                self.poblacion.sort(key=lambda individuo: self.calcularAptitud(self.calcularValorX(individuo["entero"], inicio_intervalo, presicion_input)), reverse=True)

            self.poblacion = self.poblacion[:pob_maxima]

    def limpiarDatos(self):
        self.individuos = []
        self.poblacion = []
        self.id_individuo = 0
        self.generacion = 0
        self.hijos = []
        self.generaciones = []
        self.mejor_x_generacion = []

    def graficarFuncion(self):
        x = np.linspace(-10, 10, num=1000)

        fx = [self.calcularAptitud(i) for i in x]

        plt.plot(x, fx)
        plt.title('Función objetivo')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True)
        plt.show()

    def GraficarAptitud(self):
        plt.plot(self.generaciones, self.mejor_x_generacion)
        plt.title('Evolución de la aptitud de la población')
        plt.xlabel('Generación')
        plt.ylabel('Aptitud')
        plt.grid(True)
        plt.show()
    
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = AG()
    GUI.show()
    sys.exit(app.exec_())

