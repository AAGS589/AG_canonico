import random
from random import sample
import math
import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib import pyplot
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


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
        
        #Botones
        self.btn_maximizar.clicked.connect(self.iniciarAlgoritmo)

    
    def iniciarAlgoritmo():
        print("Inicio")    

            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = AG()
    GUI.show()
    sys.exit(app.exec_())

