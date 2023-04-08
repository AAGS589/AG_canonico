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

