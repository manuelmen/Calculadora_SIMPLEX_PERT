from PyQt5.QtWidgets import *
from interfaz.ui_METODOSIMPLEX import Ui_MainWindow
from PyQt5.QtGui import QIcon, QColor
import calendar
from PyQt5 import QtGui
from datetime import datetime, timedelta
from math import *
import sys, re

class Pert(QMainWindow):


    def __init__(self, ui, icono):
        super(Pert, self).__init__()
        self.ui = ui
        self.icono = icono
        self.setWindowIcon(QIcon(self.icono))
     #Configuracion de Widgets
     #║Icono de las alertas
        # self.setWindowIcon(QIcon(self.icono))
        self.ui.numeroActividad.setMinimum(1)
        self.ui.numeroActividad.setMaximum(27)
        # print(list(calendar.day_name))
        #DESHABILITAR BOTONES DE INICIO
        # self.ui.nuevoModelo.setEnabled(False)
        self.ui.anterior.setEnabled(False)
        self.ui.siguiente.setEnabled(False)
        #Ocultar Widget de resultados
        self.ui.widgetT2.setVisible(False)


      #Eventos metodo Pert
        self.ui.generar.clicked.connect(self.generar_tabla_1)
        self.ui.siguiente.clicked.connect(self.siguiente)
        self.ui.anterior.clicked.connect(self.anterior)
        self.ui.salirPert.clicked.connect(self.salir_pert)
        self.ui.nuevoModelo.clicked.connect(self.btn_nuevo)
        self.ui.calcular_fechas.clicked.connect(self.generar_fechas)
      

    #Funciones
    #Salir de Pert
    def salir_pert(self):
        reply = QMessageBox.question(self, "Salir", "¿Seguro quiere salir de Pert?", QMessageBox.Yes, QMessageBox.No)
  
        if reply == QMessageBox.Yes:
            self.ui.widgetP.setVisible(False)
            self.ui.frame_2.setVisible(True)
        else:
            print("Ventana no se cerro")
    #Generar tabla 1
    def generar_tabla_1(self):

        self.num_actividad = int(self.ui.numeroActividad.value())
        self.ui.tabla1.setRowCount(self.num_actividad)
        self.ui.tabla1.horizontalHeader().setStyleSheet("font-size:12px;font: bold")
        self.ui.tabla1.verticalHeader().setVisible(False)
        self.ui.tabla1.resizeColumnsToContents()
        self.ui.tabla1.setColumnCount(5)
        
                
        # self.ui.tabla1.setStyleSheet("font-size: 14px")
        
        self.header = ["Actividades", "Predecesora", "To", "Tn", "Tp"]

        self.arrayActividades = ["A","B","C","D","E","F","G","H","I","J","K",
                                "L","M","N","Ñ","O","P","Q","R","S","T","U",
                                "V","W","X","Y","Z",]
        
        # Bucle: Asigna nombre a los encabezados
        for indice, ancho in enumerate((104, 104, 75, 75, 75), start=0):
            self.ui.tabla1.setColumnWidth(indice, ancho)
            item = QTableWidgetItem(self.header[indice])
            # item.setBackground(QtGui.QColor(22, 20, 90))
            self.ui.tabla1.setHorizontalHeaderItem(indice, item)

        #COLOCAR LETRAS SEGUN NUMERO DE ACTIVIDADES
        for i in range(self.num_actividad):
            self.ui.tabla1.setItem(i,0, QTableWidgetItem(self.arrayActividades[i]))
        #Activar boton Siguiente
        self.ui.siguiente.setEnabled(True)
            
    #Funcion Siguiente para la otra tabla
    def siguiente(self):

        #Recorre la tabla desde la columna 2 a la 4 y la fila 0 hasta num_actividades-1
        # print(self.num_actividad)

        self.predecesores = self.validar_predecesores()
        #Array padre
        self.array_tabla_1 = []
        #############Arrays hijos######
        #columna 2
        try:
            for i in range(self.num_actividad):
                data = []
                
                item2 = int(self.ui.tabla1.item(i,2).text())
                item3 = int(self.ui.tabla1.item(i,3).text())
                item4 = int(self.ui.tabla1.item(i,4).text())
                data.append(item2)
                data.append(item3)
                data.append(item4)
                self.array_tabla_1.append(data)
        except:
            self.show_dialog()

        if len(self.predecesores) == self.num_actividad and len(self.array_tabla_1) == self.num_actividad:
            #Validar si se trabajan sabado o domingo
            sabado = self.ui.sabado_2.isChecked()
            domingo = self.ui.domingo_2.isChecked()
            if sabado == True and domingo == True:                              
           
                self.ui.widgetT2.setVisible(True)
                self.ui.anterior.setEnabled(True)
                self.ui.siguiente.setEnabled(False)
                self.ui.groupBox_6.setEnabled(False)
                self.ui.numeroActividad.setEnabled(False)
                self.ui.generar.setEnabled(False)

                #Funcion que saca el valor de Dij
                self.sacar_Dij()
            elif sabado == True:
                print("Debe seleccionar sabado y domingo o ninguno para continuar")
                self.show_dialog_fin_d()
            elif domingo == True:
                print("Debe seleccionar sabado y domingo o ninguno para continuar")
                self.show_dialog_fin_d()
            else:
                self.ui.widgetT2.setVisible(True)
                self.ui.anterior.setEnabled(True)
                self.ui.siguiente.setEnabled(False)
                self.ui.groupBox_6.setEnabled(False)
                self.ui.numeroActividad.setEnabled(False)
                self.ui.generar.setEnabled(False)

                #Funcion que saca el valor de Dij
                self.sacar_Dij()
    ##Funcion para boton de Anterior
    def anterior(self):
        self.ui.widgetT2.setVisible(False)
        self.ui.siguiente.setEnabled(True)
        self.ui.anterior.setEnabled(False)

    ##Alerta de Validacion
    def show_dialog(self):
        QMessageBox.warning(self, "Error de Datos", "Ingrese solo números para To, Tn y Tp.")

    ##Alerta de Validacion
    def show_dialog_mayuscula(self):
        QMessageBox.warning(self, "Error de Datos", "Ingresó un predecesor incorrecto.")

    ##Alerta de Validacion
    def show_dialog_predecesor(self):
        QMessageBox.warning(self, "Error de Datos", "Si no tiene predecesor ingrese un guion (-), de lo contrario letras de la A a la Z.")
