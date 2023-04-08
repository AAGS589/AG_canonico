import random
from random import sample
import math
import matplotlib.pyplot as plt
import pandas as pd 
import numpy
from matplotlib import pyplot
import sys
from collections import Counter
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class AG(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("estilos.ui",self)
        self.inicioIntervalo.setText ("6")
        self.finalIntervalo.setText("12")
        self.pob_inicial.setText("4")
        self.pob_maxima.setText("15")
        self.num_generaciones.setText("10")
        self.presicion_input.setText("0.100")
        self.prob_cruza.setText("0.85")
        self.prob_mutacion_individuo.setText("0.2")
        self.prob_mutacion_gen.setText("0.1")
        self.btn_maximizar.clicked.connect(self.iniciarAlgoritmo)

        self.CANTIDADSOLUCIONES = 0
        self.CANTIDADBITS = 0
        self.ARREGLOCANTIDADBITS = []
        self.ARREGLOUNIR = []
        self.ARREGLOGENERACION = []
        self.LISTAINDIVIDUOS = []
        self.TEXTO = ""
        self.GRAFICAGENERACIONES = []
        self.IMG= 0
        

    def validarDatosUsuario(self):
        campos = [
            self.inicioIntervalo,
            self.finalIntervalo,
            self.pob_inicial,
            self.pob_maxima,
            self.num_generaciones,
            self.presicion_input,
            self.prob_cruza,
            self.prob_mutacion_individuo,
            self.prob_mutacion_gen,
        ]

        for campo in campos:
            if not campo.text():
                return False
            try:
                float(campo.text())
            except ValueError:
                return False

        return True
        pass

    def cantidadSoluciones(self):
        inicio_intervalo = float(self.inicioIntervalo.text())
        final_intervalo = float(self.finalIntervalo.text())
        precision = float(self.presicion_input.text())

        cantidad_soluciones = int((final_intervalo - inicio_intervalo) / precision)
        self.CANTIDADSOLUCIONES = cantidad_soluciones

        return cantidad_soluciones
        print (cantidad_soluciones)
        pass

    def cantidadBits(self):
        decimal = 0
        for x in range(self.CANTIDADSOLUCIONES):
            decimal = 2 ** x
            if self.CANTIDADSOLUCIONES <= decimal:
                # self.cantidadBitsText.setText(str(x))  
                self.CANTIDADBITS = x
                break
        pass

    def creacionIndividuo(self):
        print("----------------Método Creación de Individuos----------------")
        listaIndividuos = []
        for x in range(int(self.pob_inicial.text())):  # Cambia idPoblacionInicial a pob_inicial
            numeroBinario = ""
            for y in range(self.CANTIDADBITS):
                numero = random.randint(0, 1)
                numeroBinario += str(numero)
            if not self.binario_a_decimal(numeroBinario) == 0:
                listaIndividuos.append(numeroBinario)

        print("----------------Finalización del método----------------")
        self.LISTAINDIVIDUOS = listaIndividuos
        return listaIndividuos
        

    def selecionIndividuos(self, listaIndividuos):
        # Comentario: Seleccion de Individuos
        listaSeleccionIndividuos = []
        numero = 0
        numerov2 = 1
        self.ARREGLOUNIR = listaIndividuos
        while numero < len(listaIndividuos):
            binario = listaIndividuos[numero]
            while numerov2 < len(listaIndividuos):
                binario2 = listaIndividuos[numerov2]
                listaSeleccionIndividuos.append((binario, binario2, random.randint(1, 100) / 100, random.randint(1, self.CANTIDADBITS - 1)))
                numerov2 += 1
            numero += 1
            numerov2 = numero + 1
        # Comentario: Fin seleccion individuos
        return listaSeleccionIndividuos
        pass

    def cruzaIndividuos(self, listaSeleccionIndividuos):
        # Comentario: Cruza
        listaIndividuosCruzados = []
        for x in listaSeleccionIndividuos:
            letra1 = x[0]
            letra2 = x[1]
            if x[2] <= float(self.prob_cruza.text()):  # Cambia idPromedio a prob_cruza
                splitLetraCortada = letra1[0:x[3]]
                splitLetra2Cortada = letra2[0:x[3]]
                letraResultante = letra1[x[3]:]
                letraResultante2 = letra2[x[3]:]
                if not self.binario_a_decimal(splitLetraCortada + letraResultante2) == 0 and not self.binario_a_decimal(splitLetra2Cortada + letraResultante) == 0:
                    listaIndividuosCruzados.append(((splitLetraCortada + letraResultante2), ((random.randint(1, 100)) / 100), (splitLetra2Cortada + letraResultante), ((random.randint(1, 100)) / 100)))
            else:
                listaIndividuosCruzados.append((letra1, ((random.randint(1, 100)) / 100), letra2, ((random.randint(1, 100)) / 100)))
        # Comentario: Fin cruza
        return listaIndividuosCruzados
        pass

    def verificarPromedioDescendencia(self, listaIndividuosCruzados):
        # Comentario: Promedio descendencia
        return [x for x in listaIndividuosCruzados if x[2] <= float(self.prob_cruza.text())]

    def mutaIndividuo(self, listaIndividuosCruzados):
        # Comentario: Mutacion individuo
        lista_new_bin = []
        var_list = ""
        for x in listaIndividuosCruzados:
            binario = x[0]
            self.mutacionIndividuoCambioValor(binario, x, 1, var_list, lista_new_bin)
            binario = x[2]
            self.mutacionIndividuoCambioValor(binario, x, 3, var_list, lista_new_bin)
        # Comentario: Fin muta
        for x in lista_new_bin:
            self.ARREGLOUNIR.append(x)
        return self.ARREGLOUNIR
        pass

    def mutacionIndividuoCambioValor(self, binario, x, posicionAleatorio, var_list, lista_new_bin):
        if x[posicionAleatorio] <= float(self.prob_mutacion_individuo.text()):
            for i, y in enumerate(binario):
                if (random.randint(1, 100)) / 100 <= float(self.prob_mutacion_gen.text()):
                    if y == "0":
                        var_list += "1"
                    elif y == "1":
                        var_list += "0"
                else:
                    var_list += y
            if not self.binario_a_decimal(var_list) == 0:
                lista_new_bin.append(var_list)
            var_list = ""
        else:
            lista_new_bin.append(binario)

    def mutacionLimpieza(self, lista_new_bin):
        print("--------muta limpieza-------")
        listaNumber = []
        listaGneracion = []
        f = []
        inicio = int(self.inicioIntervalo.text())
        final = int(self.finalIntervalo.text())
        deltax = (final - inicio) / (self.CANTIDADSOLUCIONES - 1)
        listaValores = []
        for x in lista_new_bin:
            if self.binario_a_decimal(x) <= self.CANTIDADSOLUCIONES:
                d = self.binario_a_decimal(x)
                it = inicio + d * deltax
                # Actualizando la función objetivo
                fx = (it**2 * math.exp(it)) + (2 * math.cos(it))
                v = (x, it, fx)
                listaValores.append(fx)
                f.append(v)

        listaGneracion.append((
            max([x for x in listaValores]),
            min([x for x in listaValores]),
            numpy.mean(listaValores),
        ))
        print("-------fin muta limpieza-------")
        self.ARREGLOGENERACION.append([x for x in listaGneracion])
        return f
        

    def poda(self, f):
        listaPoblacionMinima = []
        listaGrficar = []
        print("--------poda------")
        print(f)

        if self.r1.isChecked():
            self.TEXTO = "Maximizar"
            f.sort(key=lambda x: x[2], reverse=True)
            if len(f) > int(self.pob_maxima.text()):
                self.eliminarRepetidos(f)
                listaPoblacionMinima = [x[0] for x in f][:int(self.pob_maxima.text())]
                listaGrficar = [x for x in f][:int(self.pob_maxima.text())]
            else:
                self.eliminarRepetidos(f)
                listaPoblacionMinima = [x[0] for x in f]
                listaGrficar = [x for x in f]

        if self.r2.isChecked():
            self.TEXTO = "Minimizar"
            f.sort(key=lambda x: x[2])
            if len(f) > int(self.idPoblacionMaxima.text()):
                self.eliminarRepetidos(f)
                listaPoblacionMinima = [x[0] for x in f][:int(self.idPoblacionMaxima.text())]
                listaGrficar = [x for x in f][:int(self.idPoblacionMaxima.text())]
            else:
                self.eliminarRepetidos(f)
                listaPoblacionMinima = [x[0] for x in f]
                listaGrficar = [x for x in f]

        print(f"Generacion nueva: {listaPoblacionMinima}")
        print("------fin poda------")
        self.GRAFICAGENERACIONES.append([(x[1], x[2], x[0]) for x in f])
        self.grafica2(listaGrficar)
        return listaPoblacionMinima
        pass
    
    def eliminarRepetidos(self, lista):
        status = True
        individuo1 = [self.binario_a_decimal(y[0]) for y in lista]
        listanew2 = [x for x, y in Counter(individuo1).items() if y > 1]
        print("----repetidos----")
        print(listanew2)
        for p in listanew2:
            individuo1.remove(p)

    def binario_a_decimal(self, numero_binario):
        numero_decimal = 0
        for posicion, digitio_string in enumerate(numero_binario[::-1]):
            numero_decimal += int(digitio_string) * 2 ** posicion
        
        return numero_decimal

    def mapearIndividuosAEspacioDeBusqueda(self, listaPoblacionMinima):
        inicio = int(self.inicioIntervalo.text())
        final = int(self.finalIntervalo.text())
        delta = (final - inicio) / self.CANTIDADBITS
        return [inicio + x * delta for x in listaPoblacionMinima]
    
    def calcularFuncionY(self,listaValoresx):
        return [(x**2 * math.exp(x) + 2 * math.cos(x)) for x in listaValoresx]


    def graficaHistorico(self):
        print(".-------grafica")
        texto = ""
        m = ""
        p = ""
        mejor = ""
        mejoresx = ""
        mejoresy = ""
        listaMejores = [(x[0][0], x[0][3]) for x in self.ARREGLOGENERACION]
        listaPeores = [x[0][1] for x in self.ARREGLOGENERACION]
        listaPromedio = [x[0][2] for x in self.ARREGLOGENERACION]
        x = [x for x in range(len(listaMejores))]

        pyplot.figure(figsize=(12, 6))

        if self.TEXTO == "Maximizar":
            m = "Mejores"
            p = "Peores"
            mejoresx = len(listaMejores) - 1
            mejoresy = listaMejores[-1]
            mejor = max(listaMejores, key=lambda x: x[1])
        else:
            m = "Peores"
            p = "Mejores"
            mejoresx = len(listaPeores) - 1
            mejoresy = listaPeores[-1]
            mejor = min(listaPeores)

        pyplot.plot(x, listaMejores, label=f"{m}")
        pyplot.plot(x, listaPeores, label=f"{p}")
        pyplot.plot(x, listaPromedio, label="Promedio")
        pyplot.scatter(mejoresx, mejoresy, label=f"El mejor individuo {round(mejor[1], 3)}", color="red")
        pyplot.title(f"Grafica historica {self.TEXTO}")
        pyplot.xlabel("Generaciones")
        pyplot.ylim(-10, 50)  # Ajustar límites de la gráfica
        pyplot.legend()
        pyplot.show()


    def grafica2(self,f):
        x = []
        y = []

        for x2 in f:
            x.append(self.binario_a_decimal(x2[0]))
            y.append((0.75*math.cos(1.50*x2[1]))*(math.sin(0.75*x2[1])) +( 0.25*math.cos(0.25*x2[1])))

        x.sort()
        y.sort()
        
        fig4 = pyplot.figure(figsize=(12,6))
        fig4.tight_layout()
        pyplot.scatter(x,y,label="Mejores Individuos")
        if x and y:
            pyplot.scatter(x[-1], y[-1], color="red")
        pyplot.xlim(min(x)-1, max(x)+1)
        pyplot.title(f"{self.TEXTO} grafica{self.IMG}")
        pyplot.savefig(f"img/i{self.IMG}.png")
        pyplot.close()
        
        self.IMG+=1
    pass

    def iniciarAlgoritmo(self):
        if self.validarDatosUsuario():
            self.ARREGLOCANTIDADBITS.clear()
            self.cantidadSoluciones()
            self.cantidadBits()
            listaIndividuo = self.creacionIndividuo()
            print("---------------------------")
            print("---------------------------")
            for x in range(int(self.num_generaciones.text())):
                print(f"Generacion: {x}")
                listaSeleccionIndividuos = self.selecionIndividuos(listaIndividuo)
                print("---------------------------")
                print("---------------------------")
                listaIndividuosCruzados  = self.cruzaIndividuos(listaSeleccionIndividuos)
                print("---------------------------")
                print("---------------------------")
                listaNewBin = self.mutaIndividuo(listaIndividuosCruzados)
                print("---------------------------")
                print("---------------------------")
                f = self.mutacionLimpieza(listaNewBin)
               
                print("---------------------------")
                print("---------------------------")
                listaIndividuo = self.poda(f)

            self.graficaHistorico()
            self.crearVideo()
            self.ARREGLOUNIR.clear()
            self.ARREGLOGENERACION.clear()
            self.LISTAINDIVIDUOS.clear()
            self.TEXTO = ""
            self.GRAFICAGENERACIONES.clear()
            self.IMG= 0
        else:
            self.msj_error.setText("Error faltan campos por rellenar")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = AG()
    GUI.show()
    sys.exit(app.exec_())
