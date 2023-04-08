import random
from random import sample
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
        self.finalIntervalo.setText("10")
        self.pob_inicial.setText("5")
        self.pob_maxima.setText("10")
        self.num_generaciones.setText("20")
        self.presicion_input.setText("0.01")
        self.prob_cruza.setText("0.2")
        self.prob_mutacion_individuo.setText("0.2")
        self.prob_mutacion_gen.setText("0.2")
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
    
    def iniciarAlgoritmo(self):
        try:
            # Obtener y validar los valores ingresados por el usuario
            inicio_intervalo = int(self.inicioIntervalo.text())
            final_intervalo = int(self.finalIntervalo.text())
            pob_inicial = int(self.pob_inicial.text())
            pob_maxima = int(self.pob_maxima.text())
            num_generaciones = int(self.num_generaciones.text())
            presicion_input = float(self.presicion_input.text())
            prob_cruza = float(self.prob_cruza.text())
            prob_mutacion_individuo = float(self.prob_mutacion_individuo.text())
            prob_mutacion_gen = float(self.prob_mutacion_gen.text())

            if inicio_intervalo >= final_intervalo:
                raise ValueError("El inicio del intervalo debe ser menor que el final del intervalo.")
            
            if pob_inicial <= 0 or pob_maxima <= 0 or num_generaciones <= 0:
                raise ValueError("La población inicial, la población máxima y el número de generaciones deben ser mayores que 0.")
            
            if presicion_input >= 1:
                raise ValueError("La precisión debe ser menor a 1.")
            
            if not (0 <= prob_cruza <= 1) or not (0 <= prob_mutacion_individuo <= 1) or not (0 <= prob_mutacion_gen <= 1):
                raise ValueError("Las probabilidades de cruza, mutación del individuo y mutación del gen deben estar en el rango [0, 1].")

            # Limpiar el mensaje de error
            self.msj_error.setText("")

            # Verificar si se debe maximizar o minimizar la función
            if self.radio_maximizar.isChecked():
                objetivo = "maximizar"
            else:
                objetivo = "minimizar"
            
            num_bits = self.cantidadDeBits(inicio_intervalo, final_intervalo, presicion_input)
            
             # Calcular el rango de los individuos
            rango = final_intervalo - inicio_intervalo
        
            # Generar la población inicial
            self.generarPoblacionInicial(rango, pob_inicial, num_bits)
        except ValueError as e:
            # Mostrar el mensaje de error en el QLabel
            self.msj_error.setText(str(e))

        except Exception as e:
             # Mostrar un mensaje de error genérico en el QLabel
            self.msj_error.setText("Error: Por favor, revisa los valores ingresados.")
            print(e)
    
    def cantidadDeBits(self, inicio_intervalo, final_intervalo, presicion_input):
        rango = final_intervalo - inicio_intervalo
        num_valores = rango * (10 ** presicion_input)
        num_bits = math.ceil(math.log2(num_valores))
        #print("Cantidad de bits necesarios:", num_bits)
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
        print("PAREJAS GENERADAS: ", parejas)
    
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

        print("PAREJAS SELECCIONADAS: ", parejas)
        return parejas
    
    def calcularValorX(self, numero_rand_asignado, inicio_intervalo, precision_deta_dex):
        x = inicio_intervalo + numero_rand_asignado * precision_deta_dex   
        return x
    
    def calcularAptitud(self, x):
        fx = 1 - (x - 0.5)**2 / (1.5)**2 + (x - 1)**3 / (1.6)**2
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

            hijos.append(["Individuo", self.id_individuo, self.binario_a_decimal(hijo1), hijo1])
            self.id_individuo += 1
            hijos.append(["Individuo", self.id_individuo, self.binario_a_decimal(hijo2), hijo2])

        print("HIJOS: ", hijos)
        return hijos

    def verificarHijos(self, hijos, intervalo):
        hijos_aceptados = []

        for hijo in hijos:
            num_entero = hijo[2]
            x = self.calcular_x(num_entero)
            if num_entero > 0 and x >= intervalo[0] and x <= intervalo[1]:
                hijos_aceptados.append(hijo)
        
        hijos.clear()

        for hijo_aceptado in hijos_aceptados:
            hijos.append(hijo_aceptado)
            num_individuo = hijo_aceptado[1]
            num_entero = hijo_aceptado[2]
            num_binario = hijo_aceptado[3]
            self.insertar_individuos_a_poblacion(num_individuo, num_entero, num_binario)

        print("HIJOS DESPUES DE LA VERIFICACION:", hijos)

    def binarioADecimal(self, numero_binario):
        numero_decimal = 0

        for posicion, digito_string in enumerate(numero_binario[::-1]):
            numero_decimal += int(digito_string) * 2 ** posicion

        return numero_decimal
    
    def seleccionHijosMutacion(self):
        probabilidades_aletorio = []

        for i in range(len(self.hijos)):
            aleatorio_decimal = random.uniform(0.01, 1.0)
            aleatorio_decimal_redondeado = round(aleatorio_decimal, 2)
            probabilidades_aletorio.append(aleatorio_decimal_redondeado)


    def seleccionHijosMutacion(self):
        probabilidades_aletorio = []

        for i in range(len(self.hijos)):
            aleatorio_decimal = random.uniform(0.01, 1.0)
            aleatorio_decimal_redondeado = round(aleatorio_decimal, 2)
            probabilidades_aletorio.append(aleatorio_decimal_redondeado)

        posicion = 0
        self.seleccion_hijos = []
        self.indice_hijos_seleccionados = []
        
        while posicion < len(self.hijos):
            if probabilidades_aletorio[posicion] < self.prob_mutacion_individuo:
                self.seleccion_hijos.append(self.hijos[posicion])
                self.indice_hijos_seleccionados.append(posicion)
                self.hijos.pop(posicion)
            else:
                posicion = posicion + 1

        print("HIJOS SELECCIONADOS:", self.seleccion_hijos)

    def graficarFuncion(self):
        # Implementación de la función para graficar la función objetivo
        pass

    def GraficarAptitud(self):
        # Implementación de la función para graficar la aptitud de la población
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = AG()
    GUI.show()
    sys.exit(app.exec_())

