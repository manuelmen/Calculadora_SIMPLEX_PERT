from PyQt5.QtWidgets import *
from interfaz.ui_METODOSIMPLEX import Ui_MainWindow
from functools import partial
import sys
import os
import webbrowser
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, PageBreak, Image, Spacer,
Paragraph, Table, TableStyle)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from PyQt5.QtGui import QIcon

class Simplex(QMainWindow):

    def __init__(self, ui, icono):
        super(Simplex, self).__init__()
        self.ui = ui
        self.icono = icono
        # self.ui.setupUi(self)
        self.setWindowIcon(QIcon(self.icono))

        self.ui.ayuda.clicked.connect(self.ayuda)

        self.estilos = getSampleStyleSheet()
 
        self.ui.calcular.setEnabled(False)
        self.ui.nuevo.setEnabled(False)
        self.ui.imprimir.setEnabled(False)
        self.ui.modelo.clicked.connect(self.generarModelo)
        self.ui.mostrar.clicked.connect(self.mostrarDatos)
        self.ui.nuevo.clicked.connect(self.nuevo)
        self.ui.calcular.clicked.connect(self.encontrarPivote3R)
        self.ui.imprimir.clicked.connect(self.generarReporte)
        self.ui.pushButton.clicked.connect(self.salir)
        # self.ui.salir.clicked.connect(self.salir)
        self.contador = 0
        self.ui.numRestricciones.setMinimum(2)
        self.ui.numRestricciones.setMaximum(3)

    #Ayuda
    def ayuda(self):

        webbrowser.open("https://drive.google.com/file/d/1XqAo14FZAPXVnsMtKnCEOgpD6ju6rDLt/view?usp=sharing", new=2, autoraise=True)

    #Notificación
    def show_dialog(self):
        QMessageBox.about(self, "Aviso", "EL ejercicio ha finalizado")
    #alerta de ingresar datos
    def show_alert(self):
        QMessageBox.warning(self, "Error", "Debe llenar todos los datos correctamente.")
    
    #Salir de la aplicacion
    def salir(self):
        reply = QMessageBox.question(self, "Salir", "¿Seguro quiere salir de Simplex?", QMessageBox.Yes, QMessageBox.No)
  
        if reply == QMessageBox.Yes:
            self.ui.widgetS.setVisible(False)
            self.ui.frame_2.setVisible(True)
        else:
            print("Ventana no se cerro")

    

    #generar pdf del resultado 
    def generarReporte(self):
        numRestriccion = int(self.ui.numRestricciones.value())

        if numRestriccion == 2:
         

            try:
                Fila1 = []
                Fila2 = []
                Fila3 = []
                Fila4 = []
                Fila5 = []
                Fila6 = []

                for i in range(7):
                    #Extrae valores de fila 0
                    itemFila0 = self.ui.matriz.item(0,i).text()
                    Fila1.append(itemFila0)
                    #Extrae valores de fila 1
                    itemFila1 = self.ui.matriz.item(1,i).text()
                    Fila2.append(itemFila1)
                    if i >= 2:
                        #Extrae valores de fila 2
                        itemFila2 = float(self.ui.matriz.item(2,i).text())
                        Fila3.append("{:.3f}".format(itemFila2))
                        #Extrae valores de fila 3
                        itemFila3 = float(self.ui.matriz.item(3,i).text())
                        Fila4.append("{:.3f}".format(itemFila3))
                        #Extrae valores de fila 4
                        itemFila4 = float(self.ui.matriz.item(4,i).text())
                        Fila5.append("{:.3f}".format(itemFila4))
                        if i == 6:
                            #Extrae valores de fila 5
                            itemFila5 = self.ui.matriz.item(5,i).text()
                            Fila6.append(itemFila5)
                        else:
                            #Extrae valores de fila 6
                            itemFila5 = float(self.ui.matriz.item(5,i).text())
                            Fila6.append("{:.3f}".format(itemFila5))
                        

                    else:
                        #Extrae valores de fila 2
                        itemFila2 = self.ui.matriz.item(2,i).text()
                        Fila3.append(itemFila2)
                        #Extrae valores de fila 3
                        itemFila3 = self.ui.matriz.item(3,i).text()
                        Fila4.append(itemFila3)
                        #Extrae valores de fila 4
                        itemFila4 = self.ui.matriz.item(4,i).text()
                        Fila5.append(itemFila4)
                        #Extrae valores de fila 5
                        itemFila5 = self.ui.matriz.item(5,i).text()
                        Fila6.append(itemFila5)

                funcion = self.ui.label_funObj.text()
                funcion_objetivo = f'Max {funcion}'
                print(funcion_objetivo)   

                resultado1 = self.ui.label_varEntra.text()
                resultado2 = self.ui.label_varSale.text()
                resultado3 = self.ui.valorZ.text()

                doc = SimpleDocTemplate("Metodo_Simplex_1.pdf", pagesize = A4)
                alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13, leading=40)
                alineacionResultados = ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=12, leading=30)
                alineacionFuncion = ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=12, leading=40)
                story=[]
                t = Table([
                        Fila1, 
                        Fila2, 
                        Fila3,
                        Fila4,
                        Fila5,
                        Fila6
                    ], colWidths=45, rowHeights=30)

                t.setStyle([
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            ('BOX',(0,0),(-1,-1),2,colors.black),
                            ('BACKGROUND', (0, 2), (-1, 0), colors.lightgrey),
                            ('BACKGROUND', (1, 0), (1, 6), colors.lightgrey),
                            ('BACKGROUND', (6, 4), (6, 4), colors.aqua),
                    ])
                titulo = " Método Simplex de 2 restricciones "
                story.append(Paragraph(titulo, alineacionTitulo))
                story.append(Paragraph(funcion_objetivo, alineacionFuncion))
                story.append(Paragraph(resultado1, alineacionResultados))
                story.append(Paragraph(resultado2, alineacionResultados))
                story.append(Paragraph(resultado3, alineacionResultados))
                story.append(t)                
                story.append(Spacer(0,15))
                doc.build(story)
                os.system("Metodo_Simplex_1.pdf")

            
                print("Se genero el reporte")
            except PermissionError:
                print("No se genero el PDF")

        elif numRestriccion == 3:
            try:
                Fila1 = []
                Fila2 = []
                Fila3 = []
                Fila4 = []
                Fila5 = []
                Fila6 = []
                Fila7 = []

                for i in range(8):
                    #Extrae valores de fila 0
                    itemFila0 = self.ui.matriz.item(0,i).text()
                    Fila1.append(itemFila0)
                    #Extrae valores de fila 1
                    itemFila1 = self.ui.matriz.item(1,i).text()
                    Fila2.append(itemFila1)
                    if i >= 2:
                        #Extrae valores de fila 2
                        itemFila2 = float(self.ui.matriz.item(2,i).text())
                        Fila3.append("{:.3f}".format(itemFila2))
                        #Extrae valores de fila 3
                        itemFila3 = float(self.ui.matriz.item(3,i).text())
                        Fila4.append("{:.3f}".format(itemFila3))
                        #Extrae valores de fila 4
                        itemFila4 = float(self.ui.matriz.item(4,i).text())
                        Fila5.append("{:.3f}".format(itemFila4))
                        #Extrae valores de fila 5
                        itemFila5 = float(self.ui.matriz.item(5,i).text())
                        Fila6.append("{:.3f}".format(itemFila5))
                        if i == 7:
                            #Extrae valores de fila 5
                            itemFila6 = self.ui.matriz.item(6,i).text()
                            Fila7.append(itemFila6)
                        else:
                            #Extrae valores de fila 6
                            itemFila6 = float(self.ui.matriz.item(6,i).text())
                            Fila7.append("{:.3f}".format(itemFila6))
                        

                    else:
                        #Extrae valores de fila 2
                        itemFila2 = self.ui.matriz.item(2,i).text()
                        Fila3.append(itemFila2)
                        #Extrae valores de fila 3
                        itemFila3 = self.ui.matriz.item(3,i).text()
                        Fila4.append(itemFila3)
                        #Extrae valores de fila 4
                        itemFila4 = self.ui.matriz.item(4,i).text()
                        Fila5.append(itemFila4)
                        #Extrae valores de fila 5
                        itemFila5 = self.ui.matriz.item(5,i).text()
                        Fila6.append(itemFila5)
                        #Extrae valores de fila 6
                        itemFila6 = self.ui.matriz.item(6,i).text()
                        Fila7.append(itemFila6)

                funcion = self.ui.label_funObj.text()
                funcion_objetivo = f'Max {funcion}'
                print(funcion_objetivo)   

                resultado1 = self.ui.label_varEntra.text()
                resultado2 = self.ui.label_varSale.text()
                resultado3 = self.ui.valorZ.text()
                resultado4 = self.ui.valorZ3.text()

                doc = SimpleDocTemplate("Metodo_Simplex_2.pdf", pagesize = A4)
                alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13, leading=40)
                alineacionResultados = ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=12, leading=40)
                alineacionFuncion = ParagraphStyle(name="centrar", alignment=TA_LEFT, fontSize=12, leading=40)
                story=[]
                t = Table([
                        Fila1, 
                        Fila2, 
                        Fila3,
                        Fila4,
                        Fila5,
                        Fila6,
                        Fila7
                    ], colWidths=50, rowHeights=30)

                t.setStyle([
                            ('GRID',(0,0),(-1,-1),0.5,colors.grey),
                            ('BOX',(0,0),(-1,-1),2,colors.black),
                            ('BACKGROUND', (0, 2), (-1, 0), colors.lightgrey),
                            ('BACKGROUND', (1, 0), (1, 6), colors.lightgrey),
                            ('BACKGROUND', (7, 5), (7, 5), colors.aqua),
                    ])
                titulo = " Método Simplex de 3 restricciones"
                story.append(Paragraph(titulo, alineacionTitulo))
                story.append(Paragraph(funcion_objetivo, alineacionFuncion))
                story.append(Paragraph(resultado1, alineacionResultados))
                story.append(Paragraph(resultado2, alineacionResultados))
                story.append(Paragraph(resultado3, alineacionResultados))
                story.append(Paragraph(resultado4, alineacionResultados))
                story.append(t)                
                story.append(Spacer(0,15))
                doc.build(story)
                os.system("Metodo_Simplex_2.pdf")

            
            
                print("Se genero el reporte")
            except PermissionError:
                print("No se genero el PDF")

    #Tabla 3 restricciones
    def tabla3r(self, arregloInversos, row, colum, Xb, complemento1, complemento2,xn2, xn1):
        
        # print(xn1)
        self.contador += 1
        self.ui.label_iterador.setText(str(self.contador))
        self.ui.matriz.setItem(row,0, QTableWidgetItem(str(arregloInversos[0])))
        #Agregamos valor xb de la fila 1
        self.ui.matriz.setItem(row,1, QTableWidgetItem(Xb))

        #Agregamos nuevos valores de la fila del pivote
        for h in range(6):
            self.ui.matriz.setItem(row,h+2, QTableWidgetItem(str(arregloInversos[h+1])))

        if row == 2:
            #Saca valor de fila del pivote y multiplica por el complemento 1
            arrayFila = []
            for i in range(6):
                item = float(self.ui.matriz.item(row,i+2).text())
                items = item*complemento1
                arrayFila.append(items)
            #Saca los valores de la fila que sigue del pivote para restarlo con arrayFila para la nueva fila
            array_nueva_fila = []
            for a in range(0, len(arrayFila)):
                item = float(self.ui.matriz.item(xn1,a+2).text())
                valores = arrayFila[a]+item
                array_nueva_fila.append(valores)
            # Agregamos esa nueva fila 3
            for f in range(6):
                self.ui.matriz.setItem(xn1,f+2, QTableWidgetItem(str(array_nueva_fila[f])))

            #Saca el valor de la fila del pivote y multiplica por el complemento 2
            arrayFila2 = []
            for j in range(6):
                item = float(self.ui.matriz.item(row,j+2).text())
                items = item*complemento2
                arrayFila2.append(items)
            
            #Saca los valores de la fila que sigue despues de la del pivote para restarlo con arrayFila2 para la nueva fila
            array_nueva_fila2 = []
            for h in range(0, len(arrayFila2)):
                item = float(self.ui.matriz.item(xn2,h+2).text())
                valores = arrayFila2[h]+item
                array_nueva_fila2.append(valores)
            
            # Agregamos esa nueva fila 4
            for g in range(6):
                self.ui.matriz.setItem(xn2,g+2, QTableWidgetItem(str(array_nueva_fila2[g])))

            #Sacamos los valores de Cb para multiplicar por la suma y sacar ZJ
            Cb1 = float(self.ui.matriz.item(2,0).text())
            Cb2 = float(self.ui.matriz.item(3,0).text())
            Cb3 = float(self.ui.matriz.item(4,0).text())

            #Sacamos Zj y la agregamos a la tabla
            Zj = []
            for m in range(0,len(array_nueva_fila)):
                multiplicacion = (Cb1*arregloInversos[m+1])+(Cb2*array_nueva_fila[m])+(Cb3*array_nueva_fila2[m])
                Zj.append(multiplicacion)
                self.ui.matriz.setItem(5,m+2, QTableWidgetItem(str(multiplicacion)))

            #Sacamos Cj-Zj y agregamos a la tabla
            # sacamos valores de Cj
            for z in range(5):
                item = float(self.ui.matriz.item(0,z+2).text())
                resta = item-Zj[z]
                self.ui.matriz.setItem(6,z+2, QTableWidgetItem(str(resta)))
            self.datos_tabla_actual_2r()


        elif row == 3:
            
            #Saca el valor de la fila del pivote y multiplica por el complemento 1
            arrayFila = []
            for i in range(6):
                item = float(self.ui.matriz.item(row,i+2).text())
                items = item*complemento1
                arrayFila.append(items)
            #Saca los valores de la fila que sigue del pivote para restarlo con arrayFila para la nueva fila
            array_nueva_fila = []
            for a in range(0, len(arrayFila)):
                item = float(self.ui.matriz.item(2,a+2).text())
                valores = arrayFila[a]+item
                array_nueva_fila.append(valores)
            # Agregamos esa nueva fila 3
            for f in range(6):
                self.ui.matriz.setItem(2,f+2, QTableWidgetItem(str(array_nueva_fila[f])))
            # print(xn1)

            #Saca el valor de la fila del pivote y multiplica por el complemento 2
            arrayFila2 = []
            for j in range(6):
                item = float(self.ui.matriz.item(row,j+2).text())
                items = item*complemento2
                arrayFila2.append(items)
            
            #Saca los valores de la fila que sigue despues de la del pivote para restarlo con arrayFila2 para la nueva fila
            array_nueva_fila2 = []
            for h in range(0, len(arrayFila2)):
                item = float(self.ui.matriz.item(4,h+2).text())
                valores = arrayFila2[h]+item
                array_nueva_fila2.append(valores)
            
            #Agregamos nueva fila 4
            for g in range(6):
                self.ui.matriz.setItem(4,g+2, QTableWidgetItem(str(array_nueva_fila2[g])))

            #Sacamos los valores de Cb para multiplicar por la suma y sacar ZJ
            Cb1 = float(self.ui.matriz.item(2,0).text())
            Cb2 = float(self.ui.matriz.item(3,0).text())
            Cb3 = float(self.ui.matriz.item(4,0).text())

            #Sacamos Zj y la agregamos a la tabla
            Zj = []
            for m in range(0,len(array_nueva_fila)):
                multiplicacion = (Cb1*array_nueva_fila[m])+(Cb2*arregloInversos[m+1])+(Cb3*array_nueva_fila2[m])
                Zj.append(multiplicacion)
                self.ui.matriz.setItem(5,m+2, QTableWidgetItem(str(multiplicacion)))
            

            # Sacamos Cj-Zj y la agregamos a la tabla
            # sacamos los valores de Cj
            for z in range(5):
                item = float(self.ui.matriz.item(0,z+2).text())
                resta = item-Zj[z]
                self.ui.matriz.setItem(6,z+2, QTableWidgetItem(str(resta)))
            self.datos_tabla_actual_2r()

        elif row == 4:
            # print(complemento1)
            # print(complemento2)
            #Saca el valor de la fila del pivote y multiplica por el complemento 1
            arrayFila = []
            for i in range(6):
                item = float(self.ui.matriz.item(row,i+2).text())
                items = item*complemento1
                arrayFila.append(items)
            #Saca los valores de la fila que sigue del pivote para restarlo con arrayFila para la nueva fila
            array_nueva_fila = []
            for a in range(0, len(arrayFila)):
                item = float(self.ui.matriz.item(2,a+2).text())
                valores = arrayFila[a]+item
                array_nueva_fila.append(valores)
            # Agregamos esa nueva fila 3
            for f in range(6):
                self.ui.matriz.setItem(2,f+2, QTableWidgetItem(str(array_nueva_fila[f])))
            # print(xn1)

            #Saca el valor de la fila del pivote y multiplica por el complemento 2
            arrayFila2 = []
            for j in range(6):
                item = float(self.ui.matriz.item(row,j+2).text())
                items = item*complemento2
                arrayFila2.append(items)
            
            #Saca valores de la fila que sigue despues de la del pivote para restarlo con arrayFila2 para la nueva fila
            array_nueva_fila2 = []
            for h in range(0, len(arrayFila2)):
                item = float(self.ui.matriz.item(3,h+2).text())
                valores = arrayFila2[h]+item
                array_nueva_fila2.append(valores)
            
            # Agregamos esa nueva fila 4
            for g in range(6):
                self.ui.matriz.setItem(3,g+2, QTableWidgetItem(str(array_nueva_fila2[g])))

            #Sacamos los valores de Cb para multiplicar por la suma y sacar ZJ
            Cb1 = float(self.ui.matriz.item(2,0).text())
            Cb2 = float(self.ui.matriz.item(3,0).text())
            Cb3 = float(self.ui.matriz.item(4,0).text())

            #Sacamos Zj y la agregamos a la tabla
            Zj = []
            for m in range(0,len(array_nueva_fila)):
                multiplicacion = (Cb1*array_nueva_fila[m])+(Cb2*array_nueva_fila2[m])+(Cb3*arregloInversos[m+1])
                Zj.append(multiplicacion)
                self.ui.matriz.setItem(5,m+2, QTableWidgetItem(str(multiplicacion)))
            

            # Sacamos Cj-Zj y la agregamos a la tabla
            # sacamos los valores de Cj
            for z in range(5):
                item = float(self.ui.matriz.item(0,z+2).text())
                resta = item-Zj[z]
                self.ui.matriz.setItem(6,z+2, QTableWidgetItem(str(resta)))
            self.datos_tabla_actual_2r()
        

        


    #Tabla 2 de 2 restricciones
    def tabla2(self, arregloInversos, row, colum, Xb, complemento,xn):
        # print(f'{row}-{colum}')
        # print(Xb)
        # print(arregloInversos)
        # print(complemento)
        # print(xn)
        #Agregamos el valor Cb de la fila 1
        
        self.contador += 1
        self.ui.label_iterador.setText(str(self.contador))
        # print(self.contador)
        self.ui.matriz.setItem(row,0, QTableWidgetItem(str(arregloInversos[0])))
        #Agregamos el valor xb de la fila 1
        self.ui.matriz.setItem(row,1, QTableWidgetItem(Xb))

        #Agregamos los nuevos valores de la fila del pivote
        for h in range(5):
            self.ui.matriz.setItem(row,h+2, QTableWidgetItem(str(arregloInversos[h+1])))

        
        

        #Fila 2 con valores naturales sin invertir
        arregloNaturales = []
        #Fila 2 valores invertidos multiplicados por el inverso
        arregloComplemento = []
       
        for c in range (5):
            items = self.ui.matriz.item(row,c+2)
            natural = float(items.text())
            arregloNaturales.append(natural)
            itemsC = natural*complemento
            arregloComplemento.append(itemsC)
        # print(arregloNaturales)

        arregloFila2 = []
        for f in range(5):
            itemsF = self.ui.matriz.item(xn,f+2)
            itemsFila = float(itemsF.text())
            arregloFila2.append(itemsFila)
        # print(arregloFila2)


        arregloTotal = []
        for t in range(0, len(arregloComplemento)):
            suma = arregloComplemento[t]+arregloFila2[t]
            arregloTotal.append(suma)
        # print(arregloTotal)
        #Agregamos los nuevos valores de la fila 2
        for t1 in range(5):
            self.ui.matriz.setItem(xn,t1+2, QTableWidgetItem(str(arregloTotal[t1])))
        
        # print(f'{Cb1}-{Cb2}')
        # print(arregloNaturales)
        # print(arregloComplemento) 
        Cb1 = 0
        Cb2 = 0
        if row == 2:
            #Valores Cb para multiplicar cada fila y cada columna
            Cb1 = float(self.ui.matriz.item(2,0).text())
            Cb2 = float(self.ui.matriz.item(3,0).text())
        else:
            #Valores Cb para multiplicar cada fila y cada columna
            Cb1 = float(self.ui.matriz.item(3,0).text())
            Cb2 = float(self.ui.matriz.item(2,0).text())


        arrayMultiplicacion = []
        for i in range(5):
            multiplicacion = (Cb1*arregloNaturales[i])+(Cb2*arregloTotal[i])
            arrayMultiplicacion.append(multiplicacion)
        # print(arrayMultiplicacion)#algo no esta bien
        
        
        for j in range(5):
            self.ui.matriz.setItem(4,j+2, QTableWidgetItem(str(arrayMultiplicacion[j])))

        arrayZj = []
        for cj in range(4):
            itemcj = float(self.ui.matriz.item(0,cj+2).text())
            
            zjCj = itemcj-arrayMultiplicacion[cj]
            arrayZj.append(zjCj)
            self.ui.matriz.setItem(5,cj+2, QTableWidgetItem(str(zjCj)))
        self.datos_tabla_actual()
        
    #Calcular la iteracion 3 restricciones
    def iteracion2(self, row, colum):
        
        if row == 3:
            pivote = float(self.ui.matriz.item(row, colum).text())
            #║Extrae el valor de Xb
            print(f'el pivote es: {pivote} desde la fila 3')
            Xb = self.ui.matriz.item(row-2, colum).text()
            #valor por el que multiplicaremos en la formula para sacar las demas filas
            m = self.ui.matriz.item(row-1,colum).text()
            n = self.ui.matriz.item(row+1,colum).text()
            complemento1 = float(m)*-1
            complemento2 = float(n)*-1

            invPivote = 1/pivote
            valorX = float(self.ui.matriz.item(row-3, colum).text())
            arrayItems = []
            #Agregamos el valor x encima del pivote al arreglo 
            for i in range(6):
                itemR = self.ui.matriz.item(row, i+2)
                itemRow = float(itemR.text())

                arrayItems.append(itemRow)
            
            arrayInversos = []
            arrayInversos.append(valorX)
            for j in range(0, len(arrayItems)):
                itemInverso = arrayItems[j]*invPivote
                arrayInversos.append(itemInverso)
            
            
            self.tabla3r(arrayInversos, row, colum, Xb, complemento1,complemento2, row-1,row+1)

        elif row == 2:
            pivote = float(self.ui.matriz.item(row, colum).text())
            #║Extrae el valor de Xb
            print(f'el pivote es: {pivote} desde la fila 2')
            Xb = self.ui.matriz.item(row-1, colum).text()

            #valor por el que multiplicaremos en la formula para sacar las demas filas
            m = self.ui.matriz.item(row+1,colum).text()
            n = self.ui.matriz.item(row+2,colum).text()
            complemento1 = float(m)*-1
            complemento2 = float(n)*-1
            
            invPivote = 1/pivote
            arrayItems = []
            
            valorX = float(self.ui.matriz.item(row-2, colum).text())
            #Agregamos el valor x encima del pivote al arreglo    
            
            for i in range(6):
                itemR = self.ui.matriz.item(row, i+2)
                itemRow = float(itemR.text())

                arrayItems.append(itemRow)
            
            arrayInversos = []
            arrayInversos.append(valorX)
            for j in range(0, len(arrayItems)):
                itemInverso = arrayItems[j]*invPivote
                arrayInversos.append(itemInverso)
            
            
            
            self.tabla3r(arrayInversos, row, colum, Xb, complemento1,complemento2, row+2, row+1)
        elif row == 4:
            pivote = float(self.ui.matriz.item(row, colum).text())
            #║Extrae el valor de Xb
            print(f'el pivote es: {pivote} desde la fila 3')
            Xb = self.ui.matriz.item(row-3, colum).text()
            #valor por el que multiplicaremos en la formula para sacar las demas filas
            m = self.ui.matriz.item(row-2,colum).text()
            n = self.ui.matriz.item(row-1,colum).text()
            complemento1 = float(m)*-1
            complemento2 = float(n)*-1

            invPivote = 1/pivote
            valorX = float(self.ui.matriz.item(row-4, colum).text())
            arrayItems = []
            #Agregamos el valor x encima del pivote al arreglo 
            for i in range(6):
                itemR = self.ui.matriz.item(row, i+2)
                itemRow = float(itemR.text())

                arrayItems.append(itemRow)
            
            arrayInversos = []
            arrayInversos.append(valorX)
            for j in range(0, len(arrayItems)):
                itemInverso = arrayItems[j]*invPivote
                arrayInversos.append(itemInverso)
            
            
            self.tabla3r(arrayInversos, row, colum, Xb, complemento1,complemento2, row-2, row-1)

            
            
                
            
    #Calcular la iteracion 2 restricciones
    def iteracion(self, row, colum):
        numRestriccion = int(self.ui.numRestricciones.value())
        # print(row)
        # print(colum)

        

        if row == 3:
            pivote = float(self.ui.matriz.item(row, colum).text())
            #║Extrae el valor de Xb
            print(f'el pivote es: {pivote} desde la fila 3')
            Xb = self.ui.matriz.item(row-2, colum).text()
            #valor por el que multiplicaremos en la formula para sacar las demas filas
            m = self.ui.matriz.item(row-1,colum).text()
            complemento = float(m)*-1

            invPivote = 1/pivote
            valorX = float(self.ui.matriz.item(row-3, colum).text())
            arrayItems = []
            #Agregamos el valor x encima del pivote al arreglo 
            for i in range(5):
                itemR = self.ui.matriz.item(row, i+2)
                itemRow = float(itemR.text())

                arrayItems.append(itemRow)
            
            arrayInversos = []
            arrayInversos.append(valorX)
            for j in range(0, len(arrayItems)):
                itemInverso = arrayItems[j]*invPivote
                arrayInversos.append(itemInverso)
            
            
            self.tabla2(arrayInversos, row, colum, Xb, complemento, row-1)

        else:
            pivote = float(self.ui.matriz.item(row, colum).text())
            #║Extrae el valor de Xb
            print(f'el pivote es: {pivote} desde la fila 2')
            Xb = self.ui.matriz.item(row-1, colum).text()

            #valor por el que multiplicaremos en la formula para sacar las demas filas
            m = self.ui.matriz.item(row+1,colum).text()
            complemento = float(m)*-1
            
            
            invPivote = 1/pivote
            arrayItems = []
            
            valorX = float(self.ui.matriz.item(row-2, colum).text())
            
            
                
            #Agregamos el valor x encima del pivote al arreglo    
            
            for i in range(5):
                itemR = self.ui.matriz.item(row, i+2)
                itemRow = float(itemR.text())

                arrayItems.append(itemRow)
            
            arrayInversos = []
            arrayInversos.append(valorX)
            for j in range(0, len(arrayItems)):
                itemInverso = arrayItems[j]*invPivote
                arrayInversos.append(itemInverso)
                       
            
            self.tabla2(arrayInversos, row, colum, Xb, complemento, row+1)
          
    
    #Encontrar el Pivote simplex de 2 restricciones
    def encontrarPivote3R(self):
        numRestriccion = int(self.ui.numRestricciones.value())

        if numRestriccion == 2:
            #ÞDeshabilita el boton mostrar datos y nuevo
            
            arrayZ = []
            for i in range(4):
                itemsZ = float(self.ui.matriz.item(5,i+2).text())
                arrayZ.append(itemsZ)
        

            if arrayZ[0] <= 0 and arrayZ[1] <= 0 and arrayZ[2] <= 0 and arrayZ[3] <= 0 :
                print("El programa ha finalizado")
                
                
            else:
                    
                varSale=0
                varEntra=0
                # x1= float(self.ui.matriz.item())
                # x2= funObX2
                # S1= 0
                # S2= 0
                arrayZj = []
                for m in range(4):
                    itemZj = self.ui.matriz.item(5,m+2)
                    Zj = float(itemZj.text())
                    arrayZj.append(Zj) 
                # arrayZjCj = [x1,x2,S1,S2]
                numMayor = max(arrayZj)
                # print(numMayor)

                if numMayor == arrayZj[0]:
                   
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 6).text())
                    bi2 = float(self.ui.matriz.item(3, 6).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2]
                    arregloVSaliente = []
                    for i in range(2):
                        item = float(self.ui.matriz.item(i+2,2).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para 0")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                    
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                        
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    
                        varSale=arrayBi[1]

                elif numMayor == arrayZj[1]:
                    #Encontramos la variable entrante
                    
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 6).text())
                    bi2 = float(self.ui.matriz.item(3, 6).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2]
                    arregloVSaliente = []
                    for i in range(2):
                        item = float(self.ui.matriz.item(i+2,3).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para 0")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                        
                        varSale=arrayBi[1]

                elif numMayor == arrayZj[2]:
                    #Encontramos la variable entrante
                   
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 6).text())
                    bi2 = float(self.ui.matriz.item(3, 6).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2]
                    arregloVSaliente = []
                    for i in range(2):
                        item = float(self.ui.matriz.item(i+2,4).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para 0")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                        
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                        
                        varSale=arrayBi[1]
                elif numMayor == arrayZj[3]:
                    
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 6).text())
                    bi2 = float(self.ui.matriz.item(3, 6).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2]
                    arregloVSaliente = []
                    for i in range(2):
                        item = float(self.ui.matriz.item(i+2,5).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para 0")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                        
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                        
                        varSale=arrayBi[1]
                    
            

              
                pivFila = 0 
                pivColumna = 0 
                c=6
                r=5
                for i in range(4):

                    itemFila = self.ui.matriz.item(r,i+2)
                    itemFila1 = float(itemFila.text())
                    pivote = i+2
                    
                    if itemFila1 == varEntra:
                        
                        pivColumna = pivote
                
                for i in range(2):
                    itemColumna = self.ui.matriz.item(i+2,c)
                    itemColumna1 = float(itemColumna.text())
                    pivote = i+2
                    if arrayCeldas[i] == 0:
                        print("nada que hacer")
                    else:
                        valor = itemColumna1/arrayCeldas[i]
                        if valor == variableSaliente:
                        
                            pivFila = pivote
                    
               
                self.iteracion(pivFila, pivColumna)
        elif numRestriccion == 3:
            #ÞDeshabilita el boton mostrar datos y nuevo
           

            arrayZ = []
            for i in range(5):
                itemsZ = float(self.ui.matriz.item(6,i+2).text())
                arrayZ.append(itemsZ)
          

            if arrayZ[0] <= 0 and arrayZ[1] <= 0 and arrayZ[2] <= 0 and arrayZ[3] <= 0 and arrayZ[4] <= 0:
                print("El programa ha finalizado")
                
            else:
                    
                varSale=0
                varEntra=0
                # x1= float(self.ui.matriz.item())
                # x2= funObX2
                # j1= 0
                # j2= 0
                arrayZj = []
                for m in range(5):
                    itemZj = self.ui.matriz.item(6,m+2)
                    Zj = float(itemZj.text())
                    arrayZj.append(Zj) 
                # arrayZjCj = [x1,x2,S1,S2]
                numMayor = max(arrayZj)
                print(numMayor)
                print(arrayZj)

                if numMayor == arrayZj[0]:
                   
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 7).text())
                    bi2 = float(self.ui.matriz.item(3, 7).text())
                    bi3 = float(self.ui.matriz.item(4, 7).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2,bi3]
                    arregloVSaliente = []
                    for i in range(3):
                        item = float(self.ui.matriz.item(i+2,2).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para 0")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                   
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                        
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                        
                        varSale=arrayBi[1]

                    if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                       
                        varSale=arrayBi[2]

                elif numMayor == arrayZj[1]:
                    #Encontramos la variable entrante
                    
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 7).text())
                    bi2 = float(self.ui.matriz.item(3, 7).text())
                    bi3 = float(self.ui.matriz.item(4, 7).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2,bi3]
                    arregloVSaliente = []
                    for i in range(3):
                        item = float(self.ui.matriz.item(i+2,3).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para cero")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                        
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                        
                        varSale=arrayBi[1]

                    if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                       
                        varSale=arrayBi[2]

                elif numMayor == arrayZj[2]:
                    #Encontramos la variable entrante
                    
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 7).text())
                    bi2 = float(self.ui.matriz.item(3, 7).text())
                    bi3 = float(self.ui.matriz.item(4, 7).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2,bi3]
                    arregloVSaliente = []
                    for i in range(3):
                        item = float(self.ui.matriz.item(i+2,4).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para 0")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                        
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                        
                        varSale=arrayBi[1]

                    if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                        
                        varSale=arrayBi[2]

                elif numMayor == arrayZj[3]:
                    #Encontramos la variable entrante
                    
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 7).text())
                    bi2 = float(self.ui.matriz.item(3, 7).text())
                    bi3 = float(self.ui.matriz.item(4, 7).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2,bi3]
                    arregloVSaliente = []
                    for i in range(3):
                        item = float(self.ui.matriz.item(i+2,5).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para 0")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                        
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                        
                        varSale=arrayBi[1]

                    if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                        
                        varSale=arrayBi[2]

                    if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                        
                        varSale=arrayBi[2]

                elif numMayor == arrayZj[4]:
                    #Encontramos la variable entrante
                    
                    varEntra=numMayor
                    #Encontramos la variable saliente
                    bi1 = float(self.ui.matriz.item(2, 7).text())
                    bi2 = float(self.ui.matriz.item(3, 7).text())
                    bi3 = float(self.ui.matriz.item(4, 7).text())
                    arrayCeldas = []
                    arrayBi = [bi1,bi2,bi3]
                    arregloVSaliente = []
                    for i in range(3):
                        item = float(self.ui.matriz.item(i+2,6).text())
                        arrayCeldas.append(item)
                        if item == 0:
                            print("No se divide para 0")
                        else:
                            resultado = arrayBi[i]/item
                            if resultado > 0:
                                arregloVSaliente.append(resultado)
                    variableSaliente = min(arregloVSaliente)
                    
                    #Determinamos si la variable saliente es S1 o S2
                    if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                       
                        varSale=arrayBi[0]
                    if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                       
                        varSale=arrayBi[1]

                    if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                        
                        varSale=arrayBi[2]
                    
            

                pivFila = 0 
                pivColumna = 0 
                c=7
                r=6
                for i in range(5):
                            
                    itemFila = self.ui.matriz.item(r,i+2)
                    itemFila1 = float(itemFila.text())
                    pivote = i+2
                    
                    if itemFila1 == varEntra:
                        
                        pivColumna = pivote
                # print(arrayCeldas)

                for i in range(3):
                    itemColumna = self.ui.matriz.item(i+2,c)
                    itemColumna1 = float(itemColumna.text())
                    pivote = i+2
                    if arrayCeldas[i] == 0:
                        print("nada que hacer")
                    else:
                        valor = itemColumna1/arrayCeldas[i]
                        if valor == variableSaliente:
                        
                            pivFila = pivote

                
                    
                
                self.iteracion2(pivFila,pivColumna)
            
        
    #Mostrar datos de Variable Entrante y saliente por tabla actual
    def datos_tabla_actual(self):
        arrayZ = []
        for i in range(4):
            itemsZ = float(self.ui.matriz.item(5,i+2).text())
            arrayZ.append(itemsZ)
        

        if arrayZ[0] <= 0 and arrayZ[1] <= 0 and arrayZ[2] <= 0 and arrayZ[3] <= 0 :
            print("El programa ha finalizado desde datos_tabla_actual")
            resultado1 = self.ui.matriz.item(2,1).text()
            resultado2 = self.ui.matriz.item(3,1).text()
            arregloBi = []
            for b in range(3):
                item = float(self.ui.matriz.item(b+2,6).text())
                arregloBi.append(item)
            self.ui.label_varEntra.setText(f'  {resultado1} = {"{:.1f}".format(arregloBi[0])}')
            self.ui.label_varSale.setText(f'  {resultado2} = {"{:.1f}".format(arregloBi[1])}')
            self.ui.valorZ.setText(f'  Z = {arregloBi[2]}')            
            
            self.show_dialog()
                        
            #Habilitar el boton mostrar datos y nuevo
            
            self.ui.mostrar.setEnabled(False)
            self.ui.calcular.setEnabled(False)
            self.ui.nuevo.setEnabled(True)
            self.ui.imprimir.setEnabled(True)
            self.contador = 0
            
        else:
            self.ui.nuevo.setEnabled(True)   
            self.ui.calcular.setEnabled(True)
            
            arrayZj = []
            for m in range(4):
                itemZj = self.ui.matriz.item(5,m+2)
                Zj = float(itemZj.text())
                arrayZj.append(Zj) 
           
            numMayor = max(arrayZj)
            
            if numMayor == arrayZj[0]:
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, X1')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 6).text())
                bi2 = float(self.ui.matriz.item(3, 6).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2]
                arregloVSaliente = []
                for i in range(2):
                    item = float(self.ui.matriz.item(i+2,2).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                variableSaliente = min(arregloVSaliente)
                
                
                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')
                    

            elif numMayor == arrayZj[1]:
                #Encontramos la variable entrante
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, X2')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 6).text())
                bi2 = float(self.ui.matriz.item(3, 6).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2]
                arregloVSaliente = []
                for i in range(2):
                    item = float(self.ui.matriz.item(i+2,3).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                variableSaliente = min(arregloVSaliente)
                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')
                    

            elif numMayor == arrayZj[2]:
                 #Encontramos la variable entrante
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, S1')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 6).text())
                bi2 = float(self.ui.matriz.item(3, 6).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2]
                arregloVSaliente = []
                for i in range(2):
                    item = float(self.ui.matriz.item(i+2,4).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                variableSaliente = min(arregloVSaliente)
                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')
                    
            elif numMayor == arrayZj[3]:
                 #Encontramos la variable entrante
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, S2')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 6).text())
                bi2 = float(self.ui.matriz.item(3, 6).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2]
                arregloVSaliente = []
                for i in range(2):
                    item = float(self.ui.matriz.item(i+2,5).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                variableSaliente = min(arregloVSaliente)
                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')
                    

    
    #Mostrar datos de Variable Entrante y saliente por tabla actual 3 restricciones
    def datos_tabla_actual_2r(self):
        arrayZ = []
        for i in range(5):
            itemsZ = float(self.ui.matriz.item(6,i+2).text())
            arrayZ.append(itemsZ)
        

        if arrayZ[0] <= 0 and arrayZ[1] <= 0 and arrayZ[2] <= 0 and arrayZ[3] <= 0 and arrayZ[4] <= 0:
            print("El programa ha finalizado desde datos_tabla_actual_2r")
            resultado1 = self.ui.matriz.item(2,1).text()
            resultado2 = self.ui.matriz.item(3,1).text()
            resultado3 = self.ui.matriz.item(4,1).text()
            arregloBi = []
            for b in range(4):
                item = float(self.ui.matriz.item(b+2,7).text())
                arregloBi.append(item)
            self.ui.label_varEntra.setText(f'  {resultado1} = {"{:.1f}".format(arregloBi[0])}')
            self.ui.label_varSale.setText(f'  {resultado2} = {"{:.1f}".format(arregloBi[1])}')
            self.ui.valorZ.setText(f'  {resultado3} = {"{:.1f}".format(arregloBi[2])}')
            self.ui.valorZ3.setText(f'  Z = {arregloBi[3]}')
            self.show_dialog()
           
            self.ui.mostrar.setEnabled(False)
            self.ui.calcular.setEnabled(False)
            self.ui.nuevo.setEnabled(True)
            self.ui.imprimir.setEnabled(True)
            #Regresamos el contador a 0
            self.contador = 0
        else:
            self.ui.nuevo.setEnabled(True)
            self.ui.calcular.setEnabled(True)
            
           
            arrayZj = []
            for m in range(5):
                itemZj = self.ui.matriz.item(6,m+2)
                Zj = float(itemZj.text())
                arrayZj.append(Zj) 
            
            numMayor = max(arrayZj)
           

            if numMayor == arrayZj[0]:
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, X1')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 7).text())
                bi2 = float(self.ui.matriz.item(3, 7).text())
                bi3 = float(self.ui.matriz.item(4, 7).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2,bi3]
                arregloVSaliente = []
                for i in range(3):
                    item = float(self.ui.matriz.item(i+2,2).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                variableSaliente = min(arregloVSaliente)
                
                
                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')
                
                if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                    valor = self.ui.matriz.item(4,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[2])}, {valor}')
                    

            elif numMayor == arrayZj[1]:
                #Encontramos la variable entrante
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, X2')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 7).text())
                bi2 = float(self.ui.matriz.item(3, 7).text())
                bi3 = float(self.ui.matriz.item(4, 7).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2,bi3]
                arregloVSaliente = []
                for i in range(3):
                    item = float(self.ui.matriz.item(i+2,3).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                    
                variableSaliente = min(arregloVSaliente)
                print(arregloVSaliente)
                print(variableSaliente)
                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')

                if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                    valor = self.ui.matriz.item(4,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[2])}, {valor}')
                    

            elif numMayor == arrayZj[2]:
                 #Encontramos la variable entrante
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, S1')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 7).text())
                bi2 = float(self.ui.matriz.item(3, 7).text())
                bi3 = float(self.ui.matriz.item(4, 7).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2,bi3]
                arregloVSaliente = []
                for i in range(3):
                    item = float(self.ui.matriz.item(i+2,4).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                variableSaliente = min(arregloVSaliente)
                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')
                
                if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                    valor = self.ui.matriz.item(4,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[2])}, {valor}')
                    
            elif numMayor == arrayZj[3]:
                 #Encontramos la variable entrante
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, S2')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 7).text())
                bi2 = float(self.ui.matriz.item(3, 7).text())
                bi3 = float(self.ui.matriz.item(4, 7).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2,bi3]
                arregloVSaliente = []
                for i in range(3):
                    item = float(self.ui.matriz.item(i+2,5).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                variableSaliente = min(arregloVSaliente)
                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')

                if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                    valor = self.ui.matriz.item(4,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[2])}, {valor}')

            elif numMayor == arrayZj[4]:
                self.ui.label_varEntra.setText(f'El número de la variable entrante es {"{:.3f}".format(numMayor)}, S3')
                
                #Encontramos la variable saliente
                bi1 = float(self.ui.matriz.item(2, 7).text())
                bi2 = float(self.ui.matriz.item(3, 7).text())
                bi3 = float(self.ui.matriz.item(4, 7).text())
                arrayCeldas = []
                arrayBi = [bi1,bi2,bi3]
                arregloVSaliente = []
                for i in range(3):
                    item = float(self.ui.matriz.item(i+2,6).text())
                    arrayCeldas.append(item)
                    if item == 0:
                        print("No se divide para 0")
                    else:
                        resultado = arrayBi[i]/item
                        if resultado > 0:
                            arregloVSaliente.append(resultado)
                variableSaliente = min(arregloVSaliente)

                
                #Determinamos si la variable saliente es S1 o S2
                if variableSaliente*arrayCeldas[0] == arrayBi[0]:
                    valor = self.ui.matriz.item(2,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[0])}, {valor}')
                    
                if variableSaliente*arrayCeldas[1] == arrayBi[1]:
                    valor = self.ui.matriz.item(3,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[1])}, {valor}')
                
                if variableSaliente*arrayCeldas[2] == arrayBi[2]:
                    valor = self.ui.matriz.item(4,1).text()
                    self.ui.label_varSale.setText(f'El número de la variable saliente es: {"{:.3f}".format(arrayBi[2])}, {valor}')
    #Funvion para el boton nuevo
    def nuevo(self):
        self.ui.label_funObj.setText("")
        self.ui.label_varSale.setText("")
        self.ui.label_varEntra.setText("")
        self.ui.numRestricciones.setValue(2)
        self.ui.tablaRestriccion.clearContents()
        self.ui.tablaRestriccion.setRowCount(0)
        self.ui.tablaRestriccion.setColumnCount(0)
        self.ui.matriz.clearContents()
        self.ui.matriz.setRowCount(0)
        self.ui.matriz.setColumnCount(0)
        self.ui.label_iterador.setText("")
        self.ui.funObjX1.setPlainText("")
        self.ui.funObjX2.setPlainText("")
        self.ui.valorZ.setText("")
        self.ui.valorZ3.setText("")


        self.ui.mostrar.setEnabled(True)
        self.ui.imprimir.setEnabled(True)     

        self.ui.nuevo.setEnabled(False)
        
        
       

    #║Mostrar datos en la tabla
    def mostrarDatos(self):
        try:
            
            numRestriccion = int(self.ui.numRestricciones.value())
            
            
            
            
            if numRestriccion == 1:
                
                rest1X1 = float(self.ui.tablaRestriccion.item(0, 0).text())
                rest1X2 = float(self.ui.tablaRestriccion.item(0, 1).text())
                rest1Result = float(self.ui.tablaRestriccion.item(0, 3).text())

                funObX1 = self.ui.funObjX1.toPlainText()
                funObX2 = self.ui.funObjX2.toPlainText()
                
            
            elif numRestriccion == 2:
                
                rest1X1 = float(self.ui.tablaRestriccion.item(0, 0).text())
                rest1X2 = float(self.ui.tablaRestriccion.item(0, 1).text())
                rest1Result = float(self.ui.tablaRestriccion.item(0, 3).text())

                rest2X1 = float(self.ui.tablaRestriccion.item(1, 0).text())
                rest2X2 = float(self.ui.tablaRestriccion.item(1, 1).text())
                rest2Result = float(self.ui.tablaRestriccion.item(1, 3).text())

                funObX1 = float(self.ui.funObjX1.toPlainText())
                funObX2 = float(self.ui.funObjX2.toPlainText())

                #Agregar datos a la matriz
                #Fila 0
                self.ui.matriz.setItem(0,0, QTableWidgetItem(" "))
                self.ui.matriz.setItem(0,1, QTableWidgetItem("Cj"))
                self.ui.matriz.setItem(0,2, QTableWidgetItem(str(funObX1)))
                self.ui.matriz.setItem(0,3, QTableWidgetItem(str(funObX2)))
                self.ui.matriz.setItem(0,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(0,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(0,6, QTableWidgetItem(" "))
                #Fila 1
                self.ui.matriz.setItem(1,0, QTableWidgetItem("Cb"))
                self.ui.matriz.setItem(1,1, QTableWidgetItem("Xb"))
                self.ui.matriz.setItem(1,2, QTableWidgetItem("X1"))
                self.ui.matriz.setItem(1,3, QTableWidgetItem("X2")) 
                self.ui.matriz.setItem(1,4, QTableWidgetItem("S1")) 
                self.ui.matriz.setItem(1,5, QTableWidgetItem("S2")) 
                self.ui.matriz.setItem(1,6, QTableWidgetItem("Bi")) 
                #Fila 2
                self.ui.matriz.setItem(2,0, QTableWidgetItem("0"))
                self.ui.matriz.setItem(2,1, QTableWidgetItem("S1"))
                self.ui.matriz.setItem(2,2, QTableWidgetItem(str(rest1X1)))
                self.ui.matriz.setItem(2,3, QTableWidgetItem(str(rest1X2)))
                self.ui.matriz.setItem(2,4, QTableWidgetItem("1"))
                self.ui.matriz.setItem(2,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(2,6, QTableWidgetItem(str(rest1Result)))
                #Fila 3
                self.ui.matriz.setItem(3,0, QTableWidgetItem("0"))
                self.ui.matriz.setItem(3,1, QTableWidgetItem("S2"))
                self.ui.matriz.setItem(3,2, QTableWidgetItem(str(rest2X1)))
                self.ui.matriz.setItem(3,3, QTableWidgetItem(str(rest2X2)))
                self.ui.matriz.setItem(3,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(3,5, QTableWidgetItem("1"))
                self.ui.matriz.setItem(3,6, QTableWidgetItem(str(rest2Result)))
                
                #Fila 4
                self.ui.matriz.setItem(4,0, QTableWidgetItem(" "))
                self.ui.matriz.setItem(4,1, QTableWidgetItem("Zj"))
                self.ui.matriz.setItem(4,2, QTableWidgetItem("0"))
                self.ui.matriz.setItem(4,3, QTableWidgetItem("0"))
                self.ui.matriz.setItem(4,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(4,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(4,6, QTableWidgetItem("0"))
                
                #Fila 5
                self.ui.matriz.setItem(5,0, QTableWidgetItem(" "))
                self.ui.matriz.setItem(5,1, QTableWidgetItem("Cj-Zj"))
                self.ui.matriz.setItem(5,2, QTableWidgetItem(str(funObX1)))
                self.ui.matriz.setItem(5,3, QTableWidgetItem(str(funObX2)))
                self.ui.matriz.setItem(5,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(5,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(5,6, QTableWidgetItem(" "))

                #Mostrar Funicion objetivo e iterador

                self.ui.label_funObj.setText(f'Z = {"{:.0f}".format(funObX1)}X1 + {"{:.0f}".format(funObX2)}X2')
                self.ui.label_iterador.setText("0")
                
                
                self.datos_tabla_actual()
                
                

            elif numRestriccion ==3:
                rest1X1 = self.ui.tablaRestriccion.item(0, 0).text()
                rest1X2 = self.ui.tablaRestriccion.item(0, 1).text()
                rest1Result = self.ui.tablaRestriccion.item(0, 3).text()

                rest2X1 = self.ui.tablaRestriccion.item(1, 0).text()
                rest2X2 = self.ui.tablaRestriccion.item(1, 1).text()
                rest2Result = self.ui.tablaRestriccion.item(1, 3).text()

                rest3X1 = self.ui.tablaRestriccion.item(2, 0).text()
                rest3X2 = self.ui.tablaRestriccion.item(2, 1).text()
                rest3Result = self.ui.tablaRestriccion.item(2, 3).text()

                funObX1 = float(self.ui.funObjX1.toPlainText())
                funObX2 = float(self.ui.funObjX2.toPlainText())

                #Agregamos los datos a la matriz
                #Fila 0
                self.ui.matriz.setItem(0,0, QTableWidgetItem(" "))
                self.ui.matriz.setItem(0,1, QTableWidgetItem("Cj"))
                self.ui.matriz.setItem(0,2, QTableWidgetItem(str(funObX1)))
                self.ui.matriz.setItem(0,3, QTableWidgetItem(str(funObX2)))
                self.ui.matriz.setItem(0,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(0,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(0,6, QTableWidgetItem("0"))
                self.ui.matriz.setItem(0,7, QTableWidgetItem(" "))
                #Fila 1
                self.ui.matriz.setItem(1,0, QTableWidgetItem("Cb"))
                self.ui.matriz.setItem(1,1, QTableWidgetItem("Xb"))
                self.ui.matriz.setItem(1,2, QTableWidgetItem("X1"))
                self.ui.matriz.setItem(1,3, QTableWidgetItem("X2")) 
                self.ui.matriz.setItem(1,4, QTableWidgetItem("S1")) 
                self.ui.matriz.setItem(1,5, QTableWidgetItem("S2")) 
                self.ui.matriz.setItem(1,6, QTableWidgetItem("S3")) 
                self.ui.matriz.setItem(1,7, QTableWidgetItem("Bi")) 
                #Fila 2
                self.ui.matriz.setItem(2,0, QTableWidgetItem("0"))
                self.ui.matriz.setItem(2,1, QTableWidgetItem("S1"))
                self.ui.matriz.setItem(2,2, QTableWidgetItem(rest1X1))
                self.ui.matriz.setItem(2,3, QTableWidgetItem(rest1X2))
                self.ui.matriz.setItem(2,4, QTableWidgetItem("1"))
                self.ui.matriz.setItem(2,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(2,6, QTableWidgetItem("0"))
                self.ui.matriz.setItem(2,7, QTableWidgetItem(rest1Result))
                #Fila 3
                self.ui.matriz.setItem(3,0, QTableWidgetItem("0"))
                self.ui.matriz.setItem(3,1, QTableWidgetItem("S2"))
                self.ui.matriz.setItem(3,2, QTableWidgetItem(rest2X1))
                self.ui.matriz.setItem(3,3, QTableWidgetItem(rest2X2))
                self.ui.matriz.setItem(3,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(3,5, QTableWidgetItem("1"))
                self.ui.matriz.setItem(3,6, QTableWidgetItem("0"))
                self.ui.matriz.setItem(3,7, QTableWidgetItem(rest2Result))
                #Fila 4
                self.ui.matriz.setItem(4,0, QTableWidgetItem("0"))
                self.ui.matriz.setItem(4,1, QTableWidgetItem("S3"))
                self.ui.matriz.setItem(4,2, QTableWidgetItem(rest3X1))
                self.ui.matriz.setItem(4,3, QTableWidgetItem(rest3X2))
                self.ui.matriz.setItem(4,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(4,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(4,6, QTableWidgetItem("1"))
                self.ui.matriz.setItem(4,7, QTableWidgetItem(rest3Result))
                
                #Fila 5
                self.ui.matriz.setItem(5,0, QTableWidgetItem(" "))
                self.ui.matriz.setItem(5,1, QTableWidgetItem("Zj"))
                self.ui.matriz.setItem(5,2, QTableWidgetItem("0"))
                self.ui.matriz.setItem(5,3, QTableWidgetItem("0"))
                self.ui.matriz.setItem(5,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(5,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(5,6, QTableWidgetItem("0"))
                self.ui.matriz.setItem(5,7, QTableWidgetItem("0"))
                #Fila 6
                self.ui.matriz.setItem(6,0, QTableWidgetItem(" "))
                self.ui.matriz.setItem(6,1, QTableWidgetItem("Cj-Zj"))
                self.ui.matriz.setItem(6,2, QTableWidgetItem(str(funObX1)))
                self.ui.matriz.setItem(6,3, QTableWidgetItem(str(funObX2)))
                self.ui.matriz.setItem(6,4, QTableWidgetItem("0"))
                self.ui.matriz.setItem(6,5, QTableWidgetItem("0"))
                self.ui.matriz.setItem(6,6, QTableWidgetItem("0"))
                self.ui.matriz.setItem(6,7, QTableWidgetItem(" "))

                #Mostrar Funicion objetivo e iterador

                self.ui.label_funObj.setText(f'Z = {"{:.0f}".format(funObX1)}X1 + {"{:.0f}".format(funObX2)}X2')
                self.ui.label_iterador.setText("0")
                
                
                self.datos_tabla_actual_2r()
        except:
            self.show_alert()                
        
    #Funcion Agregar un Combo Box en la celda
    def addCombo(self, restriccion):
        fila = 0
        columna = 2
        for i in range(restriccion):
            comboBox = QComboBox()
            comboBox.addItem("<=")
            comboBox.addItem(">=")
            self.ui.tablaRestriccion.setCellWidget(fila, columna, comboBox)

            fila +=1

    #Generar modelo
    def generarModelo(self):
        
        numRestriccion = int(self.ui.numRestricciones.value())
        
      
        if numRestriccion == 1:
            self.ui.tablaRestriccion.setRowCount(numRestriccion)
            self.ui.tablaRestriccion.setColumnCount(4)
            self.columnLabels = ["X1","X2","",""]
            self.ui.tablaRestriccion.setHorizontalHeaderLabels(self.columnLabels)
            self.rowLabels = ["®"]
            self.ui.tablaRestriccion.setVerticalHeaderLabels(self.rowLabels)
            self.ui.tablaRestriccion.resizeColumnsToContents()
            
            #Matrix1
            self.ui.matriz.setRowCount(5)
            self.ui.matriz.setColumnCount(6)
            self.columnLabels = ["","","","","",""]
            self.ui.matriz.setHorizontalHeaderLabels(self.columnLabels)
            self.rowLabels = ["","","","",""]
            self.ui.matriz.setVerticalHeaderLabels(self.rowLabels)
            self.ui.matriz.resizeColumnsToContents()
            #Agregar un Combo Box en la celda
            self.addCombo(numRestriccion)
            

        elif numRestriccion ==2:
            self.ui.tablaRestriccion.setRowCount(numRestriccion)
            self.ui.tablaRestriccion.setColumnCount(4)
            self.columnLabels = ["X1","X2","",""]
            self.ui.tablaRestriccion.setHorizontalHeaderLabels(self.columnLabels)
            self.rowLabels = ["®","®"]
            self.ui.tablaRestriccion.setVerticalHeaderLabels(self.rowLabels) 
            self.ui.tablaRestriccion.resizeColumnsToContents()
            
            #Agregar un Combo Box en la celda
            self.addCombo(numRestriccion)

             #Matrix2
            self.ui.matriz.setRowCount(6)
            self.ui.matriz.setColumnCount(7)
            self.columnLabels = ["","","","","","",""]
            self.ui.matriz.setHorizontalHeaderLabels(self.columnLabels)
            self.rowLabels = ["","","","","",""]
            self.ui.matriz.setVerticalHeaderLabels(self.rowLabels)
            self.ui.matriz.resizeColumnsToContents()
            self.ui.matriz.setEditTriggers(QAbstractItemView.NoEditTriggers)
            

        elif numRestriccion == 3:
            self.ui.tablaRestriccion.setRowCount(numRestriccion)
            self.ui.tablaRestriccion.setColumnCount(4)
            self.columnLabels = ["X1","X2","",""]
            self.ui.tablaRestriccion.setHorizontalHeaderLabels(self.columnLabels)
            self.rowLabels = ["®","®","®"]
            self.ui.tablaRestriccion.setVerticalHeaderLabels(self.rowLabels) 
            self.ui.tablaRestriccion.resizeColumnsToContents()            
            #Agregar un Combo Box en la celda
            self.addCombo(numRestriccion)
            

             #Matrix3
            self.ui.matriz.setRowCount(7)
            self.ui.matriz.setColumnCount(8)
            self.columnLabels = ["","","","","","","",""]
            self.ui.matriz.setHorizontalHeaderLabels(self.columnLabels)
            self.rowLabels = ["","","","","","",""]
            self.ui.matriz.setVerticalHeaderLabels(self.rowLabels)
            self.ui.matriz.resizeColumnsToContents()
            self.ui.matriz.setEditTriggers(QAbstractItemView.NoEditTriggers)

# if __name__ == "__main__":
#     app =  QApplication([])
#     GUI = Simplex()
#     GUI.show()
#     sys.exit(app.exec_())