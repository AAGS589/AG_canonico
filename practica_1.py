import random
from random import sample
import math
import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib import pyplot
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QRadioButton


class AG(QMainWindow):


    def __init__(self):
        super().__init__()
        uic.loadUi("estilos.ui",self)
        self.inicioIntervalo.setText ("")
        self.finalIntervalo.setText("")
        self.pob_inicial.setText("")
        self.pob_maxima.setText("")
        self.num_generaciones.setText("")
        self.presicion_input.setText("")
        self.prob_cruza.setText("")
        self.prob_mutacion_individuo.setText("")
        self.prob_mutacion_gen.setText("")
        #Checkboxes
        self.radio_maximizar = self.findChild(QRadioButton, 'radio_maximizar')
        self.radio_minimizar = self.findChild(QRadioButton, 'radio_minimizar')

        #Botones
        self.btn_maximizar.clicked.connect(self.iniciarAlgoritmo)
        self.btn_graficar_funcion.connect(self.graficarFuncion)
        self.btn_graficar_aptitud.connect(self.GraficarAptitud)
    
    def iniciarAlgoritmo(self):
        try:
            # Obtener y validar los valores ingresados por el usuario
            inicio_intervalo = float(self.inicioIntervalo.text())
            final_intervalo = float(self.finalIntervalo.text())
            pob_inicial = int(self.pob_inicial.text())
            pob_maxima = int(self.pob_maxima.text())
            num_generaciones = int(self.num_generaciones.text())
            presicion_input = int(self.presicion_input.text())
            prob_cruza = float(self.prob_cruza.text())
            prob_mutacion_individuo = float(self.prob_mutacion_individuo.text())
            prob_mutacion_gen = float(self.prob_mutacion_gen.text())

            if inicio_intervalo >= final_intervalo:
                raise ValueError("El inicio del intervalo debe ser menor que el final del intervalo.")
            
            if pob_inicial <= 0 or pob_maxima <= 0 or num_generaciones <= 0:
                raise ValueError("La población inicial, la población máxima y el número de generaciones deben ser mayores que 0.")
            
            if presicion_input <= 0:
                raise ValueError("La precisión debe ser un entero positivo.")
            
            if not (0 <= prob_cruza <= 1) or not (0 <= prob_mutacion_individuo <= 1) or not (0 <= prob_mutacion_gen <= 1):
                raise ValueError("Las probabilidades de cruza, mutación del individuo y mutación del gen deben estar en el rango [0, 1].")

            # Limpiar el mensaje de error
            self.msj_error.setText("")

            # Verificar si se debe maximizar o minimizar la función
            if self.radio_maximizar.isChecked():
                objetivo = "maximizar"
            else:
                objetivo = "minimizar"

            # Implementar el algoritmo genético utilizando los parámetros obtenidos

            # 1. Inicialización: Crear la población inicial

            # 2. Evaluación: Calcular la aptitud (fitness) de cada individuo

            # 3. Selección: Seleccionar individuos para la reproducción (cruce)

            # 4. Cruce: Generar descendientes a partir de los individuos seleccionados

            # 5. Mutación: Mutar genes de los nuevos individuos

            # 6. Reemplazo: Reemplazar individuos menos aptos por los nuevos individuos

            # 7. Iteración: Repetir el proceso hasta alcanzar el número de generaciones o algún criterio de convergencia
   
        except ValueError as e:
            # Mostrar el mensaje de error en el QLabel
            self.msj_error.setText(str(e))

        except Exception as e:
             # Mostrar un mensaje de error genérico en el QLabel
            self.msj_error.setText("Error: Por favor, revisa los valores ingresados.")
            print(e)

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