##Alerta de Validacion
    def show_dialog_fin_d(self):
        QMessageBox.warning(self, "Error de Datos", "Debe elegir sábado y domingo o ninguno para continuar.")
      #Funcion para validar predecesores   
    def validar_predecesores(self):
        array_predecesores = []
        #############Arrays hijos######
        #columna 2
        try:
            contador = 0
            for i in range(self.num_actividad):
                
                data = []
                
                item2 = str(self.ui.tabla1.item(i,1).text())
                # resoult = 
                # print(R)
                #Validamos que los predecesores sean correctos
                if re.search(r"-|^[A-Z]{1}$|^[A-Z]{1}(,[A-Z]{1}){1,10}$", item2) :                
                    data.append(item2)                
                    array_predecesores.append(data)
                else:
                    contador +=1

            if contador > 0:
                self.show_dialog_mayuscula()

        except:        
            self.show_dialog_predecesor()
        return array_predecesores

    #Sacamos los valores de cada Dij
    def sacar_Dij(self):
        
        #Recorremos la tabla para sacar Dij con la formula
        self.array_Dij = []
        for i in range(self.num_actividad):
            to = int(self.ui.tabla1.item(i,2).text())
            tn = int(self.ui.tabla1.item(i,3).text()) 
            tp = int(self.ui.tabla1.item(i,4).text()) 

            #Encontramos Dij
            Dij = ceil((to+4*tn+tp)/6)
            self.array_Dij.append(str(Dij))
        # print(self.array_Dij)
        #Creamos la segunda tabla a mostrar
        self.generar_tabla_2(self.array_Dij)

    #Creamos la nueva tabla 2
    def generar_tabla_2(self, array_Dij):
        #creamos las filas y columnas
        self.num_actividad = int(self.ui.numeroActividad.value())
        self.ui.tabla2.setRowCount(self.num_actividad)
        self.ui.tabla2.horizontalHeader().setStyleSheet("font-size:10px;font: bold")
        self.ui.tabla2.verticalHeader().setVisible(False)
        self.ui.tabla2.resizeColumnsToContents()
        self.ui.tabla2.setColumnCount(11)
        # print(self.array_Dij)

        header_t2 = ['Actividades','Dij','Ti0','Ti1','Tj0','Tj1','MTij',
                    'Fecha de Inicio Temprano','Fecha de Inicio Tardío','Fecha de Fin Temprano','Fecha de Fin Tardío']
        # Bucle: Asigna nombre a los encabezados
        for indice, ancho in enumerate((80, 35, 35, 35, 35, 35, 40, 125, 110, 110, 105), start=0):
            self.ui.tabla2.setColumnWidth(indice, ancho)
            item = QTableWidgetItem(header_t2[indice])
            # item.setBackground(QtGui.QColor(22, 20, 90))
            self.ui.tabla2.setHorizontalHeaderItem(indice, item)
        #COLOCAR LETRAS SEGUN NUMERO DE ACTIVIDADES
        for i in range(self.num_actividad):
            self.ui.tabla2.setItem(i,0, QTableWidgetItem(self.arrayActividades[i]))
            self.ui.tabla2.setItem(i,1, QTableWidgetItem(array_Dij[i]))
        

        #LLenamos la tabla 2
        
        for t in range(len(self.predecesores)):
            if self.predecesores[t][0] == "-":
                self.ui.tabla2.setItem(t,2, QTableWidgetItem("0"))
                self.ui.tabla2.setItem(t,4, QTableWidgetItem(str(array_Dij[t])))
            else:
                self.predecesor_separado = self.predecesores[t][0].split(sep=',')
               
                #Valor que contendra la posicion de los precedentes que dependan de las actividades para extraer el valor Tj0
                valor = []
                for i in range(len(self.predecesor_separado)):
                    v = self.arrayActividades.index(self.predecesor_separado[i])
                    valor.append(int(v))
                
                array_maximo = []
                for m in range (len(valor)):
                    cantidad = int(self.ui.tabla2.item(valor[m],4).text())
                    array_maximo.append(cantidad)
                valor_maximo = max(array_maximo)
                #•Agregamos el valor a Ti0
                self.ui.tabla2.setItem(t,2,QTableWidgetItem(str(valor_maximo)))
                #Agregamos el nuevo valor a Tj0
                valor_tj0 = valor_maximo + int(array_Dij[t])
                self.ui.tabla2.setItem(t,4,QTableWidgetItem(str(valor_tj0)))
                
        contador_mensaje = 0
        for r in range(int(self.num_actividad)-1, -1, -1):
            # print(r)
            if r == int(self.num_actividad)-1:
                self.fin_proyecto = self.ui.tabla2.item(r,4).text()
                self.ui.tabla2.setItem(r,5,QTableWidgetItem(self.fin_proyecto))
                Ti1 = int(self.fin_proyecto)-int(array_Dij[r])
                self.ui.tabla2.setItem(r,3,QTableWidgetItem(str(Ti1)))
              
            else:
                #Capturamos los valores dela actividad actual
                          
                item = self.ui.tabla2.item(r,0).text()
                self.actividad_actual =  item
                
                
               #☺ Separamos nuevamente las "," de los predecesores Y los guardamos en diccionario 
                diccionario = {}
                for p in range(int(self.num_actividad)):
                    item2 = self.ui.tabla1.item(p,1).text().split(sep=',')
                    # self.predecesor_separado2 = self.predecesores[r][0].split(sep=',')
                    # self.array_predecesor_actual.append(item2)
                    diccionario[p] = item2
              
                #CREAMOS UN ARRAY DONDE GUARDAREMOS LA DIRECCION DE LOS PREDECESORES
                valor2 = []                
                for p in diccionario:
                    try:
                        # v = self.array_predecesor_actual[p].index(self.actividad_actual)
                        #µ a[a.index('s')]
                        v = int(diccionario[p].index(self.actividad_actual))
                        if v >= 0:
                            llave = p                    
                            valor2.append(llave)
                    except:
                        if contador_mensaje == 0: 
                            print("No esta en lista")
                            contador_mensaje += 1
                        

               
                #Valor 2 tiene la direccion de las actividades que son predecesoras
                # print(valor2)

                if len(valor2) == 0:
                    #Agregamos el valor del proyecto final em caso de que los precedetes no tengan esa actividad
                   self.ui.tabla2.setItem(r,5,QTableWidgetItem(self.fin_proyecto))
                   nuevo_valor = self.ui.tabla2.item(r,5).text()
                   ti1_nuevo = int(nuevo_valor)-int(array_Dij[r])
                   self.ui.tabla2.setItem(r,3,QTableWidgetItem(str(ti1_nuevo)))
                #    print("Se Agg")
                else:
                    #Sacamos el minimo de los precedentes que tengan a la actividad
                    array_minimo = []
                    for n in range (len(valor2)):
                        cantidad = int(self.ui.tabla2.item(valor2[n],3).text())
                        array_minimo.append(cantidad)
                    valor_minimo = min(array_minimo)
                    #Mandamos los valores a la tabla
                    self.ui.tabla2.setItem(r,5,QTableWidgetItem(str(valor_minimo)))
                    #Agregamos el nuevo valor a Tj0
                    valor_tj_0 = valor_minimo - int(array_Dij[r])
                    self.ui.tabla2.setItem(r,3,QTableWidgetItem(str(valor_tj_0)))
                    # print(r)

        #Ciclo para llenar la columna Mtij
        for m in range(int(self.num_actividad)):
            numero_1 = int(self.ui.tabla2.item(m,3).text())
            numero_2 = int(self.ui.tabla2.item(m,2).text())

            Mtij = numero_1 - numero_2

            #Colocamos el valor de MTij           
            
            if Mtij == 0:
                self.ui.tabla2.setItem(m,6,QTableWidgetItem(str(Mtij)))
                for c in range(7):
                    #Color a las filas
                    self.ui.tabla2.item(m,c).setBackground(QtGui.QColor(222,220,217))
                    # self.ui.tabla2.item(m,6).setBackground(QtGui.QColor(251,95,95))
            else:
                self.ui.tabla2.setItem(m,6,QTableWidgetItem(str(Mtij)))
           



        #Deshabilitamos la edicion de celdas
        self.ui.tabla2.setEditTriggers(QAbstractItemView.NoEditTriggers) 

        #Calcular fecha del actual y mostrarla
        #Fecha actual
        fecha = datetime.now()
        self.ui.fechaInicio.setDateTime(fecha)
    
    #Boton nuevo de la tabla
    def btn_nuevo(self):
        #Borramos todo lo de la tabla 2 y tabla 1
        self.ui.tabla2.clearContents()
        self.ui.tabla2.setRowCount(0)
        self.ui.tabla2.setColumnCount(0)
        self.ui.tabla1.clearContents()
        self.ui.tabla1.setRowCount(0)
        self.ui.tabla1.setColumnCount(0)
        #Colocamos el spinbox en 1 y lo habilitamos
        self.ui.numeroActividad.setValue(1)
        self.ui.numeroActividad.setEnabled(True)
        #Habilitar botones o deshabilitar
        self.ui.siguiente.setEnabled(False)
        self.ui.generar.setEnabled(True)
        self.ui.anterior.setEnabled(False)
        #Habilitamos el CheckBox
        self.ui.groupBox_6.setEnabled(True)
        self.ui.sabado_2.setCheckable(False)
        self.ui.domingo_2.setCheckable(False)
        self.ui.sabado_2.setCheckable(True)
        self.ui.domingo_2.setCheckable(True)
        #Ocultar Widget 2
        self.ui.widgetT2.setVisible(False)
    #Obtener fecha
    def generar_fechas(self):

        #Validar si se trabajan sabado o domingo
        self.sabado = self.ui.sabado_2.isChecked()
        self.domingo = self.ui.domingo_2.isChecked() 

        self.fecha_inicio = self.ui.fechaInicio.text()
        

        if self.sabado == True and self.domingo == True:
            #Comprobar si es sabado o domingo
            self.nueva_fecha = self.comprobar_fecha(self.fecha_inicio)
            # print(nueva_fecha)
            #Comprobar que las actividades sin predecesores inicien con la fecha elegida
            for a in range(int(self.num_actividad)):
                ##No tienen predecesores
                if self.predecesores[a][0] == "-":
                    #Mostramos la fecha en la tabla validando que no se trabaja sabado ni domingo
                    self.ui.tabla2.setItem(a,7,QTableWidgetItem(str(self.nueva_fecha.strftime("%d/%m/%Y"))))
                    self.ui.tabla2.setItem(a,8,QTableWidgetItem(str(self.nueva_fecha.strftime("%d/%m/%Y"))))

                    #ciclo para ir validando las fechas de terminacion sumando Dij y en base a que no se trabaja sabado ni domingoen base
                    f_nueva = self.nueva_fecha.strftime("%d/%m/%Y")
                    arreglo = []
                    c = 0
                    for o in range(int(self.array_Dij[a])):
                        # fecha_tabla = self.ui.tabla2.item(a,7).text()
                        
                        fecha_t = self.comprobar_fecha_2(f_nueva).strftime("%d/%m/%Y")
                        # print(fecha_t)
                        fecha = self.comprobar_fecha(fecha_t)
                        # print(fecha)
                        nueva = fecha
                                              
                        f_nueva = nueva.strftime("%d/%m/%Y")
                        arreglo.append(f_nueva)  
                        c += 1
                    # print(arreglo[c-2])
                    mtij_valor = int(self.ui.tabla2.item(a,6).text())
                    fecha_holgura = datetime.strptime(arreglo[c-2], "%d/%m/%Y")
                    fecha_mas_holgura = fecha_holgura + timedelta(days=mtij_valor)
                    self.ui.tabla2.setItem(a,9,QTableWidgetItem(arreglo[c-2]))
                    self.ui.tabla2.setItem(a,10,QTableWidgetItem(fecha_mas_holgura.strftime("%d/%m/%Y")))


                    #Faltan sacar las fechas de los que no tienen predecesores
                else:
                    #Separamos los predecesores en un array
                    self.predecesor_separado_fecha = self.predecesores[a][0].split(sep=',')
               
                #Valor que contendra la posicion de los precedentes que dependan de las actividades para extraer el valor Tj0
                    valor_fecha = []
                    for i in range(len(self.predecesor_separado_fecha)):
                        v = self.arrayActividades.index(self.predecesor_separado_fecha[i])
                        valor_fecha.append(int(v))
                    # print(valor_fecha)

                    #extraemos los valores de las fechas que encuentre
                    array_fechas = []
                    array_fecha_tardio = []
                    #ciclo para extraer las fechas
                    for fech in range(len(valor_fecha)):
                        item_fecha = self.ui.tabla2.item(valor_fecha[fech],9).text()
                        item_fecha2 = self.ui.tabla2.item(valor_fecha[fech],10).text()
                        #convertir en formato fecha
                        conv_fech = datetime.strptime(item_fecha, "%d/%m/%Y")
                        conv_fech2 = datetime.strptime(item_fecha2, "%d/%m/%Y")
                        #agg la fecha al array
                        array_fechas.append(conv_fech)
                        array_fecha_tardio.append(conv_fech2)

                    fecha_mayor = max(array_fechas) + timedelta(days=1)
                    fecha_mayor_tar = max(array_fecha_tardio) + timedelta(days=1)
                    #comprobar que no sea sabado o domingo
                    fecha_comp = self.comprobar_fecha(fecha_mayor.strftime("%d/%m/%Y"))
                    fecha_comp2 = self.comprobar_fecha(fecha_mayor_tar.strftime("%d/%m/%Y"))

                    #mostramos en tabla la fecha de inicio temprano y tardio
                    self.ui.tabla2.setItem(a,7,QTableWidgetItem(fecha_comp.strftime("%d/%m/%Y")))
                    #Fecha de inicio tardio
                    self.ui.tabla2.setItem(a,8,QTableWidgetItem(fecha_comp2.strftime("%d/%m/%Y")))
                    print(fecha_comp)
                    ###########
                    #ciclo para ir validando las fechas de terminacion sumando Dij y en base a que no se trabaja sabado ni domingoen base
                    f_nueva = fecha_comp.strftime("%d/%m/%Y")
                    arreglo = []
                    c = 0
                    for o in range(int(self.array_Dij[a])):
                        # fecha_tabla = self.ui.tabla2.item(a,7).text()
                        
                        fecha_t = self.comprobar_fecha_2(f_nueva).strftime("%d/%m/%Y")
                        # print(fecha_t)
                        fecha = self.comprobar_fecha(fecha_t)
                        # print(fecha)
                        nueva = fecha
                                              
                        f_nueva = nueva.strftime("%d/%m/%Y")
                        arreglo.append(f_nueva)  
                        c += 1
                    # print(arreglo[c-2])
                    mtij_valor = int(self.ui.tabla2.item(a,6).text())
                    dij = int(self.ui.tabla2.item(a,1).text())

                    suma_mti_dij = mtij_valor + dij
                    fecha_holgura = self.ui.tabla2.item(a,8).text()#, "%d/%m/%Y")

                    arreglo_tardio = []
                    arreglo_tardio.append(fecha_holgura)
                    cont = 0
                    for l in range(suma_mti_dij):
                        fecha_t = self.comprobar_fecha_2(fecha_holgura).strftime("%d/%m/%Y")
                        # print(fecha_t)
                        fecha = self.comprobar_fecha(fecha_t)
                        # print(fecha)
                        nueva = fecha
                                              
                        fecha_holgura = nueva.strftime("%d/%m/%Y")
                        arreglo_tardio.append(fecha_holgura)  
                        cont += 1
                  
                    #mostrar en la tabla
                    self.ui.tabla2.setItem(a,9,QTableWidgetItem(arreglo[c-2]))
                    self.ui.tabla2.setItem(a,10,QTableWidgetItem(arreglo_tardio[cont-1]))
                   
        else:
            
            for p in range(int(self.num_actividad)):
                if self.predecesores[p][0] == "-":
                    #Mostramos la fecha en la tabla validando que no se trabaja sabado ni domingo
                    self.ui.tabla2.setItem(p,7,QTableWidgetItem(self.fecha_inicio))
                    self.ui.tabla2.setItem(p,8,QTableWidgetItem(self.fecha_inicio))
                    ##Fechas tardio
                    dij = int(self.ui.tabla2.item(p,1).text())
                    mtij = int(self.ui.tabla2.item(p,6).text())

                    #Extraer la fecha de inicio para sumar los dij
                    item_fecha = datetime.strptime(self.fecha_inicio, "%d/%m/%Y")
                    fecha_fin = item_fecha + timedelta(days=dij-1)

                    holgura = (dij + mtij)-1
                    fecha_fin_2 = item_fecha + timedelta(days=holgura)
                    
                    #mostramos en tabla
                    self.ui.tabla2.setItem(p,9,QTableWidgetItem(fecha_fin.strftime("%d/%m/%Y")))
                    self.ui.tabla2.setItem(p,10,QTableWidgetItem(fecha_fin_2.strftime("%d/%m/%Y")))





                else:
                    #Separamos los predecesores en un array
                    self.predecesor_separado_fecha = self.predecesores[p][0].split(sep=',')
               
                #Valor que contendra la posicion de los precedentes que dependan de las actividades para extraer el valor Tj0
                    valor_fecha = []
                    for i in range(len(self.predecesor_separado_fecha)):
                        v = self.arrayActividades.index(self.predecesor_separado_fecha[i])
                        valor_fecha.append(int(v))
                    print(valor_fecha)
                    #array para almacenar las fechas de terminacion
                    array_fecha_t_1 = []
                    array_fecha_t_2 = []
                    #estraer el mayot
                    for m in range(len(valor_fecha)):
                        #extraemos fechas de la tabla
                        item1 = self.ui.tabla2.item(valor_fecha[m],9).text()
                        item2 = self.ui.tabla2.item(valor_fecha[m],10).text()
                        #conversion a tipò date
                        item_1_f = datetime.strptime(item1, "%d/%m/%Y")
                        item_2_f = datetime.strptime(item2, "%d/%m/%Y")
                        #agreggamos el array
                        array_fecha_t_1.append(item_1_f)
                        array_fecha_t_2.append(item_2_f)
                    #sacamos las fechas maximas 
                    max_fec_ter_tem = max(array_fecha_t_1) + timedelta(days=1)
                    max_fec_ter_tar = max(array_fecha_t_2) + timedelta(days=1)

                    #Mostramos en la tabla las nuevas fechas
                    self.ui.tabla2.setItem(p,7,QTableWidgetItem(max_fec_ter_tem.strftime("%d/%m/%Y")))
                    self.ui.tabla2.setItem(p,8,QTableWidgetItem(max_fec_ter_tar.strftime("%d/%m/%Y")))

                    ##Fechas tardio
                    dij = int(self.ui.tabla2.item(p,1).text())
                    mtij = int(self.ui.tabla2.item(p,6).text())

                    nueva_fecha_tardio = max_fec_ter_tem + timedelta(days=dij-1)

                    suma_holguras = dij + mtij 

                    nueva_fecha_tardio_2 = max_fec_ter_tar + timedelta(days=suma_holguras-1)

                    #Mostramos en la tabla las nuevas fechas
                    self.ui.tabla2.setItem(p,9,QTableWidgetItem(nueva_fecha_tardio.strftime("%d/%m/%Y")))
                    self.ui.tabla2.setItem(p,10,QTableWidgetItem(nueva_fecha_tardio_2.strftime("%d/%m/%Y")))


      #Comprobar si es sabado o domingo
    def comprobar_fecha(self, fechas):
        #comvertimos el string a formato de fecha
        fecha = datetime.strptime(fechas, "%d/%m/%Y")
        #validamos si la fecha es sabado o domingo
       
        if fecha.weekday() == 5 or fecha.weekday() == 6:
            #validamos que sea sabado
            if fecha.weekday() == 5:
                fecha = fecha + timedelta(days=2)
               
            # return fecha
                
            if fecha.weekday() == 6 :
                fecha = fecha + timedelta(days=1)
                
            # return fecha
                
        return fecha
      #Comprobar si es sabado o domingo
    def comprobar_fecha_2(self, fechas):
        #comvertimos el string a formato de fecha
        fecha = datetime.strptime(fechas, "%d/%m/%Y")
        #validamos si la fecha es sabado o domingo
       
        # print(fecha)
        fecha2 = fecha + timedelta(days=1)
        # print(fecha2)
                
        return fecha2


# if __name__ == "__main__":
#     app =  QApplication([])
#     app.setStyle(QStyleFactory.create('Fusion'))
#     GUI = Pert()
#     GUI.show()
#     sys.exit(app.exec_())