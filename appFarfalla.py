#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tkinter import Button, DoubleVar, Label, Entry, Frame, IntVar, Label, PhotoImage, StringVar, Tk, Toplevel, messagebox, ttk, Menu,Radiobutton
from tkinter.ttk import Combobox, Scrollbar, Separator, Treeview
from tkinter import Checkbutton, Listbox, TclError, Text, filedialog, messagebox
import sqlite3
import tkinter
from reportlab import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib import colors, styles
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, PageBreak, Image, Spacer,Paragraph, Table, TableStyle
from datetime import date
from time import strptime
import webbrowser
from tkinter.messagebox import showerror, showinfo
from math import ceil
import _tkinter
from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook
from numpy.lib import math
import smtplib,ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from os import remove
from _sqlite3 import Error, IntegrityError, OperationalError


class Farfalla:
#----------------Inicio---------------------------"""  """
	def __init__(self,principal):
		self.inicio=principal
		self.inicio.title('Farfalla')
		self.inicio.geometry('')#+500+50 ubicación de la ventana en la pantalla
		self.inicio.iconphoto(True,PhotoImage(file='mariposa2.png'))
		self.inicio.config(bg='#C3C3C3')
		self.inicio.state('zoomed')
		
		#Opciones de Menu
		barraMenu=Menu(inicio)
		inicio.config(menu=barraMenu, width=375, height=375)

		#tearoff separador inicial al desplegarce el menu
		nuevo=Menu(barraMenu, tearoff=0)
		nuevo.add_command(label='Compra',command=self.Compras)
		nuevo.add_command(label='Consumo Interno',command=self.Uso_interno)
		nuevo.add_command(label='Cliente', command=self.Clientes)
		nuevo.add_command(label='Pedidos', command=self.Pedidos)
		nuevo.add_command(label='Presupuesto', command=self.Presupuesto)
		nuevo.add_command(label='Producto',command=self.Producto)
		nuevo.add_command(label='Proveedor', command=self.Proveedor)
		barraMenu.add_cascade(label='Nuevo',menu=nuevo)
				
		archivoConfig=Menu(barraMenu, tearoff=0)
		archivoConfig.add_command(label='BackUp Base de datos', command=self.backup_BD)
		archivoConfig.add_command(label='Cuentas Bancarias', command=self.Cuentas)
		archivoConfig.add_command(label='Mail de email', command=self.Config_mail)
		archivoConfig.add_command(label='Medios de pago', command=self.Medios_pago)
		archivoConfig.add_command(label='Modificar cuerpo de mail', command=self.Modificar_cuerpo_mail)
		archivoConfig.add_command(label='Precio de Venta', command=self.Calculos)
		archivoConfig.add_command(label='Proveedores', command=self.Proveedor)
		archivoConfig.add_command(label='Recargo tarjetas', command=self.Recargos)
		archivoConfig.add_command(label='Tipo de comprobante', command=self.Tipo_comprobante)
		barraMenu.add_cascade(label='Configurar', menu=archivoConfig)

		archivoBusqueda=Menu(barraMenu,tearoff=0)
		archivoBusqueda.add_command(label='Informe stock',command=self.buscar_backup )
		archivoBusqueda.add_command(label='Comprobantes',command=self.Comprobantes )
		archivoBusqueda.add_command(label="PDF's",command=self.buscar_pdf )
		archivoBusqueda.add_command(label='Ventas', command=self.Buscar_pedidos)
		archivoBusqueda.add_command(label='Presupuestos', command=self.Buscar_presupuestos)
		archivoBusqueda.add_command(label='Productos',command=self.Buscador )
		archivoBusqueda.add_command(label='Usos internos',command=self.Busqueda_uso_interno )
		barraMenu.add_cascade(label='Busqueda', menu=archivoBusqueda)

		archivoEnviar=Menu(barraMenu,tearoff=0)
		archivoEnviar.add_command(label='Enviar',command=self.Enviar_adjuntos)
		barraMenu.add_cascade(label='Enviar', menu=archivoEnviar)

		#Datos productos
		self.id=StringVar()
		self.id.set('')
		self.id_producto=StringVar()
		self.id_producto.set('')
		self.codigo=StringVar()
		self.proveedor=StringVar()
		self.producto=StringVar()
		self.stock=IntVar()
		self.stock.set('')
		self.costo=DoubleVar()
		self.costo.set('')
		self.precio_venta=DoubleVar()
		self.precio_venta.set('')
		self.subtotal=DoubleVar()
		self.porcentaje_descuento=DoubleVar()
		self.descuento=DoubleVar()
		self.con_envio=IntVar()
		self.envio=DoubleVar()
		self.con_recargo=IntVar()
		self.recargo=DoubleVar()
		self.total_compra=DoubleVar()
		self.cant_pedido=IntVar()
		self.id_presupuesto=StringVar()
		self.cant_presupuesto=IntVar()
		self.cant_presupuesto.set('')
		self.total_presupuesto=DoubleVar()
		self.total_pedido=DoubleVar()

		#Lista de presupuestos sin confirmar
		self.presupuesto=StringVar()

		#Comprobantes
		self.cte=StringVar()
		self.nrocte=StringVar()
		self.fechacte=StringVar()
		
		#Medios de pago
		self.pagos=StringVar()

		#Valores de calculos
		self.porcentaje=DoubleVar()
		self.redondeo=DoubleVar()
		self.debito=DoubleVar(value=self.mostrar_recargo(tipo_tarjeta=1))
		self.credito=DoubleVar(value=self.mostrar_recargo(tipo_tarjeta=2))
			
		#Buscadores
		self.lista_publico=IntVar()
		self.buscarProducto=StringVar()
		self.buscador_usos=StringVar()
		self.buscarComprobante=StringVar()
		self.buscarPresupuesto=StringVar()
		self.buscarPedido=StringVar()
		self.buscarEstados=StringVar()
		self.opcion=IntVar()
		self.estado_presupuesto=IntVar()
		self.estado_pedido=IntVar()
		self.rango_periodos=StringVar()

		#Mails farfalla
		self.mail_principal=StringVar()
		self.contrasenha=StringVar()
		self.mail_activo=StringVar(value=self.mostrar_mail_master())
		self.opcion=IntVar()
		self.otros=StringVar()
		self.archivo=StringVar()
		
		#Datos personas/clientes
		self.proveedor=StringVar()
		self.cliente=StringVar()
		self.nombre=StringVar()
		self.apellido=StringVar()
		self.direccion=StringVar()
		self.telefono=StringVar()
		self.correo=StringVar()

		#Totales
		self.montoCompra=DoubleVar()
		self.total_cuentas=DoubleVar()
		self.ing_efec=DoubleVar()
		self.ing_trans=DoubleVar()
		self.ing_debit=DoubleVar()
		self.ing_cred=DoubleVar()
		self.egre_efec=DoubleVar()
		self.egre_tran=DoubleVar()
		self.egre_debit=DoubleVar()
		self.egre_cred=DoubleVar()
		self.ing_mercado=DoubleVar()
		self.egre_mercado=DoubleVar()
		
		#Cuenta bancaria
		self.cbu=StringVar()
		self.alias=StringVar()
		self.titular=StringVar()
		self.dni=StringVar()
		self.id_Tribut=StringVar()
		self.cuenta=StringVar()

	#--------------------Fecha-------------------------------
		self.actual=date.today()
		self.fecha='{}/{}/{}'.format(self.actual.day,self.actual.month,self.actual.year)
		self.periodo='{}/{}'.format(self.actual.month, self.actual.year)

	#------------------------Elementos de pantalla Inicio---------------------------------------------------
		self.logo=PhotoImage(file='./logo.png',)
		self.lInicio=Label(self.inicio, image=self.logo, bg='#C3C3C3',)
		self.lInicio.grid(row=0, column=0, padx=10, pady=10, rowspan=6)

		self.fechaInicio=Label(self.inicio, text=self.fecha,font=('Comic Sans MS', 10),bg='#C3C3C3',).grid(row=0, column=1, padx=10,pady=10)
		self.frameInicio=Frame()
		self.frameInicio.config(bg='#3BA684',relief="sunken")
		self.frameInicio.grid(row=1, column=1, padx=10, pady=10)

		self.botonBuscador=Button(self.frameInicio, text='Stock de \nproductos',width=12,command=self.Buscador, font=('Comic Sans MS', 10),fg='#3BA684', cursor='hand2')
		self.botonBuscador.bind('<Return>', self.Buscador)
		self.botonBuscador.grid(row=0, column=0,pady=10, padx=10,sticky='nsew')
		self.botonCompras=Button(self.frameInicio, text='Compras',width=12, font=('Comic Sans MS', 10),fg='#3BA684',cursor='hand2', command=self.Compras)
		self.botonCompras.bind('<Return>', self.Compras)
		self.botonCompras.grid(row=1, column=0, pady=10, padx=10,sticky='nsew')
		self.botonPresupuestos=Button(self.frameInicio, text='Presupuestos',width=12,font=('Comic Sans MS', 10),fg='#3BA684',cursor='hand2',command=self.Presupuesto)
		self.botonPresupuestos.bind('<Return>', self.Presupuesto )
		self.botonPresupuestos.grid(row=2, column=0, pady=10, padx=10,sticky='nsew')
		self.botonPedidos=Button(self.frameInicio, text='Ventas',width=12,font=('Comic Sans MS', 10),fg='#3BA684',cursor='hand2', command=self.Pedidos )
		self.botonPedidos.bind('<Return>', self.Pedidos)
		self.botonPedidos.grid(row=3, column=0, pady=10, padx=10,sticky='nsew')
		self.botonClientes=Button(self.frameInicio, text='Clientes',width=12,font=('Comic Sans MS', 10),fg='#3BA684',cursor='hand2', command=self.Clientes)
		self.botonClientes.bind('<Return>',self.Clientes)
		self.botonClientes.grid(row=5, column=0,pady=10, padx=10, sticky='nsew')
		self.botonProveedor=Button(self.frameInicio, text='Proveedor',width=12, font=('Comic Sans MS', 10),fg='#3BA684',cursor='hand2', command=self.Proveedor )
		self.botonProveedor.bind('<Return>', self.Proveedor)
		self.botonProveedor.grid(row=6, column=0, pady=10, padx=10,sticky='nsew')
		self.botonEstados=Button(self.frameInicio, text='Estados',width=12, font=('Comic Sans MS', 10),fg='#3BA684',cursor='hand2',command=self.Estados )
		self.botonEstados.bind('<Return>',self.Estados)
		self.botonEstados.grid(row=7, column=0, pady=10, padx=10,sticky='nsew')
		self.botonEstados_cuenta=Button(self.frameInicio, text='Estados\nde Cuentas',width=12, font=('Comic Sans MS', 10),fg='#3BA684',cursor='hand2',command=self.Estados_cuentas)
		self.botonEstados_cuenta.bind('<Return>',self.Estados_cuentas)
		self.botonEstados_cuenta.grid(row=8, column=0, pady=10, padx=10,sticky='nsew')
		#self.boton_extra=Button(self.frameInicio, image=self.logo,bg='#3BA684', cursor='hand2',command=self.Estados_cuentas,borderwidth=0,).grid(row=8, column=0) #Ejempro de boton con imagen

		#Seleccionar origen del programa
		self.ubicacion()
					
#----------------Ventana stock Productos------------
	def Buscador(self,event=None):
		self.ventanaBuscador=Toplevel()
		self.ventanaBuscador.title("Stock de productos")
		self.ventanaBuscador.geometry("+400+100")
		self.ventanaBuscador.config(bg='#C3C3C3')
		#self.ventanaBuscador.resizable(0,0)
		self.ventanaBuscador.transient(self.inicio)
		self.ventanaBuscador.grab_set()

		self.lbuscar=Label(self.ventanaBuscador, text='Buscar por producto',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=6, column=0, padx=3)
		self.entryBuscar=Entry(self.ventanaBuscador, textvariable=self.buscarProducto,font=('Comic Sans MS', 10))
		self.entryBuscar.focus()
		self.entryBuscar.bind('<Return>', self.buscadorProductos)
		self.entryBuscar.grid(row=7, column=0, padx=3, pady=3)
		self.entryBuscar.focus()
		self.botonBuscar=Button(self.ventanaBuscador, text='Buscar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.buscadorProductos)
		self.botonBuscar.bind('<Return>', self.buscadorProductos)
		self.botonBuscar.grid(row=7, column=1, padx=3, pady=3)
		self.botonModificar=Button(self.ventanaBuscador, text='Administrar artículos',font=('Comic Sans MS', 10),fg='#3BA684', command=self.admin_producto). grid(row=7, column=2, padx=3, pady=3)
		self.botonNuevo=Button(self.ventanaBuscador, text='Nuevo artículo',font=('Comic Sans MS', 10),fg='#3BA684', command=self.nuevo_articulo). grid(row=7, column=3, padx=3, pady=3)
	
		#Tabla (ventana stock)
		self.encabezado=['id','codigo','proveedor','producto','stock','costo','precio_venta']
		self.tabla=Treeview(self.ventanaBuscador, columns=self.encabezado, show='headings',)
		self.tabla.bind('<<TreeviewSelect>>',self.seleccionar_buscador)
		self.tabla.column('id', width=63,minwidth=63, anchor="center")
		self.tabla.column('codigo', width=100,minwidth=63, anchor="center")
		self.tabla.column('proveedor', width=100,minwidth=100, anchor="center")
		self.tabla.column('producto', width=400,minwidth=400, anchor="center", stretch=True)
		self.tabla.column('stock', width=63,minwidth=63, anchor="center")
		self.tabla.column('costo', width=125,minwidth=125, anchor="center")
		self.tabla.column('precio_venta', width=125,minwidth=125, anchor="center")
		self.tabla.heading('id', text='ID')
		self.tabla.heading('codigo', text='Código')
		self.tabla.heading('proveedor', text='Proveedor')
		self.tabla.heading('producto', text='Producto')
		self.tabla.heading('stock', text='Stock')
		self.tabla.heading('costo', text='Costo')
		self.tabla.heading('precio_venta', text='Precio de venta')
		self.barra=Scrollbar(self.ventanaBuscador, orient="vertical", command=self.tabla.yview)
		self.tabla.configure(yscrollcommand=self.barra.set)
		self.barra.grid(row=9, column=5, sticky = 'NS')
		self.tabla.grid(row=9, column=0,columnspan=5,padx=10)

		self.boton_backup_lista=Button(self.ventanaBuscador, text='Informe stock',font=('Comic Sans MS', 10),fg='#3BA684',command=self.backup). grid(row=11, column=0, padx=3, pady=3)
		self.boton_uso_interno=Button(self.ventanaBuscador, text='Producto para\nuso interno',font=('Comic Sans MS', 10),fg='#3BA684',command=self.Uso_interno). grid(row=11, column=2, padx=3, pady=3)
		self.boton_lista=Button(self.ventanaBuscador, text='Generar lista de precios',font=('Comic Sans MS', 10),fg='#3BA684', command=self.lista_pdf). grid(row=10, column=3, padx=3, pady=3)
		self.boton_eliminar_lista=Button(self.ventanaBuscador, text='Eliminar lista de precios',font=('Comic Sans MS', 10),fg='#3BA684', command=self.eliminar_lista_publico). grid(row=11, column=3, padx=3, pady=3)
		
		self.ventanaBuscador.mainloop()

#----------------Ventana Compras------------------- 
	def Compras(self,event=None):
		self.ventanaCompras=Toplevel()
		self.ventanaCompras.title("Compras")
		self.ventanaCompras.geometry("+400+75")
		self.ventanaCompras.config(bg='#C3C3C3')
		self.ventanaCompras.resizable(0,0)
		self.ventanaCompras.transient(self.inicio)
		self.ventanaCompras.grab_set()

		self.id.set('')
		self.id_producto.set('')
		self.cte.set('')
		self.nrocte.set('')
		self.fechacte.set('')
		self.codigo.set('')
		self.proveedor.set('')
		self.producto.set('')
		self.stock.set('')
		self.costo.set('')
		self.precio_venta.set('')
		self.subtotal.set('')
		self.porcentaje.set('')
		self.descuento.set('')
		self.total_compra.set('')
		
		#Selección Proveedor
		self.provlabel=Label(self.ventanaCompras, text='Proveedor',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.provlabel.grid(row=0, column=0,padx=3, pady=3)
		self.cb1=Combobox(self.ventanaCompras,font=('Comic Sans MS', 10), textvariable=self.proveedor)
		self.cb1['values']=self.lista_prov()
		self.cb1.bind("<<ComboboxSelected>>",self.lista_prov)
		self.cb1.focus()
		self.cb1.grid(row=1, column=0,padx=3, pady=3,)
		self.nuevoprov=Button(self.ventanaCompras,text='Nuevo',width=6,font=('Comic Sans MS', 10),fg='#3BA684',command=self.Proveedor)
		self.nuevoprov.bind('<Return>', self.Proveedor)
		self.nuevoprov.grid(row=1, column=1,padx=3, pady=3, sticky='w')

		#Comprobante
		self.ctelabel=Label(self.ventanaCompras, text='Tipo de comprobante',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.ctelabel.grid(row=2, column=0,padx=3, pady=3)
		self.ctecb1=Combobox(self.ventanaCompras,font=('Comic Sans MS', 10), textvariable=self.cte)
		self.ctecb1['values']=self.lista_cte()
		self.ctecb1.grid(row=3, column=0,padx=3, pady=3,)

		#Número de comprobante
		self.nrolabel=Label(self.ventanaCompras, text='Número de comprobante',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.nrolabel.grid(row=2, column=1,padx=3, pady=3)
		self.nroentry=Entry(self.ventanaCompras,textvariable=self.nrocte,width=32,font=('Comic Sans MS', 10))
		self.nroentry.grid(row=3, column=1,padx=3, pady=3,)	

		#Fecha de comprobante
		self.fechalabel=Label(self.ventanaCompras, text='Fecha de comprobante',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.fechalabel.grid(row=2, column=2,padx=3, pady=3)
		self.fechaentry=Entry(self.ventanaCompras,textvariable=self.fechacte,width=32,font=('Comic Sans MS', 10))
		self.fechaentry.bind("<Return>", self.escribaFecha)
		self.fechaentry.bind("<Tab>", self.escribaFecha)
		self.fechaentry.grid(row=3, column=2,padx=3, pady=3,)

		#Pago
		self.pagolabel=Label(self.ventanaCompras, text='Medio de pago',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.pagolabel.grid(row=2, column=3,padx=3, pady=3)
		self.pagocb1=Combobox(self.ventanaCompras,font=('Comic Sans MS', 10), textvariable=self.pagos)
		self.pagocb1['values']=self.lista_medios()
		self.pagocb1.grid(row=3, column=3,padx=3, pady=3,)

		#Datos compras
		self.l1=Label(self.ventanaCompras, text='Producto',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l1.grid(row=4, column=0,pady=3, padx=3)
		self.e1=Entry(self.ventanaCompras,textvariable=self.producto,width=32,font=('Comic Sans MS', 10))
		self.e1.bind('<KeyRelease>',self.busq_list) 
		self.e1.grid(row=4, column=1,pady=3, padx=3)
		self.list1=Listbox(self.ventanaCompras,font=('Comic Sans MS', 10) )
		self.list1.config(width="60", height="10")
		self.lista_busq_prod(self.lista_prod())
		self.list1.bind('<Return>', self.mostrar_datos_producto)
		self.list1.grid(row=5, column=0,columnspan=2,rowspan=4,pady=3, padx=3)
		self.nuevoprod=Button(self.ventanaCompras,text='Añadir',font=('Comic Sans MS', 10),fg='#3BA684',command=self.nuevo_articulo)
		self.nuevoprod.grid(row=4, column=2,padx=3, pady=3,sticky='w')
		self.modifprod=Button(self.ventanaCompras,text='Modificar',font=('Comic Sans MS', 10),fg='#3BA684', command=self.modificar_nombre_articulo)
		self.modifprod.grid(row=4, column=2,padx=3, pady=3, sticky='e')

		id_producto_label=Label(self.ventanaCompras, text='Id producto',bg='#C3C3C3',font=('Comic Sans MS', 10))
		id_producto_label.grid(row=5, column=2,pady=3, padx=3,sticky='w')
		id_producto_entry=Entry(self.ventanaCompras,textvariable=self.id_producto, width=8,font=('Comic Sans MS', 10),state='readonly')
		id_producto_entry.grid(row=5, column=2,pady=3, padx=3,)
		self.l2=Label(self.ventanaCompras, text='Cód.\nProveedor',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l2.grid(row=6, column=2,pady=3, padx=3,sticky='w')
		self.e2=Entry(self.ventanaCompras,textvariable=self.codigo, width=15,font=('Comic Sans MS', 10))
		self.e2.grid(row=6, column=2,pady=3, padx=3,)

		self.l3=Label(self.ventanaCompras, text='        Cant.',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l3.grid(row=7, column=2,pady=3, padx=3,sticky='w')
		self.e3=Entry(self.ventanaCompras, textvariable=self.stock, width=12,font=('Comic Sans MS', 10))
		self.e3.grid(row=7, column=2,pady=3, padx=3,)
	
		self.l4=Label(self.ventanaCompras, text='        Costo',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l4.grid(row=8, column=2,pady=3, padx=3,sticky='w')
		self.e4=Entry(self.ventanaCompras,textvariable=self.costo, width=12,font=('Comic Sans MS', 10))
		self.e4.grid(row=8, column=2,pady=3, padx=3,)

		#Botones
		""" self.botonPVenta=Button(self.ventanaCompras, text='Calcular \nP. Venta',font=('Comic Sans MS', 10),fg='#3BA684', command=self.calculo_venta)
		self.botonPVenta.grid(row=8, column=2,pady=3, padx=3,sticky='w')
		self.e5=Entry(self.ventanaCompras,textvariable=self.precio_venta,width=12,font=('Comic Sans MS', 10))
		self.e5.grid(row=8, column=2,pady=3, padx=3,sticky='e')	 """
		self.agregarprod=Button(self.ventanaCompras,text='Agregar producto',font=('Comic Sans MS', 10),fg='#3BA684', command=self.agregar_compra)
		self.agregarprod.bind('<Return>', self.agregar_compra)
		self.agregarprod.grid(row=10, column=2,padx=3, pady=3, )
		self.recuperar=Button(self.ventanaCompras,text='Recuperar Datos',font=('Comic Sans MS', 10),fg='#3BA684', command=self.recuperar_compra)
		self.recuperar.grid(row=10, column=3,padx=3, pady=3)

		#Tabla
		self.encabezado=['id','codigo','proveedor','producto','stock','costo','pretotal']
		self.tablaCompras=Treeview(self.ventanaCompras, columns=self.encabezado, show='headings')
		self.tablaCompras.column('id', width=62,minwidth=62, anchor="center")
		self.tablaCompras.column('codigo', width=88,minwidth=88, anchor="center")
		self.tablaCompras.column('proveedor', width=100,minwidth=88, anchor="center")
		self.tablaCompras.column('producto', width=315,minwidth=315, anchor="center", stretch=True)
		self.tablaCompras.column('stock', width=62,minwidth=62, anchor="center")
		self.tablaCompras.column('costo', width=125,minwidth=125, anchor="center")
		self.tablaCompras.column('pretotal', width=125,minwidth=125, anchor="center")
		self.tablaCompras.heading('id', text='ID')
		self.tablaCompras.heading('codigo', text='Cód. Prov.')
		self.tablaCompras.heading('proveedor', text='Proveedor')
		self.tablaCompras.heading('producto', text='Producto')
		self.tablaCompras.heading('stock', text='Stock')
		self.tablaCompras.heading('costo', text='Costo')  
		self.tablaCompras.heading('pretotal', text='Total parcial') 
		self.tablaCompras.bind('<<TreeviewSelect>>',self.seleccionar_compra)
		self.tablaCompras.bind('<Key-Delete>', self.eliminar_de_lista)
		self.barra=Scrollbar(self.ventanaCompras, orient="vertical", command=self.tablaCompras.yview)
		self.tablaCompras.configure(yscrollcommand=self.barra.set)
		self.barra.grid(row=11, column=3, sticky = 'ENS', pady=10)
		self.tablaCompras.grid(row=11, column=0,columnspan=4,padx=10, pady=10)

		self.label_sub=Label(self.ventanaCompras, text='Sub-Total',bg='#C3C3C3',font=('Comic Sans MS', 10), )
		self.label_sub.grid(row=12, column=2,sticky='e')
		self.entry_subtotal=Entry(self.ventanaCompras,textvariable=self.subtotal,width=12,font=('Comic Sans MS', 10),state='readonly')
		self.entry_subtotal.grid(row=12, column=3)
		self.labelDescuento=Label(self.ventanaCompras, text='Porc. Descuento',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.labelDescuento.grid(row=13, column=2,sticky='e')
		self.label_porcentual=Label(self.ventanaCompras, text='      %',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.label_porcentual.grid(row=13, column=3,sticky='w')
		self.entryPorcentaje=Entry(self.ventanaCompras,textvariable=self.porcentaje_descuento,width=6,font=('Comic Sans MS', 10))
		self.entryPorcentaje.bind('<Tab>',self.descuento_compra)
		self.entryPorcentaje.bind('<Return>',self.descuento_compra)
		self.entryPorcentaje.grid(row=13, column=3,)
		self.labelMonto_descuento=Label(self.ventanaCompras, text='Monto descuento',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.labelMonto_descuento.grid(row=14, column=2,sticky='e')
		self.label_pesos=Label(self.ventanaCompras, text='  $',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.label_pesos.grid(row=14, column=3,sticky='w',)
		self.entryDescuento=Entry(self.ventanaCompras, text=self.descuento,width=12,font=('Comic Sans MS', 10))
		self.entryDescuento.bind('<Tab>',self.sumaTotales)
		self.entryDescuento.bind('<Return>',self.sumaTotales)
		self.entryDescuento.grid(row=14, column=3,)
		self.label_total=Label(self.ventanaCompras, text='Total',bg='#C3C3C3',font=('Comic Sans MS', 10), )
		self.label_total.grid(row=15, column=2,sticky='e')
		self.entry_sumatotal=Entry(self.ventanaCompras,textvariable=self.total_compra,width=12,font=('Comic Sans MS', 10),bg='#C3C3C3')
		self.entry_sumatotal.config(state='readonly')
		self.entry_sumatotal.grid(row=15, column=3,)
		

		self.limpiar_pantalla_compras=Button(self.ventanaCompras,text='Limpiar pantalla',font=('Comic Sans MS', 10),fg='#3BA684',command=self.limpiar_compras)
		self.limpiar_pantalla_compras.bind('<Return>',self.finalizar_compra)
		self.limpiar_pantalla_compras.grid(row=16, column=0,padx=3, pady=3,rowspan=2)

		self.final=Button(self.ventanaCompras,text='Finalizar compra',font=('Comic Sans MS', 10),fg='#3BA684',command=self.finalizar_compra)
		self.final.bind('<Return>',self.finalizar_compra)
		self.final.grid(row=16, column=3,padx=3, pady=3,rowspan=2)
		self.ventanaCompras.mainloop()

#----------------Ventana Tipo de comprobante-------
	def Tipo_comprobante(self,event=None):
			self.ventanatipo_cte = Toplevel()
			self.ventanatipo_cte.title("Configuración de Comprobantes")
			self.ventanatipo_cte.geometry("+600+200")
			self.ventanatipo_cte.config(bg='#C3C3C3')
			self.ventanatipo_cte.resizable(0,0)
			self.ventanatipo_cte.transient(self.inicio)
			self.ventanatipo_cte.grab_set()

			self.cte.set('')
					
			espacio=Label(self.ventanatipo_cte, text='',bg='#C3C3C3').grid(row=0, column=0, )

			l1=Label(self.ventanatipo_cte, text='Tipo de Comprobante',bg='#C3C3C3',font=('Comic Sans MS', 10))
			l1.grid(row=2, column=1,pady=3, padx=3)
			self.cb_tipo1=Combobox(self.ventanatipo_cte, textvariable=self.cte,width=33,font=('Comic Sans MS', 10))
			self.cb_tipo1['values']=self.lista_cte()
			self.cb_tipo1.bind("<<ComboboxSelected>>",self.lista_cte)
			self.cb_tipo1.focus()
			self.cb_tipo1.grid(row=3, column=1,pady=3, padx=3)
			
			botonAgregar=Button(self.ventanatipo_cte, text='Agregar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.agregar_tipocte).grid(row=10, column=1, padx=3, pady=3,sticky='w')
			botonAgregar=Button(self.ventanatipo_cte, text='Eliminar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.eliminar_tipocte).grid(row=10, column=1, padx=3, pady=3,sticky='e')

			self.ventanatipo_cte.mainloop()
			
#----------------Ventana Medios de pagos------------
	def Medios_pago(self,event=None):
			self.ventanamedios_pagos = Toplevel()
			self.ventanamedios_pagos.title("Medios de pagos")
			self.ventanamedios_pagos.geometry("+600+200")
			self.ventanamedios_pagos.config(bg='#C3C3C3')
			self.ventanamedios_pagos.resizable(0,0)
			self.ventanamedios_pagos.transient(self.inicio)
			self.ventanamedios_pagos.grab_set()

			self.pagos.set('')
					
			espacio=Label(self.ventanamedios_pagos, text='',bg='#C3C3C3').grid(row=0, column=0, )

			l1=Label(self.ventanamedios_pagos, text='Medio de pago',bg='#C3C3C3',font=('Comic Sans MS', 10))
			l1.grid(row=2, column=1,pady=3, padx=3)
			self.cb1=Combobox(self.ventanamedios_pagos, textvariable=self.pagos,width=33,font=('Comic Sans MS', 10))
			self.cb1['values']=self.lista_medios()
			self.cb1.bind("<<ComboboxSelected>>",self.lista_medios)
			self.cb1.focus()
			self.cb1.grid(row=3, column=1,pady=3, padx=3)
			
			botonAgregar=Button(self.ventanamedios_pagos, text='Agregar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.agregar_medio).grid(row=10, column=1, padx=3, pady=3,sticky='w')
			botonAgregar=Button(self.ventanamedios_pagos, text='Eliminar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.eliminar_medio).grid(row=10, column=1, padx=3, pady=3,sticky='e')

			self.ventanamedios_pagos.mainloop()

#----------------Ventana Modificador de nombre de artículo
	def modificar_nombre_articulo(self,event=None):
		try:
			self.list1.selection_get()
			self.Modificador=Toplevel()
			self.Modificador.title("Cambiar descripcion del artículo")
			self.Modificador.geometry("+600+200")
			self.Modificador.config(bg='#C3C3C3')
			self.Modificador.resizable(0,0)
			self.Modificador.transient(self.inicio)
			self.Modificador.grab_set()

			self.articulo=self.list1.selection_get()
			self.actualizado=StringVar()
			self.articulo_inicial=Label(self.Modificador, text=f'Modificar la descripción del artículo\n\n{self.articulo}\n\npor: ',bg='#C3C3C3',font=('Comic Sans MS', 10))
			self.articulo_inicial.grid(row=0, column=0, columnspan=3)
			self.articulo_modificado=Entry(self.Modificador, textvariable=self.actualizado,font=('Comic Sans MS', 10),width=37)
			self.articulo_modificado.focus()
			self.articulo_modificado.grid(row=1, column=0,padx=5)
			self.guardar=Button(self.Modificador, text='Guardar cambios',font=('Comic Sans MS', 10),command=self.guardar_cambio )
			self.guardar.bind('<Return>', self.guardar_cambio)
			self.guardar.grid(row=1, column=1,padx=5)
			self.Modificador.mainloop()
		except TclError:
			messagebox.showerror('Error','Debe seleccionar un articulo para modificar')
		
#----------------Ventana Proveedor-----------------
	def Proveedor(self,event=None):
		self.ventanaProveedor = Toplevel()
		self.ventanaProveedor.title("Gestión de Proveedores")
		self.ventanaProveedor.geometry("+600+200")
		self.ventanaProveedor.config(bg='#C3C3C3')
		self.ventanaProveedor.resizable(0,0)
		self.ventanaProveedor.transient(self.inicio)
		self.ventanaProveedor.grab_set()
		self.proveedor.set('')
		self.direccion.set('')
		self.telefono.set('')
		self.correo.set('')
		
		espacio=Label(self.ventanaProveedor, text='',bg='#C3C3C3').grid(row=0, column=0, )
		l1=Label(self.ventanaProveedor, text='Proveedor',bg='#C3C3C3',font=('Comic Sans MS', 10))
		l1.grid(row=2, column=1,pady=3, padx=3)
		self.cb1=Combobox(self.ventanaProveedor, textvariable=self.proveedor,width=33,font=('Comic Sans MS', 10))
		self.cb1['values']=self.lista_prov()
		self.cb1.bind("<<ComboboxSelected>>",self.mostrar_datos_proveedor)
		self.cb1.focus()
		self.cb1.grid(row=3, column=1,pady=3, padx=3)
		
		l2=Label(self.ventanaProveedor, text='Dirección',bg='#C3C3C3',font=('Comic Sans MS', 10))
		l2.grid(row=4, column=1,pady=3, padx=3)
		e2=Entry(self.ventanaProveedor,textvariable=self.direccion, width=37,font=('Comic Sans MS', 10))
		e2.grid(row=5, column=1,pady=3, padx=3)
		l3=Label(self.ventanaProveedor, text='Teléfono',bg='#C3C3C3',font=('Comic Sans MS', 10))
		l3.grid(row=6, column=1,pady=3, padx=3)
		e3=Entry(self.ventanaProveedor,textvariable=self.telefono, width=37,font=('Comic Sans MS', 10))
		e3.grid(row=7, column=1,pady=3, padx=3)
		l4=Label(self.ventanaProveedor, text='Correo',bg='#C3C3C3',font=('Comic Sans MS', 10))
		l4.grid(row=8, column=1,pady=3, padx=3)
		e4=Entry(self.ventanaProveedor,textvariable=self.correo,width=37,font=('Comic Sans MS', 10))
		e4.grid(row=9, column=1,pady=3, padx=3)
		botonAgregar=Button(self.ventanaProveedor, text='Agregar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.agregar_proveedor).grid(row=10, column=1, padx=3, pady=3,sticky='w')
		botonAgregar=Button(self.ventanaProveedor, text='Modificar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.modificar_proveedor).grid(row=10, column=1,padx=3, pady=3,sticky='ns')
		botonAgregar=Button(self.ventanaProveedor, text='Eliminar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.eliminar_proveedor).grid(row=10, column=1, padx=3, pady=3,sticky='e')
		self.ventanaProveedor.mainloop()
			
#----------------Ventana Cliente-----------------
	def Clientes(self,event=None):
		self.ventanaClientes = Toplevel()
		self.ventanaClientes.title("Gestión de Clientes")
		self.ventanaClientes.geometry("+400+100")
		self.ventanaClientes.config(bg='#C3C3C3')
		self.ventanaClientes.resizable(0,0)
		self.ventanaClientes.transient(self.inicio)
		self.ventanaClientes.grab_set()

		self.cliente=StringVar()
		self.cliente.set('')
		self.nombre.set('')
		self.apellido.set('')
		self.direccion.set('')
		self.telefono.set('')
		self.correo.set('')
			
		espacio=Label(self.ventanaClientes, text='',bg='#C3C3C3').grid(row=0, column=0, )

		#Buscar Clientes
		self.labelCliente=Label(self.ventanaClientes, text='Cliente',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.labelCliente.grid(row=0, column=1,pady=3, padx=3)
		self.entryCliente=Entry(self.ventanaClientes,textvariable=self.cliente,width=32,font=('Comic Sans MS', 10))
		self.entryCliente.bind('<KeyRelease>',self.busq_cliente) 
		self.entryCliente.focus()
		self.entryCliente.grid(row=1, column=1,pady=3, padx=3)
		self.listaClientes=Listbox(self.ventanaClientes,font=('Comic Sans MS', 10) )
		self.listaClientes.config(width="37", height="10")
		self.lista_busq_cliente(self.lista_cliente())
		self.listaClientes.bind('<Return>', self.mostrar_datos_cliente)
		self.listaClientes.grid(row=2, column=1,columnspan=3,pady=3, padx=3)

		labelNombre=Label(self.ventanaClientes, text='Nombre',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelNombre.grid(row=3, column=1,pady=3, padx=3)
		entryNombre=Entry(self.ventanaClientes,textvariable=self.nombre, width=37,font=('Comic Sans MS', 10))
		entryNombre.grid(row=4, column=1,pady=3, padx=3)

		labelApellido=Label(self.ventanaClientes, text='Apellido',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelApellido.grid(row=5, column=1,pady=3, padx=3)
		entryApellido=Entry(self.ventanaClientes,textvariable=self.apellido, width=37,font=('Comic Sans MS', 10))
		entryApellido.grid(row=6, column=1,pady=3, padx=3)

		labelDireccion=Label(self.ventanaClientes, text='Dirección',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelDireccion.grid(row=7, column=1,pady=3, padx=3)
		entryDireccion=Entry(self.ventanaClientes,textvariable=self.direccion, width=37,font=('Comic Sans MS', 10))
		entryDireccion.grid(row=8, column=1,pady=3, padx=3)

		labelTelefono=Label(self.ventanaClientes, text='Teléfono',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelTelefono.grid(row=9, column=1,pady=3, padx=3)
		entryTelefono=Entry(self.ventanaClientes,textvariable=self.telefono, width=37,font=('Comic Sans MS', 10))
		entryTelefono.grid(row=10, column=1,pady=3, padx=3)

		labelCorreo=Label(self.ventanaClientes, text='Correo',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelCorreo.grid(row=11, column=1,pady=3, padx=3)
		entryCorreo=Entry(self.ventanaClientes,textvariable=self.correo,width=37,font=('Comic Sans MS', 10))
		entryCorreo.grid(row=12, column=1,pady=3, padx=3)

		botonAgregar=Button(self.ventanaClientes, text='Agregar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.agregar_cliente).grid(row=13, column=1, padx=3, pady=3,sticky='w')
		botonAgregar=Button(self.ventanaClientes, text='Modificar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.modificar_cliente).grid(row=13, column=1,padx=3, pady=3,sticky='ns')
		botonAgregar=Button(self.ventanaClientes, text='Eliminar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.eliminar_cliente).grid(row=13, column=1, padx=3, pady=3,sticky='e')

		self.ventanaClientes.mainloop()
		
#----------------Ventana Producto------------------
	def Producto(self,event=None):
		self.ventanaProducto=Toplevel()
		self.ventanaProducto.title("Productos")
		self.ventanaProducto.geometry("+600+200")
		self.ventanaProducto.config(bg='#C3C3C3')
		self.ventanaProducto.resizable(0,0)
		self.ventanaProducto.transient(self.inicio)
		self.ventanaProducto.grab_set()

		#ID	
		self.l1=Label(self.ventanaProducto, text='ID',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l1.grid(row=0, column=0,pady=3, padx=3)
		self.e1=Entry(self.ventanaProducto, textvariable=self.id_producto,width=12,state='readonly',font=('Comic Sans MS', 10),justify='center')
		self.e1.grid(row=0, column=1,pady=3, padx=3)

		#Código del proveedor
		self.l2=Label(self.ventanaProducto, text='Cód. Proveedor',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l2.grid(row=1, column=0,pady=3, padx=3)
		self.e2=Entry(self.ventanaProducto,textvariable=self.codigo, width=18,font=('Comic Sans MS', 10),justify='center')
		self.e2.focus()
		self.e2.grid(row=1, column=1,pady=3, padx=3)
		
		#Proveedor
		self.l3=Label(self.ventanaProducto, text='Proveedor',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l3.grid(row=2, column=0,pady=3, padx=3)
		self.combo_proveedor=Combobox(self.ventanaProducto,textvariable=self.proveedor, width=32,font=('Comic Sans MS', 10),justify='center')
		self.combo_proveedor['values']=self.lista_prov()
		self.combo_proveedor.grid(row=2, column=1,pady=3, padx=3)

		#Producto
		self.l4=Label(self.ventanaProducto, text='Producto',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l4.grid(row=3, column=0,pady=3, padx=3)
		self.e4=Entry(self.ventanaProducto,textvariable=self.producto,width=50,font=('Comic Sans MS', 9),justify='center')
		self.e4.grid(row=3, column=1,pady=3, padx=3)

		#Cantidades
		self.l5=Label(self.ventanaProducto, text='Cant.',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l5.grid(row=4, column=0,pady=3, padx=3)
		self.e5=Entry(self.ventanaProducto, textvariable=self.stock, width=12,font=('Comic Sans MS', 10),justify='center')
		self.e5.grid(row=4, column=1,pady=3, padx=3)

		#Costos
		self.l6=Label(self.ventanaProducto, text='Costo',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l6.grid(row=5, column=0,pady=3, padx=3)
		self.e6=Entry(self.ventanaProducto,textvariable=self.costo, width=12,font=('Comic Sans MS', 10),justify='center')
		self.e6.grid(row=5, column=1,pady=3, padx=3)

		#Precio de venta
		self.l7=Label(self.ventanaProducto, text='P. Venta',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.l7.grid(row=6, column=0,pady=3, padx=3)
		self.e7=Entry(self.ventanaProducto,textvariable=self.precio_venta,width=12,font=('Comic Sans MS', 10),justify='center')
		self.e7.grid(row=6, column=1,pady=3, padx=3)
		self.calcPVenta=Button(self.ventanaProducto, text='Calcular P. Venta',font=('Comic Sans MS', 10),fg='#3BA684', command=self.boton_precio_venta)
		self.calcPVenta.grid(row=6, column=2,pady=3, padx=3)

		#Botones
		self.botonAgregar=Button(self.ventanaProducto, text='Agregar artículo',font=('Comic Sans MS', 10),fg='#3BA684',command=self.agregar_articulo). grid(row=7, column=0, padx=3, pady=3)
		self.botonEliminar=Button(self.ventanaProducto, text='Eliminar artículo',font=('Comic Sans MS', 10),fg='#3BA684',command=self.eliminar_articulo). grid(row=7, column=1, padx=3, pady=3)
		self.botonModificar=Button(self.ventanaProducto, text='Modificar artículo',font=('Comic Sans MS', 10),fg='#3BA684',command=self.modificar_articulo). grid(row=7, column=2, padx=3, pady=3)
		
		self.ventanaProducto.mainloop()
		
#----------------Ventana consumo interno------------------
	def Uso_interno (self,event=None):
		self.ventanaUso_interno=Toplevel()
		self.ventanaUso_interno.title("Productos para consumo interno")
		self.ventanaUso_interno.geometry("+400+100")
		self.ventanaUso_interno.config(bg='#C3C3C3')
		#self.ventanaUso_interno.resizable(0,0)
		self.ventanaUso_interno.transient(self.inicio)
		self.ventanaUso_interno.grab_set()
	
		self.producto.set('')
		self.id_producto.set('')
		self.cant_pedido.set('')

		#Fecha
		self.lFecha=Label(self.ventanaUso_interno, text='Fecha',bg='#C3C3C3',font=('Comic Sans MS', 10)).grid(row=0,column=1, pady=3, padx=3)
		self.eFechaActual=Label(self.ventanaUso_interno,text=self.fecha,bg='#C3C3C3',font=('Comic Sans MS', 10)).grid(row=1,column=1, pady=3, padx=3)

		#Ver historial de usos internos
		self.botonHistorial=Button(self.ventanaUso_interno, text='Historial de\nusos interno',font=('Comic Sans MS', 10),fg='#3BA684',command=self.Busqueda_uso_interno)
		self.botonHistorial.bind('<Return>',self.Busqueda_uso_interno)
		self.botonHistorial.grid(row=1, column=4,  padx=3, pady=3)

		#Articulos del Pedido
		labelproducto=Label(self.ventanaUso_interno, text='Producto',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelproducto.grid(row=0, column=0,pady=3, padx=10)
		self.entryProd_pedido=Entry(self.ventanaUso_interno,textvariable=self.producto,width=32,font=('Comic Sans MS', 10))
		self.entryProd_pedido.bind('<KeyRelease>',self.busq_list) 
		self.entryProd_pedido.grid(row=1, column=0,pady=3, padx=3)
		self.list1=Listbox(self.ventanaUso_interno,font=('Comic Sans MS', 10) )
		self.list1.config(width="50", height="12")
		self.list1.bind('<Return>',self.datos_para_pedido)
		self.lista_busq_prod(self.lista_prod())
		self.list1.grid(row=6, column=0,columnspan=2,pady=3, padx=3)

		self.id_producto_label=Label(self.ventanaUso_interno, text='Id prod.', bg='#C3C3C3',font=('Comic Sans MS', 10) )
		self.id_producto_label.grid(row=7, column=0,pady=3, padx=3,sticky='w')
		self.id_producto_entry=Entry(self.ventanaUso_interno, textvariable=self.id_producto, width=8,font=('Comic Sans MS', 10), state='readonly')
		self.id_producto_entry.grid(row=7, column=0,pady=3, padx=3,)

		#Cantidad de articulos del pedido
		self.cant_pedido_label=Label(self.ventanaUso_interno, text='Cant.',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.cant_pedido_label.grid(row=7, column=0,pady=3, padx=3,sticky='e')
		self.cant_pedido_entry=Entry(self.ventanaUso_interno, textvariable=self.cant_pedido, width=12,font=('Comic Sans MS', 10))
		self.cant_pedido_entry.bind('<Return>',self.agregar_uso_interno)
		self.cant_pedido_entry.grid(row=7, column=1,pady=3, padx=3,sticky='w')

		#Boton agregar item
		self.botonAgregar=Button(self.ventanaUso_interno, text='Agregar artículo',font=('Comic Sans MS', 10),fg='#3BA684',command=self.agregar_uso_interno)
		self.botonAgregar.bind('<Return>',self.agregar_uso_interno)
		self.botonAgregar.grid(row=7, column=2,  padx=3, pady=3)

		#Tabla de productos del pedido
		self.encabezado=['id','producto','stock']
		self.tabla_uso_interno=ttk.Treeview(self.ventanaUso_interno, columns=self.encabezado, show='headings')
		self.tabla_uso_interno.column('id', width=62,minwidth=62, anchor="center")
		self.tabla_uso_interno.column('producto', width=312,minwidth=312, anchor="center", stretch=True)
		self.tabla_uso_interno.column('stock', width=62,minwidth=62, anchor="center")
		self.tabla_uso_interno.heading('id', text='ID')
		self.tabla_uso_interno.heading('producto', text='Producto')
		self.tabla_uso_interno.heading('stock', text='Cant.')
		self.tabla_uso_interno.bind('<Key-Delete>', self.eliminar_uso_interno)
		self.barra_uso_interno=Scrollbar(self.ventanaUso_interno, orient="vertical", command=self.tabla_uso_interno.yview)
		self.tabla_uso_interno.configure(yscrollcommand=self.barra_uso_interno.set)
		self.barra_uso_interno.grid(row=6, column=6, sticky = 'NS',pady=10)
		self.tabla_uso_interno.grid(row=6, column=2,columnspan=4,padx=10, pady=10,sticky='w')

		#Boton confirmación de pedido.
		self.botonConfirmar=Button(self.ventanaUso_interno, text='Confirmar',font=('Comic Sans MS', 10),fg='#3BA684', command=self.confirmar_uso_interno). grid(row=7, column=4, padx=3, pady=10)

		self.ventanaUso_interno.mainloop()

#----------------Ventana historial usos internos-----------
	def Busqueda_uso_interno (self,event=None):
		self.ventanaHistorial=Toplevel()
		self.ventanaHistorial.title("Productos para consumo interno")
		self.ventanaHistorial.geometry("+400+100")
		self.ventanaHistorial.config(bg='#C3C3C3')
		#self.ventanaHistorial.resizable(0,0)
		self.ventanaHistorial.transient(self.inicio)
		self.ventanaHistorial.grab_set()

		Label(self.ventanaHistorial, text='Buscador',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=0, column=0, padx=3)
		self.entryB_usos=Entry(self.ventanaHistorial, textvariable=self.buscador_usos,font=('Comic Sans MS', 10))
		self.entryB_usos.focus()
		self.entryB_usos.bind('<Return>',self.buscar_usos)
		self.entryB_usos.grid(row=1, column=0, padx=3, pady=3)
		self.entryB_usos.focus()
		self.botonB_usos=Button(self.ventanaHistorial, text='Buscar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.buscar_usos)
		self.botonB_usos.bind('<Return>',self.buscar_usos)
		self.botonB_usos.grid(row=1, column=1, padx=3, pady=3)
		
		#Tabla Historial de usos
		self.encabezado_usos=['id','id_producto','producto', 'cantidad','fecha']
		self.tablaBusq_usos=Treeview(self.ventanaHistorial, columns=self.encabezado_usos , show='headings',)
		self.tablaBusq_usos.column('id', width=50,minwidth=50, anchor="center")
		self.tablaBusq_usos.column('id_producto', width=50,minwidth=60, anchor="center")
		self.tablaBusq_usos.column('producto', width=225,minwidth=225, anchor="center")
		self.tablaBusq_usos.column('cantidad', width=50,minwidth=50, anchor="center")
		self.tablaBusq_usos.column('fecha', width=80,minwidth=80, anchor="center")
		self.tablaBusq_usos.heading('id', text='ID')
		self.tablaBusq_usos.heading('id_producto', text='ID prod.')
		self.tablaBusq_usos.heading('producto', text='Producto')
		self.tablaBusq_usos.heading('cantidad', text='Cant.')
		self.tablaBusq_usos.heading('fecha', text='Fecha')
		self.barraBusq_usos=Scrollbar(self.ventanaHistorial, orient="vertical", command=self.tablaBusq_usos.yview)
		self.tablaBusq_usos.configure(yscrollcommand=self.barraBusq_usos.set)
		self.barraBusq_usos.grid(row=2, column=4, sticky = 'NS')
		self.tablaBusq_usos.grid(row=2, column=0,columnspan=4,padx=10)

		self.ventanaHistorial.mainloop()

#----------------Ventana precio de venta------------------
	def Calculos(self):
		self.ventanaCalculos=Toplevel()
		self.ventanaCalculos.title('Precio de venta')
		self.ventanaCalculos.geometry('+500+50')#+500+50 ubicación de la ventana en la pantalla
		self.ventanaCalculos.config(bg='#C3C3C3')
		self.ventanaCalculos.resizable(width=0, height=0)
		self.ventanaCalculos.transient(self.inicio)
		self.ventanaCalculos.grab_set()

		#TITULO
		Label(self.ventanaCalculos,text='Configuración de precio de venta',font=('Comic Sans MS', 16),bg='#C3C3C3', justify='center').grid(row=0, column=0, columnspan=3,pady=5)
		
		Label(self.ventanaCalculos,text='Seleccionar proveedor\ndonde aplicar el\nprecio de venta',font=('Comic Sans MS', 10, 'bold'),bg='#C3C3C3', justify='center').grid(row=1, column=0,pady=5)
		self.toda_lista_radio=Radiobutton(self.ventanaCalculos, text='Toda la lista',font=('Comic Sans MS', 10),bg='#C3C3C3', variable=self.lista_publico, value=1,command=self.seleccion_precio_publico)
		self.toda_lista_radio.bind('<Return>', self.seleccion_precio_publico)
		self.toda_lista_radio.grid(row=2, column=0, padx=3, pady=3, sticky='w')
		self.proveedor_radio=Radiobutton(self.ventanaCalculos, text='Por proveedor',font=('Comic Sans MS', 10),bg='#C3C3C3',variable=self.lista_publico, value=2,command=self.seleccion_precio_publico)
		self.proveedor_radio.bind('<Return>', self.seleccion_precio_publico)
		self.proveedor_radio.grid(row=3, column=0, padx=3, pady=3, sticky='w')
		self.lista_proveedor=Combobox(self.ventanaCalculos,font=('Comic Sans MS', 10), textvariable=self.proveedor)
		self.lista_proveedor.config(state='disabled')
		self.lista_proveedor['values']=self.lista_prov()
		self.lista_proveedor.bind("<<ComboboxSelected>>",self.datos_para_precio_publico)
		self.lista_proveedor.focus()
		self.lista_proveedor.grid(row=4, column=0,padx=3, pady=3,)

		Separator(self.ventanaCalculos, orient='vertical').grid(row=1, column=1, padx=10, pady=10, rowspan=7,sticky="NS")

		Label(self.ventanaCalculos,text='Incremento del\ncosto para venta',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=1, column=2,columnspan=3)
		self.porcentaje_entry=Entry(self.ventanaCalculos,textvariable=self.porcentaje,font=('Comic Sans MS', 10), justify='center')
		self.porcentaje_entry.config(state='disabled')
		self.porcentaje_entry.grid(row=2, column=2,columnspan=2)
		Label(self.ventanaCalculos,text='%',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='left').grid(row=2, column=4)
		Label(self.ventanaCalculos,text='El redondeo será\nmultiplo de (distinto a 0):',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=3, column=1,columnspan=3)
		self.redondeo_entry=Entry(self.ventanaCalculos,textvariable=self.redondeo,font=('Comic Sans MS', 10), justify='center')
		self.redondeo_entry.config(state='disabled')
		self.redondeo_entry.grid(row=4, column=2,columnspan=2)
		self.safe=Button(self.ventanaCalculos, text='Guardar',font=('Comic Sans MS', 10),fg='#3BA684', command=self.guardar)
		self.safe.grid(row=5, column=2,columnspan=3,pady=5)
		self.cambio_masivo=Button(self.ventanaCalculos, text='Cambio masivo',font=('Comic Sans MS', 10),fg='#3BA684', command=self.cambio_masivo)
		self.cambio_masivo.grid(row=6, column=2,columnspan=3,pady=5)
		
		self.ventanaCalculos.mainloop()

#----------------Ventana Cuenta------------------
	def Cuentas(self):
		self.ventanaCuentas=Toplevel()
		self.ventanaCuentas.title('Cuentas bancarias')
		self.ventanaCuentas.geometry('+500+50')#+500+50 ubicación de la ventana en la pantalla
		self.ventanaCuentas.config(bg='#C3C3C3')
		self.ventanaCuentas.resizable(width=0, height=0)
		self.ventanaCuentas.transient(self.inicio)
		self.ventanaCuentas.grab_set()

		self.cbu.set('')
		self.alias.set('')
		self.titular.set('')
		self.dni.set('')
		self.id_Tribut.set('')
		self.cuenta.set('')

		Label(self.ventanaCuentas,text='CBU',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=1, column=0,padx=3,pady=3)
		self.cbu_enry=Entry(self.ventanaCuentas,textvariable=self.cbu,font=('Comic Sans MS', 10), justify='center',width="32")
		self.cbu_enry.focus()
		self.cbu_enry.grid(row=1, column=1,padx=3,pady=3)
		Label(self.ventanaCuentas,text='Alis CBU',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=2, column=0,padx=3,pady=3)
		self.alias_entry=Entry(self.ventanaCuentas,textvariable=self.alias,font=('Comic Sans MS', 10), justify='center',width="32").grid(row=2, column=1,padx=3,pady=3)
		Label(self.ventanaCuentas,text='Titular',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='left').grid(row=3, column=0,padx=3,pady=3)
		self.titular_entry=Entry(self.ventanaCuentas,textvariable=self.titular,font=('Comic Sans MS', 10), justify='center',width="32").grid(row=3, column=1,padx=3,pady=3)
		Label(self.ventanaCuentas,text='DNI',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=4, column=0,padx=3,pady=3)
		self.dni_entry=Entry(self.ventanaCuentas,textvariable=self.dni,font=('Comic Sans MS', 10), justify='center',width="32").grid(row=4, column=1,padx=3,pady=3)
		Label(self.ventanaCuentas,text='Id. Tributaria',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=5, column=0,padx=3,pady=3)
		self.idTribut_entry=Entry(self.ventanaCuentas,textvariable=self.id_Tribut,font=('Comic Sans MS', 10), justify='center',width="32").grid(row=5, column=1,padx=3,pady=3)
		Label(self.ventanaCuentas,text='Tipo de cuenta',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=6, column=0,padx=3,pady=3)
		self.cuenta_entry=Entry(self.ventanaCuentas,textvariable=self.cuenta,font=('Comic Sans MS', 10), justify='center',width="32").grid(row=6, column=1,padx=3,pady=3)
		Label(self.ventanaCuentas,text='Cuentas registradas',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=0, column=2,padx=3,pady=3)
		self.lista_cuenta=Listbox(self.ventanaCuentas,font=('Comic Sans MS', 10) )
		self.lista_cuenta.config(width="25", height="12")
		self.lista_cuenta.bind('<Return>',self.mostrar_datos_cuenta)
		self.lista_cuenta.bind('<Double-1>',self.mostrar_datos_cuenta)
		self.lista_cuenta.grid(row=1, column=2,rowspan=6,pady=3, padx=3)
		self.ver_lista_cuenta(self.listado_cuenta())
		self.barra_cuentas=Scrollbar(self.ventanaCuentas, orient="vertical", command=self.lista_cuenta.yview)
		self.lista_cuenta.configure(yscrollcommand=self.barra_cuentas.set)
		self.barra_cuentas.grid(row=1, column=3,rowspan=6, sticky = 'NS',pady=3)

		self.crear=Button(self.ventanaCuentas, text='Crear',font=('Comic Sans MS', 10),fg='#3BA684',command=self.nva_cuenta )
		self.crear.grid(row=7, column=0,pady=5,padx=3,sticky = 'w')
		self.modificar_cuenta=Button(self.ventanaCuentas, text='Guardar',font=('Comic Sans MS', 10),fg='#3BA684', command=self.modif_cuenta)
		self.modificar_cuenta.grid(row=7, column=1,pady=5,padx=3,sticky = 'w')
		self.borrar_cuenta=Button(self.ventanaCuentas, text='Eliminar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.elim_cuenta )
		self.borrar_cuenta.grid(row=7, column=1,pady=5,padx=3,sticky = 'e')
		
		self.ventanaCuentas.mainloop()

#----------------Ventana presupuestos--------------
	def Presupuesto(self,event=None):
		self.ventanaPresupuesto=Toplevel()
		self.ventanaPresupuesto.title("Presupuestos")
		self.ventanaPresupuesto.geometry("+400+100")
		self.ventanaPresupuesto.config(bg='#C3C3C3')
		self.ventanaPresupuesto.resizable(0,0)
		self.ventanaPresupuesto.transient(self.inicio)
		self.ventanaPresupuesto.grab_set()

		self.id_presupuesto.set('')
		self.producto.set('')
		self.id_producto.set('')
		self.cant_presupuesto.set('')
		self.precio_venta.set('')
		self.subtotal.set('')
		self.porcentaje.set(0.0)
		self.descuento.set(0.0)
		self.envio.set(0.0)
		self.total_presupuesto.set('')
		
		#Selección Cliente
		provlabel=Label(self.ventanaPresupuesto, text='Cliente',bg='#C3C3C3',font=('Comic Sans MS', 10))
		provlabel.grid(row=0, column=0,padx=3, pady=3,sticky='w')
		self.cbCliente=Combobox(self.ventanaPresupuesto,font=('Comic Sans MS', 10),width=15, textvariable=self.cliente)
		self.cbCliente['values']=self.lista_cliente()
		self.cbCliente.bind("<<ComboboxSelected>>",self.lista_cliente)
		self.cbCliente.focus()
		self.cbCliente.grid(row=1, column=0,padx=3, pady=3,sticky='w')
		self.nuevoCliente=Button(self.ventanaPresupuesto,text='Nuevo',width=5,font=('Comic Sans MS', 10),fg='#3BA684',command=self.Clientes)
		self.nuevoCliente.bind('<Return>', self.Clientes)
		self.nuevoCliente.grid(row=1, column=0,padx=3, pady=3, sticky='e')

		#Número de pedido
		labelNro_pedido=Label(self.ventanaPresupuesto, text='N° de pedido',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelNro_pedido.grid(row=0, column=1,padx=3, pady=3,)
		self.entryNro_pedido=Entry(self.ventanaPresupuesto,font=('Comic Sans MS', 10), textvariable=self.id_presupuesto)
		self.entryNro_pedido.config(state="readonly", width="12")
		self.entryNro_pedido.grid(row=1, column=1,padx=3, pady=3, )

		#Fecha
		labelFecha=Label(self.ventanaPresupuesto, text='Fecha',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelFecha.grid(row=0, column=2,padx=3, pady=3)
		labelFecha_actual=Label(self.ventanaPresupuesto, text=self.fecha ,bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelFecha_actual.grid(row=1, column=2,padx=3, pady=3)

		#Gestion de presupuestos
		self.presupuesto_anterior=Button(self.ventanaPresupuesto,text='Presupuestos anteriores',font=('Comic Sans MS', 10),fg='#3BA684', command=self.Buscar_presupuestos)
		self.presupuesto_anterior.bind('<Return>', self.Buscar_presupuestos)
		self.presupuesto_anterior.grid(row=1, column=3,padx=3, pady=3,)
		
		#Articulos del presupuestos
		labelproducto=Label(self.ventanaPresupuesto, text='Producto',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelproducto.grid(row=2, column=0,pady=3, padx=3)
		self.entryProd_presupuesto=Entry(self.ventanaPresupuesto,textvariable=self.producto,width=32,font=('Comic Sans MS', 10))
		self.entryProd_presupuesto.bind('<KeyRelease>',self.busq_list) 
		self.entryProd_presupuesto.grid(row=3, column=0,pady=3, padx=3)
		label_id_prod=Label(self.ventanaPresupuesto, text='Id Producto',bg='#C3C3C3',font=('Comic Sans MS', 10))
		label_id_prod.grid(row=2, column=1,pady=3, padx=3)
		self.entry_id=Entry(self.ventanaPresupuesto, textvariable=self.id_producto,font=('Comic Sans MS', 10),width=8, state='readonly',justify='center')
		self.entry_id.grid(row=3, column=1,pady=3, padx=3)
		self.list1=Listbox(self.ventanaPresupuesto,font=('Comic Sans MS', 10) )
		self.list1.config(width="50", height="12")
		self.list1.bind('<Return>',self.datos_para_presupuesto)
		self.lista_busq_prod(self.lista_prod())
		self.list1.grid(row=4, column=0,columnspan=2,pady=3, padx=3)
		
		self.l3=Label(self.ventanaPresupuesto, text='Cant.',bg='#C3C3C3',font=('Comic Sans MS', 10),justify='right')
		self.l3.grid(row=7, column=0,pady=3, padx=3, sticky='e', )
		self.e3=Entry(self.ventanaPresupuesto, textvariable=self.cant_presupuesto, width=12,font=('Comic Sans MS', 10))
		self.e3.bind('<Return>', self.agregar_al_presupuesto)
		self.e3.grid(row=7, column=1,pady=3, padx=3, sticky='w')

		self.l4=Label(self.ventanaPresupuesto, text='Precio',bg='#C3C3C3',font=('Comic Sans MS', 10),justify='right')
		self.l4.grid(row=8, column=0,pady=3, padx=3, sticky='e', )
		self.e4=Entry(self.ventanaPresupuesto, textvariable=self.precio_venta, width=12,font=('Comic Sans MS', 10))
		self.e4.bind('<Return>',self.agregar_al_presupuesto )
		self.e4.grid(row=8, column=1,pady=3, padx=3, sticky='w')

		#Agregar al presupuesto
		self.botonagregar_al_presupuesto=Button(self.ventanaPresupuesto,text='Agregar',font=('Comic Sans MS', 10),fg='#3BA684', command=self.agregar_al_presupuesto)
		self.botonagregar_al_presupuesto.bind('<Return>', self.agregar_al_presupuesto)
		self.botonagregar_al_presupuesto.grid(row=9, column=1,padx=3, pady=3,)

		#Recuperar presupuesto incompleto
		self.recuperar_presupuesto=Button(self.ventanaPresupuesto,text='Presupuesto incompleto',font=('Comic Sans MS', 10),fg='#3BA684', command=self.recuperar_presupuesto)
		self.recuperar_presupuesto.bind('<Return>', self.recuperar_presupuesto)
		self.recuperar_presupuesto.grid(row=3, column=2,padx=3, pady=3,)
			
		#Descartar presupuesto incompleto
		self.recuperar_presupuesto=Button(self.ventanaPresupuesto,text='Limpiar pantalla',font=('Comic Sans MS', 10),fg='#3BA684',command=self.descartar_presupuesto )
		self.recuperar_presupuesto.bind('<Return>', self.descartar_presupuesto)
		self.recuperar_presupuesto.grid(row=3, column=3,padx=3, pady=3,)

		#Tabla
		self.encabezado=['id_prod','producto','stock','precio_venta','pretotal']
		self.tablaPresupuesto=Treeview(self.ventanaPresupuesto, columns=self.encabezado, show='headings')
		self.tablaPresupuesto.column('id_prod', width=62,minwidth=62, anchor="center")
		self.tablaPresupuesto.column('producto', width=313,minwidth=313, stretch=True)
		self.tablaPresupuesto.column('stock', width=62,minwidth=62, anchor="center")
		self.tablaPresupuesto.column('precio_venta', width=125,minwidth=125, anchor="center")
		self.tablaPresupuesto.column('pretotal', width=125,minwidth=125, anchor="center")
		self.tablaPresupuesto.heading('id_prod', text='ID prod')
		self.tablaPresupuesto.heading('producto', text='Producto')
		self.tablaPresupuesto.heading('stock', text='Cant.')
		self.tablaPresupuesto.heading('precio_venta', text='Precio Unitario')  
		self.tablaPresupuesto.heading('pretotal', text='Importe') 
		self.tablaPresupuesto.bind('<Key-Delete>', self.eliminar_de_presupuesto)
		self.barra=Scrollbar(self.ventanaPresupuesto, orient="vertical", command=self.tablaPresupuesto.yview)
		self.tablaPresupuesto.configure(yscrollcommand=self.barra.set)
		self.barra.grid(row=4, column=6, sticky = 'NS',pady=10)
		self.tablaPresupuesto.grid(row=4, column=2,columnspan=4,padx=10, pady=10)
		
		#Montos
		self.label_sub=Label(self.ventanaPresupuesto, text='Sub-Total',bg='#C3C3C3',font=('Comic Sans MS', 10), )
		self.label_sub.grid(row=7, column=3,sticky='e')
		self.label_subpesos=Label(self.ventanaPresupuesto, text='$',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.label_subpesos.grid(row=7, column=4,sticky='w',)
		self.entry_subtotal=Entry(self.ventanaPresupuesto,textvariable=self.subtotal,width=12,font=('Comic Sans MS', 10),state='readonly')
		self.entry_subtotal.grid(row=7, column=4)
		self.labelDescuento=Label(self.ventanaPresupuesto, text='Porc. Descuento',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.labelDescuento.grid(row=8, column=3,sticky='e')
		self.label_porcentual=Label(self.ventanaPresupuesto, text='    %',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.label_porcentual.grid(row=8, column=4,sticky='w')
		self.entryPorcentaje=Entry(self.ventanaPresupuesto,textvariable=self.porcentaje_descuento,width=6,font=('Comic Sans MS', 10))
		self.entryPorcentaje.bind('<Tab>',self.descuento_presupuesto)
		self.entryPorcentaje.bind('<Return>',self.descuento_presupuesto)
		self.entryPorcentaje.grid(row=8, column=4,)
		self.labelMonto_descuento=Label(self.ventanaPresupuesto, text='Monto descuento',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.labelMonto_descuento.grid(row=9, column=3,sticky='e')
		self.label_pesos=Label(self.ventanaPresupuesto, text='$',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.label_pesos.grid(row=9, column=4,sticky='w',)
		self.entryDescuento=Entry(self.ventanaPresupuesto, text=self.descuento,width=12,font=('Comic Sans MS', 10))
		self.entryDescuento.bind('<Tab>',self.sumaTotales_presupuesto)
		self.entryDescuento.bind('<Return>',self.sumaTotales_presupuesto)
		self.entryDescuento.grid(row=9, column=4,)
		
		#Opción de envio
		self.envio_boton=Checkbutton(self.ventanaPresupuesto,text="Con envio",font=('Comic Sans MS', 10),bg='#C3C3C3',)
		self.envio_boton.config(command=self.boton_envio,variable=self.con_envio)
		self.envio_boton.grid(row=10, column=3,sticky='e')
		Label(self.ventanaPresupuesto, text='$',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right').grid(row=10, column=4,sticky='w',)
		self.envio_entry=Entry(self.ventanaPresupuesto,textvariable=self.envio,width=12,font=('Comic Sans MS', 10),state='readonly')
		self.envio_entry.bind('<Tab>',self.sumaTotales_presupuesto)
		self.envio_entry.grid(row=10, column=4)
		
		#Totales
		self.label_total=Label(self.ventanaPresupuesto, text='Total',bg='#C3C3C3',font=('Comic Sans MS', 10), )
		self.label_total.grid(row=11, column=3,sticky='e')
		self.label_totalpesos=Label(self.ventanaPresupuesto, text='$',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.label_totalpesos.grid(row=11, column=4,sticky='w',)
		self.entry_sumatotal=Entry(self.ventanaPresupuesto,textvariable=self.total_presupuesto,width=12,font=('Comic Sans MS', 10),bg='#C3C3C3')
		self.entry_sumatotal.config(state='readonly')
		self.entry_sumatotal.grid(row=11, column=4,)

		

		Label(self.ventanaPresupuesto,font=('Comic Sans MS', 10),bg='#C3C3C3', text='Datos de cuenta bancaria').grid(row=11, column=2,padx=3, pady=3,sticky='w')
		self.cbCuenta=Combobox(self.ventanaPresupuesto,font=('Comic Sans MS', 10),width=18, textvariable=self.titular)
		self.cbCuenta['values']=self.listado_cuenta()
		self.cbCuenta.bind("<<ComboboxSelected>>",self.lista_cliente)
		self.cbCuenta.grid(row=12, column=2,padx=3, pady=3,sticky='w')

		self.final=Button(self.ventanaPresupuesto,text='Guardar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.finalizar_presupuesto)
		self.final.bind('<Return>', self.finalizar_presupuesto)
		self.final.grid(row=12, column=4,padx=3, pady=3,rowspan=2)
		
		try:
			self.datos_en_tabla()
		except:
			pass
		finally:
			self.tablaPresupuesto.delete(*self.tablaPresupuesto.get_children())
		self.ventanaPresupuesto.mainloop()

#----------------Ventana Buscar presupuestos--------------
	def Buscar_presupuestos (self,event=None):
		self.ventanaBuscar_presupuestos=Toplevel()
		self.ventanaBuscar_presupuestos.title("Busqueda de presupuestos")
		self.ventanaBuscar_presupuestos.geometry("+400+100")
		self.ventanaBuscar_presupuestos.config(bg='#C3C3C3')
		self.ventanaBuscar_presupuestos.resizable(0,0)
		self.ventanaBuscar_presupuestos.transient(self.inicio)
		self.ventanaBuscar_presupuestos.grab_set()

		self.lbuscar_prto=Label(self.ventanaBuscar_presupuestos, text='Buscar por cliente',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=0, column=0, padx=3)
		self.entryBPrto=Entry(self.ventanaBuscar_presupuestos, textvariable=self.buscarPresupuesto,font=('Comic Sans MS', 10))
		self.entryBPrto.focus()
		self.entryBPrto.bind('<Return>',self.buscadorPresupuesto)
		self.entryBPrto.grid(row=1, column=0, padx=3, pady=3)
		self.entryBPrto.focus()
		self.botonBPrto=Button(self.ventanaBuscar_presupuestos, text='Buscar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.buscadorPresupuesto)
		self.botonBPrto.bind('<Return>',self.buscadorPresupuesto)
		self.botonBPrto.grid(row=1, column=1, padx=3, pady=3)
		self.botonNvoPrto=Button(self.ventanaBuscar_presupuestos, text='Nuevo Prto',font=('Comic Sans MS', 10),fg='#3BA684', command=self.Presupuesto). grid(row=1, column=3, padx=3, pady=3)
	
		#Tabla Presupuestos
		self.encabezado_ptro=['id','cliente', 'fecha', 'total','estado', 'envio']
		self.tablaCtePrto=Treeview(self.ventanaBuscar_presupuestos, columns=self.encabezado_ptro , show='headings',)
		self.tablaCtePrto.bind('<<TreeviewSelect>>',self.items_prto)
		self.tablaCtePrto.column('id', width=50,minwidth=50, anchor="center")
		self.tablaCtePrto.column('cliente', width=125,minwidth=125, anchor="center")
		self.tablaCtePrto.column('fecha', width=125,minwidth=125, anchor="center")
		self.tablaCtePrto.column('total', width=125,minwidth=125, anchor="center")
		self.tablaCtePrto.column('estado', width=125,minwidth=125, anchor="center")
		self.tablaCtePrto.column('envio', width=100,minwidth=100, anchor="center")
		self.tablaCtePrto.heading('id', text='ID')
		self.tablaCtePrto.heading('cliente', text='Cliente')
		self.tablaCtePrto.heading('fecha', text='Fecha del Prto.')
		self.tablaCtePrto.heading('total', text='Total del Prto.')
		self.tablaCtePrto.heading('estado', text='Estado')
		self.tablaCtePrto.heading('envio', text='Envío')
		self.barraCtePrto=Scrollbar(self.ventanaBuscar_presupuestos, orient="vertical", command=self.tablaCtePrto.yview)
		self.tablaCtePrto.configure(yscrollcommand=self.barraCtePrto.set)
		self.barraCtePrto.grid(row=2, column=4, sticky = 'NS')
		self.tablaCtePrto.grid(row=2, column=0,columnspan=4,padx=10)

		#Detalle del presupuesto seleccionado
		self.listaPrto=Label(self.ventanaBuscar_presupuestos, text='Lista de productos del\npresupuesto seleccionado',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=1, column=6, columnspan=3)
		self.encabezado_detallePto=['producto','stock']
		self.tablaListaPrto=Treeview(self.ventanaBuscar_presupuestos, columns=self.encabezado_detallePto, show='headings',)
		self.tablaListaPrto.bind('<<TreeviewSelect>>',)
		self.tablaListaPrto.column('producto', width=313,minwidth=313, anchor="center")
		self.tablaListaPrto.column('stock', width=62,minwidth=62, anchor="center")
		self.tablaListaPrto.heading('producto', text='Producto')
		self.tablaListaPrto.heading('stock', text='Cant.')
		self.barraListaPrto=Scrollbar(self.ventanaBuscar_presupuestos, orient="vertical", command=self.tablaListaPrto.yview)
		self.tablaListaPrto.configure(yscrollcommand=self.barraListaPrto.set)
		self.barraListaPrto.grid(row=2, column=8, sticky = 'NS')
		self.tablaListaPrto.grid(row=2, column=6,columnspan=2,padx=10)

		#Boton confirmación de presupuesto
		self.botonConfirmar=Button(self.ventanaBuscar_presupuestos, text='Confirmar presupuesto',font=('Comic Sans MS', 10),fg='#3BA684', command=self.Pedidos). grid(row=5, column=4,columnspan=3, padx=3, pady=3)

		self.ventanaBuscar_presupuestos.mainloop()

#----------------Ventana pedidos-------------------
	def Pedidos(self,event=None):
		self.ventanaPedidos = Toplevel(inicio)
		self.ventanaPedidos.title("Ventas")
		self.ventanaPedidos.geometry("+400+100")
		self.ventanaPedidos.config(bg='#C3C3C3')
		self.ventanaPedidos.resizable(0,0)
		self.ventanaPedidos.transient(self.inicio)
		self.ventanaPedidos.grab_set()
	
		self.id_producto.set('')
		self.cliente.set(''),
		self.pagos.set(''),
		self.presupuesto.set(''),
		self.cant_pedido.set('')
		self.subtotal.set(''),
		self.porcentaje_descuento.set(0.0)
		self.descuento.set(0.0)		
		self.envio.set(0.0)
		self.total_pedido.set('')
		self.recargo.set('')
		
		self.titulo_pedido=Label(self.ventanaPedidos, text='Venta de productos',bg='#C3C3C3',font=('Comic Sans MS', 16)).grid(row=0,column=0, columnspan=6,pady=10, padx=10)

		#Cliente
		self.lCliente=Label(self.ventanaPedidos, text='Cliente',bg='#C3C3C3',font=('Comic Sans MS', 10)).grid(row=2,column=0, pady=3, padx=3)
		self.cbCliente=Combobox(self.ventanaPedidos,font=('Comic Sans MS', 10),width=18, textvariable=self.cliente)
		self.cbCliente['values']=self.lista_cliente()
		self.cbCliente.bind("<<ComboboxSelected>>",self.lista_cliente)
		self.cbCliente.focus()
		self.cbCliente.grid(row=3,column=0, pady=3, padx=3)

		#Fecha
		self.lFecha=Label(self.ventanaPedidos, text='Fecha',bg='#C3C3C3',font=('Comic Sans MS', 10)).grid(row=2,column=1, pady=3, padx=3)
		self.eFechaActual=Label(self.ventanaPedidos,text=self.fecha,bg='#C3C3C3',font=('Comic Sans MS', 10)).grid(row=3,column=1, pady=3, padx=3)
	
		#Pago
		self.pagolabel=Label(self.ventanaPedidos, text='Medio de pago',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.pagolabel.grid(row=2, column=2,padx=3, pady=3)
		self.pagocb1=Combobox(self.ventanaPedidos,font=('Comic Sans MS', 10), textvariable=self.pagos, width=15)
		self.pagocb1['values']=self.lista_medios()
		self.pagocb1.bind("<<ComboboxSelected>>",self.boton_recargo)
		self.pagocb1.grid(row=3, column=2,padx=10, pady=3,)

		#Presupuestos sin confirmar
		self.prto_label=Label(self.ventanaPedidos, text='Presupestos sin confirmar',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.prto_label.grid(row=2, column=3,padx=3, pady=3)
		self.prto_cb=Combobox(self.ventanaPedidos,font=('Comic Sans MS', 10), textvariable=self.presupuesto)
		self.prto_cb.bind("<<ComboboxSelected>>",self.prto_en_tabla)
		self.prto_cb['values']=self.prto_sin_conf()
		self.prto_cb.grid(row=3, column=3,padx=3, pady=3,)

		self.boton_pedido_incompleto=Button(self.ventanaPedidos, text='Pedido\nincompleto',font=('Comic Sans MS', 10),fg='#3BA684',command=self.recuperar_pedido)
		self.boton_pedido_incompleto.bind('<Return>',self.recuperar_pedido)
		self.boton_pedido_incompleto.grid(row=5, column=3,  padx=3, pady=3)
		self.boton_eliminar_pedido=Button(self.ventanaPedidos, text='Limpiar pantalla',font=('Comic Sans MS', 10),fg='#3BA684',command=self.descartar_pedido)
		self.boton_eliminar_pedido.bind('<Return>',self.descartar_pedido)
		self.boton_eliminar_pedido.grid(row=5, column=4,  padx=3, pady=3, columnspan=2)

		#Articulos del Pedido
		labelproducto=Label(self.ventanaPedidos, text='Producto',bg='#C3C3C3',font=('Comic Sans MS', 10))
		labelproducto.grid(row=4, column=0,pady=3, padx=10)
		self.entryProd_pedido=Entry(self.ventanaPedidos,textvariable=self.producto,width=32,font=('Comic Sans MS', 10))
		self.entryProd_pedido.bind('<KeyRelease>',self.busq_list) 
		self.entryProd_pedido.grid(row=5, column=0,pady=3, padx=3)
		label_id_prod=Label(self.ventanaPedidos, text='Id Producto',bg='#C3C3C3',font=('Comic Sans MS', 10))
		label_id_prod.grid(row=4, column=1,pady=3, padx=3)
		self.entry_id=Entry(self.ventanaPedidos, textvariable=self.id_producto,font=('Comic Sans MS', 10),width=8, state='readonly',justify='center')
		self.entry_id.grid(row=5, column=1,pady=3, padx=3)
		self.list1=Listbox(self.ventanaPedidos,font=('Comic Sans MS', 10) )
		self.list1.config(width="50", height="12")
		self.list1.bind('<Return>',self.datos_para_pedido)
		self.lista_busq_prod(self.lista_prod())
		self.list1.grid(row=6, column=0,columnspan=2,pady=3, padx=3)

		#Cantidad de articulos del pedido
		self.cant_pedido_label=Label(self.ventanaPedidos, text='Cant.',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.cant_pedido_label.grid(row=7, column=0,pady=3, padx=3,)
		self.cant_pedido_entry=Entry(self.ventanaPedidos, textvariable=self.cant_pedido, width=12,font=('Comic Sans MS', 10))
		self.cant_pedido_entry.bind('<Return>',self.agregar_al_pedido)
		self.cant_pedido_entry.grid(row=7, column=0,pady=3, padx=3,sticky='e')

		#Precio del producto(modificable para la salida, pero no en la base de datos)
		self.precio_label=Label(self.ventanaPedidos, text='Precio',bg='#C3C3C3',font=('Comic Sans MS', 10),justify='right')
		self.precio_label.grid(row=8, column=0,pady=3, padx=3,  )
		self.precio_entry=Entry(self.ventanaPedidos, textvariable=self.precio_venta, width=12,font=('Comic Sans MS', 10))
		self.precio_entry.bind('<Return>',)
		self.precio_entry.grid(row=8, column=0,pady=3, padx=3, sticky='e')

		self.botonAgregar=Button(self.ventanaPedidos, text='Agregar artículo',font=('Comic Sans MS', 10),fg='#3BA684',command=self.agregar_al_pedido)
		self.botonAgregar.bind('<Return>',self.agregar_al_pedido)
		self.botonAgregar.grid(row=8, column=1,  padx=3, pady=3)

		#Tabla de productos del pedido
		self.encabezado=['id_prod','producto','stock','precio_venta','pretotal']
		self.tablaPedido=ttk.Treeview(self.ventanaPedidos, columns=self.encabezado, show='headings')
		self.tablaPedido.column('id_prod', width=62,minwidth=62, anchor="center")
		self.tablaPedido.column('producto', width=312,minwidth=312, anchor="center", stretch=True)
		self.tablaPedido.column('stock', width=62,minwidth=62, anchor="center")
		self.tablaPedido.column('precio_venta', width=125,minwidth=125, anchor="center")
		self.tablaPedido.column('pretotal', width=125,minwidth=125, anchor="center")
		self.tablaPedido.heading('id_prod', text='ID prod')
		self.tablaPedido.heading('producto', text='Producto')
		self.tablaPedido.heading('stock', text='Cant.')
		self.tablaPedido.heading('precio_venta', text='P. Unit.')   
		self.tablaPedido.heading('pretotal', text='Importe')   
		self.tablaPedido.bind('<Key-Delete>', self.eliminar_de_pedido)
		self.barraPedido=Scrollbar(self.ventanaPedidos, orient="vertical", command=self.tablaPedido.yview)
		self.tablaPedido.configure(yscrollcommand=self.barraPedido.set)
		self.barraPedido.grid(row=6, column=6, sticky = 'NS',pady=10)
		self.tablaPedido.grid(row=6, column=2,columnspan=4,padx=10, pady=10,sticky='w')

		#Subtotal, descuento y total
		self.label_sub=Label(self.ventanaPedidos, text='Sub-Total',bg='#C3C3C3',font=('Comic Sans MS', 10), )
		self.label_sub.grid(row=7, column=2,padx=10, sticky='w')
		self.label_subpesos=Label(self.ventanaPedidos, text='$',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.label_subpesos.grid(row=7, column=2,sticky='e',)
		self.entry_subtotal=Entry(self.ventanaPedidos,textvariable=self.subtotal,width=11,font=('Comic Sans MS', 10),state='readonly')
		self.entry_subtotal.grid(row=7, column=3,padx=10, sticky='w')
		self.labelDescuento=Label(self.ventanaPedidos, text='Porc. Descuento',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.labelDescuento.grid(row=8, column=2,padx=10, sticky='w')
		self.label_porcentual=Label(self.ventanaPedidos, text=' %',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='left')
		self.label_porcentual.grid(row=8, column=2,sticky='e')
		self.entryPorcentaje=Entry(self.ventanaPedidos,textvariable=self.porcentaje_descuento,width=11,font=('Comic Sans MS', 10))
		self.entryPorcentaje.bind('<Tab>',self.descuento_presupuesto)
		self.entryPorcentaje.bind('<Return>',self.descuento_presupuesto)
		self.entryPorcentaje.grid(row=8, column=3,padx=10, sticky='w')
		self.labelMonto_descuento=Label(self.ventanaPedidos, text='Monto descuento',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right')
		self.labelMonto_descuento.grid(row=9, column=2,padx=10, sticky='w')
		self.label_pesos=Label(self.ventanaPedidos, text='$',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='left')
		self.label_pesos.grid(row=9, column=2,sticky='e',)
		self.entryDescuento=Entry(self.ventanaPedidos, text=self.descuento,width=11,font=('Comic Sans MS', 10))
		self.entryDescuento.bind('<Tab>',self.sumaTotales_pedido)
		self.entryDescuento.bind('<Return>',self.sumaTotales_pedido)
		self.entryDescuento.grid(row=9, column=3,padx=10, sticky='w')

		#Opción de envio
		self.envio_boton=Checkbutton(self.ventanaPedidos,text="Con envio",font=('Comic Sans MS', 10),bg='#C3C3C3',)
		self.envio_boton.config(command=self.boton_envio,variable=self.con_envio)
		self.envio_boton.grid(row=10, column=2,padx=10, sticky='w')
		Label(self.ventanaPedidos, text='$',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right').grid(row=10, column=2,sticky='e',)
		self.envio_entry=Entry(self.ventanaPedidos,textvariable=self.envio,width=11,font=('Comic Sans MS', 10),state='readonly')
		self.envio_entry.bind('<Tab>',self.sumaTotales_pedido)
		self.envio_entry.grid(row=10, column=3,padx=10, sticky='w')

		#Total
		self.label_total=Label(self.ventanaPedidos, text='Total',bg='#C3C3C3',font=('Comic Sans MS', 10), )
		self.label_total.grid(row=7, column=3,padx=10, sticky='e')
		self.label_totalpesos=Label(self.ventanaPedidos, text='     $',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='left')
		self.label_totalpesos.grid(row=7, column=4,sticky='w',)
		self.entry_sumatotal=Entry(self.ventanaPedidos,textvariable=self.total_pedido,width=11,font=('Comic Sans MS', 10),bg='#C3C3C3')
		self.entry_sumatotal.config(state='readonly')
		self.entry_sumatotal.grid(row=7, column=4,padx=10, sticky='e',)

		#Opción de recargo
		self.recargo_boton=Checkbutton(self.ventanaPedidos,text="Recargo",font=('Comic Sans MS', 10),bg='#C3C3C3',)
		self.recargo_boton.config(command=self.boton_recargo,variable=self.con_recargo)
		self.recargo_boton.grid(row=8, column=3,padx=10, sticky='e')
		Label(self.ventanaPedidos, text='     $',bg='#C3C3C3',font=('Comic Sans MS', 10), justify='right').grid(row=8, column=4,sticky='w',)
		self.recargo_entry=Entry(self.ventanaPedidos,textvariable=self.recargo,font=('Comic Sans MS', 10),state='readonly',width=11)
		self.recargo_entry.bind('<Tab>',self.sumaTotales_pedido)
		self.recargo_entry.grid(row=8, column=4,padx=10, sticky='e')

		#Boton confirmación de pedido.
		self.botonConfirmar=Button(self.ventanaPedidos, text='Confirmar\nventa',font=('Comic Sans MS', 10),fg='#3BA684', command=self.comando_finalizar). grid(row=10, column=4, padx=3, pady=10)
				
		self.ventanaPedidos.mainloop()

#----------------Ventana Buscar pedidos--------------
	def Buscar_pedidos (self,event=None):
		self.ventanaBuscar_pedidos=Toplevel()
		self.ventanaBuscar_pedidos.title("Busqueda de pedido")
		self.ventanaBuscar_pedidos.geometry("+400+100")
		self.ventanaBuscar_pedidos.config(bg='#C3C3C3')
		self.ventanaBuscar_pedidos.resizable(0,0)
		self.ventanaBuscar_pedidos.transient(self.inicio)
		self.ventanaBuscar_pedidos.grab_set()

		self.lbuscar_pdo=Label(self.ventanaBuscar_pedidos, text='Buscar por cliente',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=0, column=0, padx=3)
		self.entryBPdo=Entry(self.ventanaBuscar_pedidos, textvariable=self.buscarPedido,font=('Comic Sans MS', 10))
		self.entryBPdo.focus()
		self.entryBPdo.bind('<Return>',self.buscadorPedido)
		self.entryBPdo.grid(row=1, column=0, padx=3, pady=3)
		self.entryBPdo.focus()
		self.botonBPdo=Button(self.ventanaBuscar_pedidos, text='Buscar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.buscadorPedido)
		self.botonBPdo.bind('<Return>',self.buscadorPedido)
		self.botonBPdo.grid(row=1, column=1, padx=3, pady=3)
		self.botonNvoPdo=Button(self.ventanaBuscar_pedidos, text='Nuevo Prto',font=('Comic Sans MS', 10),fg='#3BA684', command=self.Pedidos). grid(row=1, column=3, padx=3, pady=3)
	
		#Tabla Presupuestos
		self.encabezado_pdo=['id','cliente', 'fecha', 'total','estado', 'envio']
		self.tablaCtePdo=Treeview(self.ventanaBuscar_pedidos, columns=self.encabezado_pdo , show='headings',)
		self.tablaCtePdo.bind('<<TreeviewSelect>>',self.items_pdo)
		self.tablaCtePdo.column('id', width=50,minwidth=50, anchor="center")
		self.tablaCtePdo.column('cliente', width=125,minwidth=125, anchor="center")
		self.tablaCtePdo.column('fecha', width=125, anchor="center")
		self.tablaCtePdo.column('total', width=125,minwidth=125, anchor="center")
		self.tablaCtePdo.column('estado', width=125,minwidth=125, anchor="center")
		self.tablaCtePdo.column('envio', width=100,minwidth=100, anchor="center")
		self.tablaCtePdo.heading('id', text='ID')
		self.tablaCtePdo.heading('cliente', text='Cliente')
		self.tablaCtePdo.heading('fecha', text='Fecha del Pdo.')
		self.tablaCtePdo.heading('total', text='Total del Pdo.')
		self.tablaCtePdo.heading('estado', text='Estado')
		self.tablaCtePdo.heading('envio', text='Envío')
		self.barraCtePdo=Scrollbar(self.ventanaBuscar_pedidos, orient="vertical", command=self.tablaCtePdo.yview)
		self.tablaCtePdo.configure(yscrollcommand=self.barraCtePdo.set)
		self.barraCtePdo.grid(row=2, column=4, sticky = 'NS')
		self.tablaCtePdo.grid(row=2, column=0,columnspan=4,padx=10)

		#Detalle del presupuesto seleccionado
		self.listaPdo=Label(self.ventanaBuscar_pedidos, text='Lista de productos del\npedido seleccionado',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=1, column=6, columnspan=3)
		self.encabezado_detallePdo=['producto','stock']
		self.tablaListaPdo=Treeview(self.ventanaBuscar_pedidos, columns=self.encabezado_detallePdo, show='headings',)
		self.tablaListaPdo.bind('<<TreeviewSelect>>',)
		self.tablaListaPdo.column('producto', width=312,minwidth=312, anchor="center")
		self.tablaListaPdo.column('stock', width=62,minwidth=62, anchor="center")
		self.tablaListaPdo.heading('producto', text='Producto')
		self.tablaListaPdo.heading('stock', text='Cant.')
		self.barraListaPdo=Scrollbar(self.ventanaBuscar_pedidos, orient="vertical", command=self.tablaListaPdo.yview)
		self.tablaListaPdo.configure(yscrollcommand=self.barraListaPdo.set)
		self.barraListaPdo.grid(row=2, column=8, sticky = 'NS')
		self.tablaListaPdo.grid(row=2, column=6,columnspan=2,padx=10)

		self.ventanaBuscar_pedidos.mainloop()

#----------------Ventana Comprovantes de compra--------------
	def Comprobantes (self,event=None):
		self.ventanaComprobantes=Toplevel()
		self.ventanaComprobantes.title("Comprobantes")
		self.ventanaComprobantes.geometry("+400+100")
		self.ventanaComprobantes.config(bg='#C3C3C3')
		self.ventanaComprobantes.resizable(0,0)
		self.ventanaComprobantes.transient(self.inicio)
		self.ventanaComprobantes.grab_set()

		self.lbuscar=Label(self.ventanaComprobantes, text='Buscar por proveedor',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=0, column=0, padx=3)
		self.entryBCte=Entry(self.ventanaComprobantes, textvariable=self.buscarComprobante,font=('Comic Sans MS', 10))
		self.entryBCte.focus()
		self.entryBCte.bind('<Return>',self.buscadorComprobantes)
		self.entryBCte.grid(row=1, column=0, padx=3, pady=3)
		self.entryBCte.focus()
		self.botonBuscar=Button(self.ventanaComprobantes, text='Buscar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.buscadorComprobantes)
		self.botonBuscar.bind('<Return>',self.buscadorComprobantes)
		self.botonBuscar.grid(row=1, column=1, padx=3, pady=3)
		self.botonNuevo=Button(self.ventanaComprobantes, text='Nueva Compra',font=('Comic Sans MS', 10),fg='#3BA684', command=self.Compras). grid(row=1, column=3, padx=3, pady=3)
	
		#Tabla Comprobantes
		self.encabezado=['id','proveedor','tipo', 'numero', 'fecha', 'total']
		self.tablaCte=Treeview(self.ventanaComprobantes, columns=self.encabezado, show='headings',)
		self.tablaCte.bind('<<TreeviewSelect>>',self.items_comprobante)
		self.tablaCte.column('id', width=37,minwidth=37, anchor="center")
		self.tablaCte.column('proveedor', width=125,minwidth=125, anchor="center")
		self.tablaCte.column('tipo', width=125,minwidth=125, anchor="center")
		self.tablaCte.column('numero', width=125,minwidth=125, anchor="center")
		self.tablaCte.column('fecha', width=125,minwidth=125, anchor="center")
		self.tablaCte.column('total', width=125,minwidth=125, anchor="center")
		self.tablaCte.heading('id', text='ID')
		self.tablaCte.heading('proveedor', text='Proveedor')
		self.tablaCte.heading('tipo', text='Tipo de Cte.')
		self.tablaCte.heading('numero', text='N° de Cte.')
		self.tablaCte.heading('fecha', text='Fecha del Cte.')
		self.tablaCte.heading('total', text='Total del Cte.')
		self.barraCte=Scrollbar(self.ventanaComprobantes, orient="vertical", command=self.tablaCte.yview)
		self.tablaCte.configure(yscrollcommand=self.barraCte.set)
		self.barraCte.grid(row=2, column=4, sticky = 'NS')
		self.tablaCte.grid(row=2, column=0,columnspan=4,padx=10)

		#Detalle del comprobante seleccionado
		self.tituliLista=Label(self.ventanaComprobantes, text='Lista de productos del\ncomprobante seleccionado',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=1, column=6, columnspan=3)
		self.encabezado=['producto','stock']
		self.tablaLista=Treeview(self.ventanaComprobantes, columns=self.encabezado, show='headings',)
		self.tablaLista.column('producto', width=312,minwidth=312, anchor="center")
		self.tablaLista.column('stock', width=62,minwidth=62, anchor="center")
		self.tablaLista.heading('producto', text='Producto')
		self.tablaLista.heading('stock', text='Cant.')
		self.barraLista=Scrollbar(self.ventanaComprobantes, orient="vertical", command=self.tablaLista.yview)
		self.tablaLista.configure(yscrollcommand=self.barraLista.set)
		self.barraLista.grid(row=2, column=8, sticky = 'NS')
		self.tablaLista.grid(row=2, column=6,columnspan=2,padx=10)
		
		self.ventanaComprobantes.mainloop()

#----------------Ventana Configurar mail de envio---------
	def Config_mail(self,event=None):
		self.ventanaConfig_mail = Toplevel()
		self.ventanaConfig_mail.title("Gestión de cuenta de Mail")
		self.ventanaConfig_mail.geometry("+600+200")
		self.ventanaConfig_mail.config(bg='#C3C3C3')
		self.ventanaConfig_mail.resizable(0,0)
		self.ventanaConfig_mail.transient(self.inicio)
		self.ventanaConfig_mail.grab_set()

		self.mail_activo=StringVar(value=self.mostrar_mail_master())
			
		titulo=Label(self.ventanaConfig_mail, text='Solo utilizar @gmail.com',bg='#C3C3C3', font=('Comic Sans MS', 10)).grid(row=0, column=1,pady=3, padx=3 )

		l1=Label(self.ventanaConfig_mail, text='Mail',bg='#C3C3C3',font=('Comic Sans MS', 10))
		l1.grid(row=1, column=1,pady=3, padx=3)
		self.master_mail_cb=Combobox(self.ventanaConfig_mail, textvariable=self.mail_principal,width=34,font=('Comic Sans MS', 10))
		self.master_mail_cb['values']=self.lista_mail()
		self.master_mail_cb.bind("<<ComboboxSelected>>",self.mostrar_datos_mail)
		self.master_mail_cb.focus()
		self.master_mail_cb.grid(row=2, column=1,pady=3, padx=3)
			
		l2=Label(self.ventanaConfig_mail, text='Contraseña',bg='#C3C3C3',font=('Comic Sans MS', 10))
		l2.grid(row=3, column=1,pady=3, padx=3)
		self.pass_entry=Entry(self.ventanaConfig_mail,textvariable=self.contrasenha, width=37,font=('Comic Sans MS', 10),show='*')
		self.pass_entry.grid(row=4, column=1,pady=3, padx=3)

		l3=Label(self.ventanaConfig_mail, text='Mail fijado',bg='#C3C3C3',font=('Comic Sans MS', 10))
		l3.grid(row=6, column=1,pady=3, padx=3)
		self.mail_activo_entry=Entry(self.ventanaConfig_mail,textvariable=self.mail_activo, width=37,font=('Comic Sans MS', 10),state='readonly')
		self.mail_activo_entry.grid(row=7, column=1,pady=3, padx=3)

		botonAgregar=Button(self.ventanaConfig_mail, text='Agregar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.agregar_mail).grid(row=10, column=1, padx=3, pady=3,sticky='w')
		botonModificar=Button(self.ventanaConfig_mail, text='Modificar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.modificar_mail).grid(row=10, column=1,padx=3, pady=3,sticky='ns')
		botonEliminar=Button(self.ventanaConfig_mail, text='Eliminar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.eliminar_mail).grid(row=10, column=1, padx=3, pady=3,sticky='e')
		botonFijar=Button(self.ventanaConfig_mail, text='Fijar mail',font=('Comic Sans MS', 10),fg='#3BA684',command=self.activar_mail).grid(row=11, column=1, padx=3, pady=3,)

		self.ventanaConfig_mail.mainloop()

#----------------Ventana Estados--------------------------
	def Estados(self,event=None):
		self.ventanaEstados=Toplevel()
		self.ventanaEstados.title("Estados")
		self.ventanaEstados.geometry("+400+100")
		self.ventanaEstados.config(bg='#C3C3C3')
		self.ventanaEstados.resizable(0,0)
		self.ventanaEstados.transient(self.inicio)
		self.ventanaEstados.grab_set()

		self.buscarEstados.set('')
		self.opcion.set(0)
		self.estado_presupuesto.set(0)
		self.estado_pedido.set(0)

		#Busqueda
		Label(self.ventanaEstados, text='Busqueda',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=0, column=0, padx=3, pady=3)
		self.busca_estado=Entry(self.ventanaEstados, textvariable=self.buscarEstados, font=('Comic Sans MS', 10))
		self.busca_estado.bind('<Return>', self.config_busqueda)
		self.busca_estado.focus()
		self.busca_estado.grid(row=1, column=0, padx=3, pady=3, rowspan=2)
		self.id_radio=Radiobutton(self.ventanaEstados, text='ID',font=('Comic Sans MS', 10),bg='#C3C3C3', variable=self.opcion, value=1,command=self.config_busqueda)
		self.id_radio.bind('<Return>', self.config_busqueda)
		self.id_radio.grid(row=1, column=1, padx=3, pady=3, sticky='w')
		self.cliente_radio=Radiobutton(self.ventanaEstados, text='Cliente',font=('Comic Sans MS', 10),bg='#C3C3C3',variable=self.opcion, value=2,command=self.config_busqueda)
		self.cliente_radio.bind('<Return>', self.config_busqueda)
		self.cliente_radio.grid(row=2, column=1, padx=3, pady=3, sticky='w')

		#Tabla Presupuestos
		Label(self.ventanaEstados, text='Presupuestos',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=4, column=0, padx=3, pady=3)
		self.encabezado_ptro=['id','cliente', 'fecha', 'total','estado', 'envio']
		self.tablaCtePrto=Treeview(self.ventanaEstados, columns=self.encabezado_ptro , show='headings',)
		self.tablaCtePrto.bind('<<TreeviewSelect>>',self.selecion_presupuesto)
		self.tablaCtePrto.column('id', width=50,minwidth=50, anchor="center")
		self.tablaCtePrto.column('cliente', width=125,minwidth=125, anchor="center")
		self.tablaCtePrto.column('fecha', width=125,minwidth=125, anchor="center")
		self.tablaCtePrto.column('total', width=125,minwidth=125, anchor="center")
		self.tablaCtePrto.column('estado', width=125,minwidth=125, anchor="center")
		self.tablaCtePrto.column('envio', width=100,minwidth=100, anchor="center")
		self.tablaCtePrto.heading('id', text='ID')
		self.tablaCtePrto.heading('cliente', text='Cliente')
		self.tablaCtePrto.heading('fecha', text='Fecha del Prto.')
		self.tablaCtePrto.heading('total', text='Total del Prto.')
		self.tablaCtePrto.heading('estado', text='Estado')
		self.tablaCtePrto.heading('envio', text='Envío')
		self.barraCtePrto=Scrollbar(self.ventanaEstados, orient="vertical", command=self.tablaCtePrto.yview)
		self.tablaCtePrto.configure(yscrollcommand=self.barraCtePrto.set)
		self.barraCtePrto.grid(row=5, column=4, sticky = 'NS',rowspan=4)
		self.tablaCtePrto.grid(row=5, column=0,columnspan=4,padx=10, rowspan=4)

		#Estados Presupuestos
		Label(self.ventanaEstados, text='Estados de presupuestos',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=4, column=5, padx=3, pady=3)
		self.confirmar_radio=Radiobutton(self.ventanaEstados, text='Confirmar',font=('Comic Sans MS', 10),bg='#C3C3C3', variable=self.estado_presupuesto, value=1,state='disabled')
		self.confirmar_radio.grid(row=5, column=5, padx=3, pady=3, sticky='w')
		self.reconsultado_radio=Radiobutton(self.ventanaEstados, text='Reconsultado',font=('Comic Sans MS', 10),bg='#C3C3C3',variable=self.estado_presupuesto, value=2,state='disabled')
		self.reconsultado_radio.grid(row=6, column=5, padx=3, pady=3, sticky='w')
		self.cancelar_radio=Radiobutton(self.ventanaEstados, text='Cancelar',font=('Comic Sans MS', 10),bg='#C3C3C3',variable=self.estado_presupuesto, value=3,state='disabled')
		self.cancelar_radio.grid(row=7, column=5, padx=3, pady=3, sticky='w')

		botonCambiar=Button(self.ventanaEstados, text='Cambiar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.cambiar_presupuesto).grid(row=8, column=5, padx=3, pady=3,)
		
		#Espacio entre tablas
		Label(self.ventanaEstados, text='',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=10, column=0, padx=3, pady=3, )
		Separator(self.ventanaEstados, orient='horizontal').grid(row=10, column=0, padx=10, pady=10, columnspan=7,sticky="EW")

		#Tabla Presupuestos
		Label(self.ventanaEstados, text='Pedidos',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=11, column=0, padx=3, pady=3)
		self.encabezado_pdo=['id','cliente', 'fecha', 'total','estado', 'envio']
		self.tablaCtePdo=Treeview(self.ventanaEstados, columns=self.encabezado_pdo , show='headings',)
		self.tablaCtePdo.bind('<<TreeviewSelect>>',self.selecion_pedido)
		self.tablaCtePdo.column('id', width=50,minwidth=50, anchor="center")
		self.tablaCtePdo.column('cliente', width=125,minwidth=125, anchor="center")
		self.tablaCtePdo.column('fecha', width=125,minwidth=125, anchor="center")
		self.tablaCtePdo.column('total', width=125,minwidth=125, anchor="center")
		self.tablaCtePdo.column('estado', width=125,minwidth=125, anchor="center")
		self.tablaCtePdo.column('envio', width=100,minwidth=100, anchor="center")
		self.tablaCtePdo.heading('id', text='ID')
		self.tablaCtePdo.heading('cliente', text='Cliente')
		self.tablaCtePdo.heading('fecha', text='Fecha del Pdo.')
		self.tablaCtePdo.heading('total', text='Total del Pdo.')
		self.tablaCtePdo.heading('estado', text='Estado')
		self.tablaCtePdo.heading('envio', text='Envío')
		self.barraCtePdo=Scrollbar(self.ventanaEstados, orient="vertical", command=self.tablaCtePdo.yview)
		self.tablaCtePdo.configure(yscrollcommand=self.barraCtePdo.set)
		self.barraCtePdo.grid(row=12, column=4, sticky = 'NS',rowspan=4)
		self.tablaCtePdo.grid(row=12, column=0,columnspan=4,padx=10,rowspan=4)

		#Estados Pedidos
		Label(self.ventanaEstados, text='Estados de Pedidos',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=11, column=5, padx=3, pady=3)
		self.retirado_radio=Radiobutton(self.ventanaEstados, text='Retirado',font=('Comic Sans MS', 10),bg='#C3C3C3', variable=self.estado_pedido, value=1, state='disabled')
		self.retirado_radio.grid(row=12, column=5, padx=3, pady=3, sticky='w')
		self.enviado_radio=Radiobutton(self.ventanaEstados, text='Enviado',font=('Comic Sans MS', 10),bg='#C3C3C3',variable=self.estado_pedido, value=2, state='disabled')
		self.enviado_radio.grid(row=13, column=5, padx=3, pady=3, sticky='w')

		botonCambiar=Button(self.ventanaEstados, text='Cambiar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.cambiar_pedido).grid(row=14, column=5, padx=3, pady=3,)
		
		self.ventanaEstados.mainloop()

#----------------Ventana estados de cuentas------------------
	def Estados_cuentas(self):
		self.ventanaEstados_cuentas=Toplevel()
		self.ventanaEstados_cuentas.title('Estados de cuentas')
		self.ventanaEstados_cuentas.geometry('+500+50')#+500+50 ubicación de la ventana en la pantalla
		self.ventanaEstados_cuentas.config(bg='#C3C3C3')
		self.ventanaEstados_cuentas.resizable(width=0, height=0)
		self.ventanaEstados_cuentas.transient(self.inicio)
		self.ventanaEstados_cuentas.grab_set()

		self.rango_periodos.set('Todos')
				
		Label(self.ventanaEstados_cuentas, text='Total de cuentas',font=('Comic Sans MS', 20),bg='#C3C3C3').grid(row=0, column=0, padx=3, pady=3, columnspan=2)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 20),bg='#C3C3C3').grid(row=1, column=0, padx=3, pady=3,sticky='w')
		self.totales_cuentas=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly', textvariable=self.total_cuentas, justify='center')
		self.totales_cuentas.grid(row=1, column=0, padx=3, pady=3, columnspan=2)

		Label(self.ventanaEstados_cuentas, text='Periodo',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=0, column=2, padx=3, pady=3, sticky='s')
		self.periodo=Combobox(self.ventanaEstados_cuentas, textvariable=self.rango_periodos, width=18)
		self.periodo['values']=self.periodos_cuentas()
		self.periodo.current(0)
		self.periodo.bind('<<ComboboxSelected>>',self.totales_cuenta)
		self.periodo.grid(row=1, column=2, padx=3, pady=3,sticky='n')

		Label(self.ventanaEstados_cuentas, text='Tipo de cuenta',font=('Comic Sans MS', 16),bg='#C3C3C3').grid(row=2, column=0, padx=10, pady=3,)
		Label(self.ventanaEstados_cuentas, text='Efectivo',font=('Comic Sans MS', 12),bg='#C3C3C3').grid(row=3, column=0, padx=10, pady=3,)
		Label(self.ventanaEstados_cuentas, text='Transferencia',font=('Comic Sans MS', 12),bg='#C3C3C3').grid(row=4, column=0, padx=10, pady=3,)
		Label(self.ventanaEstados_cuentas, text='T. Débito',font=('Comic Sans MS', 12),bg='#C3C3C3').grid(row=5, column=0, padx=10, pady=3,)
		Label(self.ventanaEstados_cuentas, text='T. Crédito',font=('Comic Sans MS', 12),bg='#C3C3C3').grid(row=6, column=0, padx=10, pady=3,)
		Label(self.ventanaEstados_cuentas, text='Mercado Pago',font=('Comic Sans MS', 12),bg='#C3C3C3').grid(row=7, column=0, padx=10, pady=3,)

		Label(self.ventanaEstados_cuentas, text='Ingresos',font=('Comic Sans MS', 16),bg='#C3C3C3').grid(row=2, column=1, padx=10, pady=3,)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=3, column=1,sticky='w')
		self.efectivo_ingreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12, fg='green', textvariable=self.ing_efec,justify="center" )
		self.efectivo_ingreso.grid(row=3, column=1, padx=10, pady=3)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=4, column=1,sticky='w')
		self.transf_ingreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12, fg='green',textvariable=self.ing_trans,justify="center" )
		self.transf_ingreso.grid(row=4, column=1, padx=10, pady=3)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=5, column=1,sticky='w')
		self.debito_ingreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12, fg='green',textvariable=self.ing_debit,justify="center" )
		self.debito_ingreso.grid(row=5, column=1, padx=10, pady=3)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=6, column=1,sticky='w')
		self.credito_ingreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12, fg='green',textvariable=self.ing_cred,justify="center" )
		self.credito_ingreso.grid(row=6, column=1, padx=10, pady=3)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=7, column=1,sticky='w')
		self.credito_ingreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12, fg='green',textvariable=self.ing_mercado,justify="center" )
		self.credito_ingreso.grid(row=7, column=1, padx=10, pady=3)

		Label(self.ventanaEstados_cuentas, text='Egresos',font=('Comic Sans MS', 16),bg='#C3C3C3').grid(row=2, column=2, padx=10, pady=3,)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=3, column=2, sticky='w')
		self.efectivo_egreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12,fg='red', textvariable=self.egre_efec,justify="center")
		self.efectivo_egreso.grid(row=3, column=2, padx=10, pady=3)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=4, column=2,sticky='w')
		self.transf_egreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12,fg='red',textvariable=self.egre_tran,justify="center" )
		self.transf_egreso.grid(row=4, column=2, padx=10, pady=3)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=5, column=2, sticky='w')
		self.debito_egreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12,fg='red',textvariable=self.egre_debit,justify="center")
		self.debito_egreso.grid(row=5, column=2, padx=10, pady=3)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=6, column=2,sticky='w')
		self.credito_egreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12, fg='red',textvariable=self.egre_cred,justify="center")
		self.credito_egreso.grid(row=6, column=2, padx=10, pady=3)
		Label(self.ventanaEstados_cuentas, text='$',font=('Comic Sans MS', 10),bg='#C3C3C3').grid(row=7, column=2,sticky='w')
		self.credito_egreso=Entry(self.ventanaEstados_cuentas, font=('Comic Sans MS', 10), state='readonly',width=12, fg='red',textvariable=self.egre_mercado,justify="center")
		self.credito_egreso.grid(row=7, column=2, padx=10, pady=3)
		
		self.ventanaEstados_cuentas.mainloop()

#----------------Ventana Recargo Tarjetas------------------
	def Recargos(self):
		self.ventanaRecargos=Toplevel()
		self.ventanaRecargos.title('Recargos Tarjetas')
		self.ventanaRecargos.geometry('+500+50')
		self.ventanaRecargos.config(bg='#C3C3C3')
		self.ventanaRecargos.resizable(width=0, height=0)
		self.ventanaRecargos.transient(self.inicio)
		self.ventanaRecargos.grab_set()

		#Valores de calculos
		self.debito=DoubleVar(value=self.mostrar_recargo(tipo_tarjeta=1))
		self.credito=DoubleVar(value=self.mostrar_recargo(tipo_tarjeta=2))

		Label(self.ventanaRecargos,text='Configuración de\nrecargos en tarjetas',font=('Comic Sans MS', 16),bg='#C3C3C3', justify='center').grid(row=0, column=0,padx=10,pady=5)
		Label(self.ventanaRecargos,text='Recargo T. Débito',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=1, column=0,columnspan=3)
		Entry(self.ventanaRecargos,textvariable=self.debito,font=('Comic Sans MS', 10), justify='center').grid(row=2, column=0,)
		Label(self.ventanaRecargos,text='%',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='left').grid(row=2, column=0,sticky='w')
		Label(self.ventanaRecargos,text='Recargo T. Crédito',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='center').grid(row=3, column=0,columnspan=3)
		Entry(self.ventanaRecargos,textvariable=self.credito,font=('Comic Sans MS', 10), justify='center').grid(row=4, column=0,)
		Label(self.ventanaRecargos,text='%',font=('Comic Sans MS', 10),bg='#C3C3C3', justify='left').grid(row=4, column=0,sticky='w')
		
		self.safe=Button(self.ventanaRecargos, text='Guardar',font=('Comic Sans MS', 10),fg='#3BA684', command=self.guardar_recargo)
		self.safe.grid(row=5, column=0,columnspan=3,pady=5)
		
		self.ventanaRecargos.mainloop()

#----------------Ventana Modificación cuerpo de mail predeterminado
	def Modificar_cuerpo_mail(self):
		self.ventanaCuerpo_mail=Toplevel()
		self.ventanaCuerpo_mail.title('Configurar cuerpo de mail')
		self.ventanaCuerpo_mail.geometry('+500+50')
		self.ventanaCuerpo_mail.config(bg='#C3C3C3')
		self.ventanaCuerpo_mail.resizable(0,0)
		self.ventanaCuerpo_mail.transient(self.inicio)
		self.ventanaCuerpo_mail.grab_set()

		Label(self.ventanaCuerpo_mail,bg='#C3C3C3',justify='center',font=('Comic Sans MS', 16), text='Opciones de configuracion de mail').grid(row=0, column=0,columnspan=3)
		self.boton_presupuesto=Radiobutton(self.ventanaCuerpo_mail, text="Presupuestos", variable=self.opcion, value=1,bg='#C3C3C3',justify='right',font=('Comic Sans MS', 10),command=self.seleccion).grid(row=1, column=0,sticky='w')
		self.boton_pedido=Radiobutton(self.ventanaCuerpo_mail, text="Pedidos", variable=self.opcion, value=2,bg='#C3C3C3',justify='right',font=('Comic Sans MS', 10),command=self.seleccion).grid(row=2, column=0,sticky='w')
		self.boton_listas=Radiobutton(self.ventanaCuerpo_mail, text="Listas de precios", variable=self.opcion,value=3, bg='#C3C3C3',justify='right',font=('Comic Sans MS', 10),command=self.seleccion).grid(row=3, column=0,sticky='w')
		self.boton_otros=Radiobutton(self.ventanaCuerpo_mail, text="Otros", variable=self.opcion, value=4,bg='#C3C3C3',justify='right',font=('Comic Sans MS', 10),command=self.seleccion ).grid(row=4, column=0,sticky='w')
		self.opciones_otros=Combobox(self.ventanaCuerpo_mail,textvariable=self.otros, font=('Comic Sans MS', 10),width=15,state='disabled')
		self.opciones_otros['values']=self.otras_opciones()
		self.opciones_otros.bind('<<ComboboxSelected>>',self.seleccion_otros)
		self.opciones_otros.grid(row=4, column=0,sticky='e')
		Label(self.ventanaCuerpo_mail,bg='#C3C3C3',justify='center',font=('Comic Sans MS', 10), text='Ingrese el texto que desea en el cuerpo del mail:').grid(row=5, column=0,columnspan=3)
		self.cuerpo_mail=Text(self.ventanaCuerpo_mail,font=('Comic Sans MS', 16),width=37, height=8)
		self.barra_texto=Scrollbar(self.ventanaCuerpo_mail, orient="vertical", command=self.cuerpo_mail.yview)
		self.cuerpo_mail.configure(yscrollcommand=self.barra_texto.set)
		self.barra_texto.grid(row=6, column=3, sticky = 'NS')
		self.cuerpo_mail.grid(row=6, column=0,columnspan=3, padx=10,pady=3)
		self.insertar_cliente=Button(self.ventanaCuerpo_mail,text='Insertar cliente',font=('Comic Sans MS', 10),fg='#3BA684',command=self.insertar_cliente).grid(row=7, column=0)
		self.insertar_cliente=Button(self.ventanaCuerpo_mail,text='Eliminar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.eliminar_otros).grid(row=7, column=1)
		self.guardar_cuerpo=Button(self.ventanaCuerpo_mail,text='Guardar',font=('Comic Sans MS', 10),fg='#3BA684',command=self.guardar_mail).grid(row=7, column=2)

		self.ventanaCuerpo_mail.mainloop()

#----------------Ventana envios de mail con adjuntos---------
	def Enviar_adjuntos(self):
		self.ventanaEnviar_adjuntos=Toplevel()
		self.ventanaEnviar_adjuntos.title('Configurar cuerpo de mail')
		self.ventanaEnviar_adjuntos.geometry('+500+50')
		self.ventanaEnviar_adjuntos.config(bg='#C3C3C3')
		self.ventanaEnviar_adjuntos.resizable(0,0)
		self.ventanaEnviar_adjuntos.transient(self.inicio)
		self.ventanaEnviar_adjuntos.grab_set()

		self.archivo.set('Archivo')

		#Seleccion de asunto
		Label(self.ventanaEnviar_adjuntos,bg='#C3C3C3',justify='center',font=('Comic Sans MS', 16), text='Opciones de configuracion de mail').grid(row=0, column=0,columnspan=3)
		Label(self.ventanaEnviar_adjuntos,bg='#C3C3C3',justify='center',font=('Comic Sans MS', 10), text='Asunto').grid(row=1, column=0,)
		self.boton_presupuesto=Radiobutton(self.ventanaEnviar_adjuntos, text="Presupuestos", variable=self.opcion, value=1,bg='#C3C3C3',justify='right',font=('Comic Sans MS', 10),command=self.seleccion_para_enviar).grid(row=2, column=0,sticky='w')
		self.boton_pedido=Radiobutton(self.ventanaEnviar_adjuntos, text="Pedidos", variable=self.opcion, value=2,bg='#C3C3C3',justify='right',font=('Comic Sans MS', 10),command=self.seleccion_para_enviar).grid(row=3, column=0,sticky='w')
		self.boton_listas=Radiobutton(self.ventanaEnviar_adjuntos, text="Listas de precios", variable=self.opcion,value=3, bg='#C3C3C3',justify='right',font=('Comic Sans MS', 10),command=self.seleccion_para_enviar).grid(row=4, column=0,sticky='w')
		self.boton_otros=Radiobutton(self.ventanaEnviar_adjuntos, text="Otros", variable=self.opcion, value=4,bg='#C3C3C3',justify='right',font=('Comic Sans MS', 10),command=self.seleccion_para_enviar ).grid(row=5, column=0,sticky='w')
		self.opciones_otros=Combobox(self.ventanaEnviar_adjuntos,textvariable=self.otros, font=('Comic Sans MS', 10),width=15,state='disabled')
		self.opciones_otros['values']=self.otras_opciones()
		self.opciones_otros.bind('<<ComboboxSelected>>',self.seleccion_otros_para_enviar)
		self.opciones_otros.grid(row=6, column=0,)

		Separator(self.ventanaEnviar_adjuntos, orient='vertical').grid(row=1, column=1, padx=10, rowspan=6,sticky="SN")

		#Busqueda de clientes
		self.labelCliente=Label(self.ventanaEnviar_adjuntos, text='Cliente',bg='#C3C3C3',font=('Comic Sans MS', 10))
		self.labelCliente.grid(row=1, column=2,pady=3, padx=3)
		self.entryCliente=Entry(self.ventanaEnviar_adjuntos,textvariable=self.cliente,width=31,font=('Comic Sans MS', 10))
		self.entryCliente.bind('<KeyRelease>',self.busq_cliente) 
		self.entryCliente.focus()
		self.entryCliente.grid(row=2, column=2,pady=3, padx=3)
		self.listaClientes=Listbox(self.ventanaEnviar_adjuntos,font=('Comic Sans MS', 10) )
		self.listaClientes.config(width="31", height="5")
		self.lista_busq_cliente(self.lista_cliente())
		self.listaClientes.bind('<Return>',self.mostrar_mail_cliente )
		self.listaClientes.grid(row=3, column=2,columnspan=3, rowspan=3,pady=3, padx=3, sticky='w')

		Separator(self.ventanaEnviar_adjuntos, orient='horizontal').grid(row=7, column=0, pady=10, columnspan=7,sticky="we")

		#Mail de cliente seleccionado
		Label(self.ventanaEnviar_adjuntos,bg='#C3C3C3',justify='center',font=('Comic Sans MS', 10), text='Mail seleccionados').grid(row=8, column=0,columnspan=4,)
		self.direcion_mail=Text(self.ventanaEnviar_adjuntos,width=62,height=1,font=('Comic Sans MS', 10))
		self.direcion_mail.grid(row=9, column=0,pady=3, padx=3, columnspan=4)

		#Archivo adjunto
		self.nombre_archivo=Entry(self.ventanaEnviar_adjuntos,font=('Comic Sans MS', 10),width=62, textvariable=self.archivo, state='disabled')
		self.nombre_archivo.grid(row=10, column=0,pady=3, padx=3, columnspan=5, sticky='w')
		self.insertar_archivo=Button(self.ventanaEnviar_adjuntos,text='Insertar archivo',font=('Comic Sans MS', 10),fg='#3BA684',command=self.adjuntar_pdf).grid(row=11, column=0,pady=3, padx=3)
			
		self.enviar_mail=Button(self.ventanaEnviar_adjuntos,text='Enviar',font=('Comic Sans MS', 16),fg='#3BA684',command=self.mail_personalizado, width=12 ).grid(row=11, column=2, rowspan=3)

		self.ventanaEnviar_adjuntos.mainloop()

#----------------Base de datos---------------------
	#Conexión
	def conectar(self):
		try:
			conexion=sqlite3.connect('bdFarfalla.db')
			return conexion
		except sqlite3.Error as Error:
			messagebox.showerror('Error','Problemas para recuperar los datos')

#----------------Tablas y mas que usan BBDD -------------------
# Menú configuracion
	def backup_BD(self):
		try:
			#Si existe la base de datos
			conexion = self.conectar()
			# Crear BD de respaldo
			actual=date.today()
			fecha=f'{actual.day}-{actual.month}-{actual.year}'
			conexion_backup = sqlite3.connect(f'backup_{fecha}.db')
			with conexion_backup:
				conexion.backup(conexion_backup)
		except sqlite3.Error as error:
			print("Error: ", error)
		finally:
			if conexion_backup:
				conexion_backup.close()
				conexion.close()
				messagebox.showinfo('Guardado', 'La base de datos generó el respaldo correctamente')

#ventana Stock productos
	#Buscar productos tabla inventario
	def buscadorProductos(self,event=None):
		self.tabla.delete(*self.tabla.get_children())
		conexion=self.conectar()
		cursor=conexion.cursor()
		producto=self.buscarProducto.get()
		cursor.execute("""SELECT PR.id,PR.codigo_proveedor,PV.proveedor,PR.producto,PR.stock,PR.costo,PR.precio_venta
						 FROM productos as PR
						 INNER JOIN
							proveedores as PV
							on PR.id_proveedor = PV.id
				WHERE PR.producto LIKE ? or PR.codigo_proveedor LIKE ? or PR.id LIKE ?
				ORDER BY producto ASC""",(f'%{producto}%',f'%{producto}%',f'%{producto}%',))
		datos=cursor.fetchall()
		for (id,codigo,proveedor,producto,stock,costo,precio_venta) in datos:
				self.tabla.insert('','end',values=(id,codigo,proveedor,producto,stock,costo,precio_venta))
		self.buscarProducto.set('')
		conexion.commit()
		conexion.close()
		self.entryBuscar.focus()

	#Armado de lista de precios publico
	def lista_venta(self):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("""SELECT producto, stock, precio_venta 
					FROM productos 
					WHERE stock>0 AND precio_venta>0
					ORDER BY producto ASC""")
		datos=cursor.fetchall()
		lista=[]
		for e in datos:
			lista.append(e)
		lista=list(map(list, lista))
		return lista
		
	#Eliminar de lista de precios publico del día
	def eliminar_lista_publico(self):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("DELETE FROM lista_publico WHERE fecha=(?)", [self.fecha])
		conexion.commit()
		messagebox.showinfo('Borrado', 'La lista se eliminó exitosamente')

	#Backup stock
	def backup (self, event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		archivo = Workbook()
		hoja=archivo.active
		hoja.append(['id','codigo_proveedor','proveedor','producto', 'stock'])
		tabla=cursor.execute("""SELECT PR.id, PR.codigo_proveedor, PV.proveedor,PR.producto,PR.stock
				FROM productos as PR
					INNER JOIN
					proveedores as PV
					on PR.id_proveedor = PV.id""")
		for i in tabla:
			hoja.append(i)
		#Ajuste de ancho de columnas
		for i in hoja.columns:
			ancho = 0
			columna = i[0].column_letter
			for celda in i:
				try:
					if len(str(celda.value)) > ancho:
						ancho = len(celda.value)
				except:
					pass
			ajuste_celda = (ancho + 2) * 1.2
			hoja.column_dimensions[columna].width = ajuste_celda
		
		#Guardado del archivo
		archivo.save(f".\Backup_stock\stock_{self.fecha.replace('/','-')}.xlsx")
		os.system(f".\Backup_stock\stock_{self.fecha.replace('/','-')}.xlsx")
	
#ventana Productos	
	#Trasladar datos productos de tabla a ventana Productos
	def admin_producto(self,event=None):
		try:
			seleccion=self.tabla.item(self.tabla.selection())['values']
			id_busq=seleccion[0]
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("""SELECT PR.id,PR.codigo_proveedor,PV.proveedor,PR.producto,PR.stock,PR.costo,PR.precio_venta
							 FROM productos as PR
							 INNER JOIN
								proveedores as PV
								on PR.id_proveedor = PV.id
								WHERE PR.id="""+ str(id_busq))
			admin=cursor.fetchall()
			for datos in admin:
				self.id_producto.set(datos[0])
				self.codigo.set(datos[1])
				self.proveedor.set(datos[2])
				self.producto.set(datos[3])
				self.stock.set(datos[4])
				self.costo.set(datos[5])
				self.precio_venta.set(datos[6])
			conexion.commit()
			conexion.close()
			self.tabla.delete(*self.tabla.get_children())
			self.Producto()
		except IndexError:
			messagebox.showerror('ERROR', 'Debe seleccionar un producto existente para modificar')
		
	#Agregar artículos ventana Productos
	def agregar_articulo(self,event=None):
		if self.proveedor.get()=='' or self.producto.get()=='':
			messagebox.showerror('ERROR', 'Debe ingresar "Proveedor/Producto"')
		else:
			try:
				conexion=self.conectar()
				cursor=conexion.cursor()
				proveedor=self.proveedor.get()
				cursor.execute('SELECT id FROM proveedores WHERE proveedor like ?', [proveedor])
				id_proveedor=cursor.fetchone()
				datos=[
					self.codigo.get(),
					id_proveedor[0],
					self.producto.get(),
					self.stock.get(),
					self.costo.get(),
					self.precio_venta.get()
					]
				cursor.execute("INSERT INTO productos VALUES(NULL,?,?,?,?,?,?)", (datos))
				conexion.commit()
				messagebox.showinfo('Añadido', 'El artículo se agregó exitosamente')
				self.id_producto.set('')
				self.codigo.set('')
				self.proveedor.set('')
				self.producto.set('')
				self.stock.set('')
				self.costo.set('')
				self.precio_venta.set('')
				self.e2.focus()
				conexion.close()
			except TypeError:
				messagebox.showerror('ERROR', 'Debe ingresar un proveedor de la lista')
			except IntegrityError:
				messagebox.showerror('ERROR', 'El producto ya está ingresado')
		
	#Eliminar artículos ventana Productos
	def eliminar_articulo(self,event=None):
		eliminar=messagebox.askyesno('Eliminar','Si elimina este producto,\ntodos los datos relacionado\ncon el mismo sufriran daños irreparables,\n¿Desea continuar con la eliminación?')
		if eliminar==True:
			eliminar2=messagebox.askyesno('ÚLTIMA ADVERTENCIA','SI ELIMINA ESTE PRODUCTO,\nTODOS LOS DATOS RELACIONADO\nCON EL MISMO SUFRIRAN DAÑOS IRREPARABLES,\n¿DESEA CONTINUAR CON LA ELIMINACIÓN?')
			if eliminar2==True:
				conexion=self.conectar()
				cursor=conexion.cursor()
				id_busq=self.id_producto.get()
				cursor.execute("DELETE FROM productos WHERE id="+str(id_busq))
				conexion.commit()
				messagebox.showinfo('Borrado', 'El artículo se eliminó exitosamente')
				self.id_producto.set('')
				self.codigo.set('')
				self.proveedor.set('')
				self.producto.set('')
				self.stock.set('')
				self.costo.set('')
				self.precio_venta.set('')
				conexion.close()

	#Modificar artículos ventana Productos
	def modificar_articulo(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			id_busq=self.id_producto.get()
			proveedor=self.proveedor.get()
			cursor.execute('SELECT id FROM proveedores WHERE proveedor like ?', [proveedor])
			id_proveedor=cursor.fetchone()
			datos=[
				self.id_producto.get(),
				self.codigo.get(),
				id_proveedor[0],
				self.producto.get(),
				self.stock.get(),
				self.costo.get(),
				self.precio_venta.get()        
			]
			cursor.execute('''
			UPDATE productos
			SET id=?, codigo_proveedor=?, id_proveedor=?, producto=?, stock=?, costo=?, precio_venta=?
			WHERE id='''+str(id_busq),
			datos)
			conexion.commit()
			conexion.close()
			if datos!=None:
				messagebox.showinfo('Modificado', 'Los datos han sido modificados exitosamente')
		except AttributeError or IndexError:
			messagebox.showerror('ERROR', 'Debe seleccionar un producto existente para modificar')
		except TypeError:
			messagebox.showerror('ERROR', 'Debe ingresar un proveedor de la lista')

#Ventana uso interno
	#Stock disponible
	def stock_disponible_uso_interno(self, id_producto=None, cantidad=None, producto=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('SELECT stock FROM productos WHERE id LIKE ?', [id_producto])
		stock=cursor.fetchone()[0]
		#Corroboramos que haya stock suficiente para descontar
		if stock-cantidad<0:
			#Si no hay, avisamos que con el ID seleccionadado no hay suficientes.
			messagebox.showerror('ERROR', f'No dispone de:\n\n{cantidad} unidades de\n{producto},\npara realizar la extracción.\n\nSTOCK ACTUAL: {stock} unidades.')
		else:
			cursor.execute("""UPDATE productos
								SET stock = (SELECT stock - ? FROM productos WHERE id LIKE ?)
								WHERE id LIKE ?""",((cantidad, id_producto, id_producto)))
			conexion.commit()
			fecha=self.fecha
			for i in datos:
				cursor.execute('INSERT INTO uso_interno VALUES (NULL,?,?,?)',[id_producto,cantidad,fecha])
			conexion.commit()
			conexion.close()
			messagebox.showinfo('Registro exitoso', 'El uso interno se registró exitosamente')

	#Tabla uso interno
	def agregar_uso_interno(self, event=None):
		id_prod=self.id_producto.get()		
		producto=self.producto.get()
		cantidad=self.cant_pedido.get()
		datos=[(
			id_prod,
			producto,
			cantidad
		)]
		for id_prod,producto,stock in datos:
			self.tabla_uso_interno.insert('', 'end', values=(id_prod,producto,stock))
		self.producto.set('')
		self.cant_pedido.set('')
		
	#Eliminar seleccion
	def eliminar_uso_interno (self, event=None):
		self.tabla_uso_interno.delete(self.tabla_uso_interno.selection())

	#Confirmar uso interno
	def confirmar_uso_interno (self,event=None):
		datos=[]
		fecha=self.fecha
		index=0
		for i in self.tabla_uso_interno.get_children():
			datos.append(self.tabla_uso_interno.item(i)['values'])
			datos[index].append(fecha)
			index+=1
		#Productos 
		id_prod=[]
		salida_stock=[]	
		for i in datos:
			id_prod.append(i[0])
			salida_stock.append(i[2])
		for i in datos:
			self.stock_disponible_uso_interno(id_producto=i[0], cantidad=i[2], producto=i[3])

		self.producto.set('')
		self.id_producto.set('')
		self.cant_pedido.set('')
		self.tabla_uso_interno.delete(*self.tabla_uso_interno.get_children())

#Ventana historial de usos internos
	#Buscar datos
	def buscar_usos (self,event=None):
		self.tablaBusq_usos.delete(*self.tablaBusq_usos.get_children())
		conexion=self.conectar()
		cursor=conexion.cursor()
		busqueda=self.buscador_usos.get()
		cursor.execute("""SELECT UI.id,UI.id_producto,PR.producto,UI.cantidad,UI.fecha
						 FROM uso_interno as UI
						 INNER JOIN
							productos as PR
							on UI.id_producto = PR.id
						WHERE UI.id LIKE ? or UI.id_producto LIKE ? or PR.producto LIKE ? or UI.fecha LIKE ? or UI.cantidad LIKE ?""",
		 (f'%{busqueda}%',f'%{busqueda}%',f'%{busqueda}%',f'%{busqueda}%',f'%{busqueda}%'))#LIKE para buscar coincidencias en una columna. %% comodin de busqueda
		datos=cursor.fetchall()
		for (id,id_prod,producto, cantidad, fecha) in datos:
				self.tablaBusq_usos.insert('','end',values=(id,id_prod, producto,cantidad, fecha))
		self.buscador_usos.set('')
		conexion.commit()
		conexion.close()
		self.tablaBusq_usos.selection()
 		
#ventana Compras	
	#Lista inicial de productos en ventana Compras y Presupuestos
	def lista_prod(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("""SELECT producto FROM productos
				GROUP BY producto
				ORDER BY producto
				""")
		lista=[]
		for i in cursor.fetchall():
			lista.append(i[0])
		return lista
		conexion.commit()
		conexion.close()
	
	#Datos del producto seleecionado
	def mostrar_datos_producto(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		proveedor = str(self.proveedor.get())
		producto = self.list1.selection_get()
		try:
			cursor.execute('SELECT id FROM proveedores WHERE proveedor LIKE ?', [proveedor])
			id_proveedor=cursor.fetchone()[0]
			cursor.execute("SELECT * FROM productos WHERE producto LIKE ? and id_proveedor LIKE ? ", [producto,id_proveedor])
			admin=cursor.fetchall()
			
			if admin!=[]:
				for datos in admin:
					self.id_producto.set(datos[0])
					self.codigo.set(datos[1])
					self.producto.set(datos[3])
					self.costo.set(datos[5])
					self.precio_venta.set(datos[6])
			else:
				agregar_proveedor_al_producto=messagebox.askyesno(f'Producto sin proveedor {proveedor}', f'¿Desea agregar {producto} al proveedor {proveedor}?')
				if agregar_proveedor_al_producto == True:
					cursor.execute("""INSERT INTO productos
									VALUES (NULL,'',?,?,0,0,0)
									""", [id_proveedor,producto])
					conexion.commit()
				
		except TypeError:
				messagebox.showerror('Sin datos', 'Debe seleccionar un proveedor de la lista')
		conexion.commit()
		conexion.close()

	#Mostrar compra en tabla
	def mostrar_compra(self,event=None):
		self.tablaCompras.delete(*self.tablaCompras.get_children())
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('''SELECT TEMP_C.id, TEMP_C.codigo_proveedor, PV.proveedor, PD.producto, TEMP_C.cantidad, TEMP_C.costo, TEMP_C.cantidad*TEMP_C.costo as "pretotal"
			FROM temporalcompra AS TEMP_C
			INNER JOIN proveedores AS PV
				ON TEMP_C.id_proveedor=PV.id
			INNER JOIN productos AS PD
				ON TEMP_C.id_producto=PD.id''')
		datos=cursor.fetchall()
		
		for (id,codigo_proveedor,proveedor,producto,stock,costo,pretotal) in datos:
			self.tablaCompras.insert('', 'end', values=(id,codigo_proveedor,proveedor,producto,stock,costo,pretotal))
		conexion.commit()
		conexion.close()
		
	#Mostrar datos
	def agregar_compra(self,event=None):
		proveedor=str(self.proveedor.get())
		try:
			seleccion=self.tablaCompras.get_children()[0]
			proveedor_tabla=self.tablaCompras.item(seleccion)['values']
		except IndexError:
			proveedor_tabla=['','',proveedor]
		if proveedor=='':
			messagebox.showerror('Sin datos', 'Debe seleccionar un proveedor de la lista')
		elif proveedor!=proveedor_tabla[2]:
			try:
				messagebox.showerror('ERROR', 'Debe coincidir el proveedor en todos los articulos')
			except UnboundLocalError:
				pass
		else:
			try:
				codigo_proveedor=str(self.codigo.get())
				id_producto=int(self.id_producto.get())
				cantidad=int(self.stock.get())
				costo=float(self.costo.get())
				conexion=self.conectar()
				cursor=conexion.cursor()
				cursor.execute('SELECT id FROM proveedores WHERE proveedor LIKE ?',[proveedor])
				id_proveedor=cursor.fetchone()
				datos=[
					codigo_proveedor,
					id_proveedor [0],
					id_producto,
					cantidad,
					costo	
				]
				cursor.execute('''CREATE TABLE IF NOT EXISTS temporalcompra 
						(id INTEGER,
						codigo_proveedor TEXT,
						id_proveedor INTEGER,
						id_producto INTEGER UNIQUE,
						cantidad INTEGER,
						costo REAL,
						PRIMARY KEY ("id" AUTOINCREMENT),
						FOREIGN KEY("id_proveedor") REFERENCES proveedores (id),
						FOREIGN KEY("id_producto") REFERENCES productos (id))''')
				try:
					cursor.execute('INSERT INTO temporalcompra VALUES (NULL,?,?,?,?,?)', datos )
					conexion.commit()
					conexion.close()

					self.mostrar_compra()
					self.suma_subtotales()
					self.descuento_compra()
					self.sumaTotales()

					self.codigo.set('')
					self.producto.set('')
					self.stock.set('')
					self.costo.set('')
					self.precio_venta.set('')
				except sqlite3.IntegrityError:
					messagebox.showerror('Duplicado', f'Ya existe este articulo {self.producto.get()} en la lista')
					
			except TypeError:
				messagebox.showerror('Sin datos', 'Debe seleccionar un proveedor de la lista')
			
	#Recuperar compra incompleta
	def recuperar_compra(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute('''SELECT TEMP_C.id, TEMP_C.codigo_proveedor, PV.proveedor, PD.producto,TEMP_C.cantidad, TEMP_C.costo, TEMP_C.cantidad*TEMP_C.costo as "pretotal"
					FROM temporalcompra AS TEMP_C
						INNER JOIN proveedores AS PV
							ON TEMP_C.id_proveedor=PV.id
						INNER JOIN productos AS PD
							ON TEMP_C.id_producto=PD.id''')
			datos=cursor.fetchall()
			for (id,codigo,proveedor,producto,stock,costo,pretotal) in datos:
				self.tablaCompras.insert('', 'end', values=(id,codigo,proveedor,producto,stock,costo,pretotal))
			self.proveedor.set(datos[0][2])
			conexion.commit()
			conexion.close()
			self.mostrar_compra()
			self.suma_subtotales()
			self.descuento_compra()
			self.sumaTotales()
		except sqlite3.OperationalError as error:
			messagebox.showinfo('Sin datos', 'No se registran datos a recuperar')
		
	#Sacar de lista compras
	def eliminar_de_lista(self,event=None):
		seleccion=self.tablaCompras.item(self.tablaCompras.selection())['values']
		id_busq=seleccion[0]
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('DELETE FROM temporalcompra WHERE id='+str(id_busq) )					
		conexion.commit()
		conexion.close()

		self.tablaCompras.delete(self.tablaCompras.selection())
		self.mostrar_compra()
		self.suma_subtotales()
		self.descuento_compra()
		self.sumaTotales()
		self.codigo.set('')
		self.producto.set('')
		self.stock.set('')
		self.costo.set('')
		self.precio_venta.set('')
		self.e1.focus()
		
	#Finalizar compra
	def finalizar_compra(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("""SELECT PR.id ,TC.codigo_proveedor,TC.id_proveedor,
						TC.cantidad + PR.stock as "stock actualizado", TC.costo 
						FROM temporalcompra as TC
						INNER JOIN productos as PR
							on PR.id=TC.id_producto""")
		datos=cursor.fetchall()

		#Datos actualizados del stock, costo y precio de venta de los productos ingresados en la compra
		datos_actualizados_productos=[]
		for i in datos:
			id_proveedor=i[2]
			costo=float(i[4])
			cursor.execute(""" SELECT porcentaje,redondeo FROM precio_venta WHERE id_proveedor LIKE ? """,[id_proveedor])
			datos_venta=cursor.fetchone()
			if datos_venta!=None:
				redondeo=float(datos_venta[1])
				porcentaje=float(datos_venta[0])
			else:
				redondeo=float(5)
				porcentaje=float(50)
				messagebox.showinfo('Precios de Venta',f'No está configura el proveedor para obtener el precio de venta\n\nSe utilizarán los valores standar de:\nPORCENTAJE: {porcentaje} %\nREDONDEA A $ {redondeo}')
			datos_actualizados_productos.append((i[0],i[1],i[2],i[3],i[4],self.calculo_venta(costo,redondeo,porcentaje)))
		
		for i in datos_actualizados_productos:
			cursor.execute("""UPDATE productos 
					SET codigo_proveedor=?,
						stock=?,
						costo=?,
						precio_venta=?
					WHERE id LIKE ?""",(i[1],i[3],i[4],i[5],i[0]))
		conexion.commit()

		#Datos del comprobante de compra
		proveedor=self.proveedor.get()
		tipo_comprobante=self.cte.get()
		nro_comprobante=self.nrocte.get()
		fecha_comprobante=self.fechacte.get()
		medio_pago=self.pagos.get()
		sub_total=self.subtotal.get()
		descuento=self.porcentaje_descuento.get()
		
		cursor.execute(" SELECT id FROM proveedores WHERE proveedor LIKE ? " ,[proveedor])
		id_proveedor=cursor.fetchone()[0]
		
		cursor.execute(" SELECT id FROM tipo_cte WHERE tipo LIKE ? ",[tipo_comprobante])
		id_tipo_comprobante=cursor.fetchone()[0]

		cursor.execute("SELECT id FROM medios_pagos WHERE tipo LIKE ? ",[medio_pago])
		id_medio_pago=cursor.fetchone()[0]

		datos=[
			id_proveedor,
			id_tipo_comprobante,
			nro_comprobante,
			fecha_comprobante,
			id_medio_pago,
			sub_total,
			descuento
		]
		try:
			cursor.execute(""" INSERT INTO compras
								(id, 
								id_proveedor, 
								id_tipo_comprobante, 
								numero_comprobante,
								fecha,
								id_medio_pago,
								sub_total,
								porcentaje_dto)
						VALUES (NULL,?,?,?,?,?,?,?) """ ,datos)
			conexion.commit() 
		

			#DETALLE DE LA COMPRA
			cursor.execute(" SELECT id FROM compras ORDER BY id DESC")
			id_compra=cursor.fetchone()[0]

			cursor.execute("SELECT * FROM temporalcompra")
			datos=cursor.fetchall()
			detalle_compra=[]
			for i in datos:
				detalle_compra.append((id_compra,i[3],i[4],i[5]))
			for i in detalle_compra:
				cursor.execute("""INSERT INTO detalle_compra 
							(id, id_compra, id_producto, cantidad, costo)
							VALUES (NULL,?,?,?,?)""", i)
			conexion.commit()
			
			#Actualizacion de las cuentas
			id_tipo=1
			datos=[
				id_tipo,
				id_medio_pago,
				self.periodo,
				self.total_compra.get()
			]
			cursor.execute('INSERT INTO estado_cuentas VALUES (NULL,?,?,?,?)',datos)
			conexion.commit() 

			#Limpiar pantalla finalizado el trabajo
			self.limpiar_compras()
		except sqlite3.IntegrityError:
			messagebox.showerror('ERROR', f'Existe un comprobante\n\n"{nro_comprobante}"\n\ningresado anteriormente')
	
	def limpiar_compras(self):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('DROP TABLE temporalcompra')
		conexion.commit()
		self.proveedor.set(''),
		self.cte.set(''),
		self.nrocte.set(''),
		self.pagos.set('')
		self.fechacte.set(''),
		self.subtotal.set(''),
		self.porcentaje_descuento.set(0.0),
		self.descuento.set(0.0),
		self.total_compra.set('')
		self.tablaCompras.delete(*self.tablaCompras.get_children())
		self.suma_subtotales()
		self.descuento_compra()
		self.sumaTotales()
		conexion.close()

#Ventana Modificador de nombre de producto
	#Modificar nombre artículo
	def guardar_cambio(self,event=None):
		articulo=self.list1.selection_get()
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('UPDATE productos SET producto=? WHERE producto=(?)', [self.actualizado.get(),articulo])
		conexion.commit()
		conexion.close()
		if articulo!=None:
			messagebox.showinfo('Modificado', 'Los datos han sido modificados exitosamente')

#Ventana Precio de venta
	#Seleccion de lista de proveedor a guardar/aplicar datos para precio de venta
	def seleccion_precio_publico(self, event=None):
		if self.lista_publico.get()==1:
			self.porcentaje_entry.config(state='normal')
			self.redondeo_entry.config(state='normal')
			self.lista_proveedor.config(state='disabled')
			self.proveedor.set('')
			self.porcentaje.set('')
			self.redondeo.set('')
			self.safe.config(state='disabled')
		else:
			self.lista_proveedor.config(state='normal')
			self.porcentaje_entry.config(state='normal')
			self.redondeo_entry.config(state='normal')
			self.safe.config(state='normal')

	def datos_para_precio_publico(self, event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		proveedor=self.lista_proveedor.get()
		cursor.execute("""SELECT PV.porcentaje, PV.redondeo 
						FROM precio_venta as PV
						INNER JOIN proveedores as PRV
							on PRV.id=PV.id_proveedor
						WHERE PRV.proveedor=(?)""", [proveedor,])
		admin=cursor.fetchall()
		for datos in admin:
			self.porcentaje.set(datos[0])
			self.redondeo.set(datos[1])
		conexion.commit()
		conexion.close()

	#Guardar datos ventana precio de venta
	def guardar(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		proveedor=self.lista_proveedor.get()
		try:
			cursor.execute("""UPDATE precio_venta 
						SET porcentaje=?, redondeo=?
						WHERE id_proveedor IN 
						(SELECT id FROM proveedores WHERE proveedor LIKE ?) """,
						(self.porcentaje.get(),self.redondeo.get(),(proveedor)))
			messagebox.showinfo('Correcto', 'Se guardo ajuste correctamente')
		except sqlite3.OperationalError as error:
			messagebox.showerror('Error', 'No se pudo guardar, intentelo nuevamente')
		conexion.commit()
		conexion.close()

	def cambio_masivo (self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		redondeo=float(self.redondeo.get())
		porcentaje=float(self.porcentaje.get())
		nuevos=[]
		if self.lista_publico.get()==1:
			cursor.execute('SELECT id, costo FROM productos')
		elif self.lista_publico.get()==0:
			messagebox.showerror('Error', 'Debe seleccionar un proveedor')
		else:
			self.guardar()
			proveedor=self.lista_proveedor.get()
			cursor.execute("""SELECT PR.id, PR.costo 
							FROM productos as PR
							INNER JOIN proveedores as PV
								on PV.id=PR.id_proveedor
							WHERE PV.proveedor LIKE ? """, [proveedor])
		actual=cursor.fetchall()
		for i in actual:
			if i[1]=='  -   ' or i[1]== '' or i[1]== None:
				nuevos.append((i[0],0))
			else:
				if redondeo==0:
					redondeo=0.01
				final=self.calculo_venta(costo=i[1],redondeo=redondeo,porcentaje=porcentaje)
				nuevos.append((i[0],final))
		for i in nuevos:
			cursor.execute('UPDATE productos SET precio_venta=? WHERE id=(?)',(i[1],i[0]))
		conexion.commit()
		conexion.close()
		messagebox.showinfo('Correcto', 'Se ajustó correctamente')
		
#Ventana Comprobantes
	#Buscar comprobantes
	def buscadorComprobantes(self,event=None):
		self.tablaCte.delete(*self.tablaCte.get_children())
		conexion=self.conectar()
		cursor=conexion.cursor()
		proveedor=self.buscarComprobante.get()
		cursor.execute("""SELECT CO.id,PV.proveedor, CTE.tipo, CO.numero_comprobante, CO.fecha, CO.sub_total-round(CO.sub_total*CO.porcentaje_dto*0.01,2) as total
				FROM compras as CO
				INNER JOIN proveedores AS PV
					ON PV.id=CO.id_proveedor
				INNER JOIN tipo_cte AS CTE
					on CTE.id=CO.id_tipo_comprobante
				WHERE PV.proveedor LIKE ? or CO.numero_comprobante LIKE ? or CO.fecha LIKE ? or total LIKE ? """,(f'%{proveedor}%',f'%{proveedor}%',f'%{proveedor}%',f'%{proveedor}%',))#LIKE para buscar coincidencias en una columna. %% comodin de busqueda
		datos=cursor.fetchall()
		for (id, proveedor, tipo, numero, fecha, total) in datos:
				self.tablaCte.insert('','end',values=(id, proveedor, tipo, numero, fecha, total))
		self.buscarComprobante.set('')
		conexion.commit()
		conexion.close()
		self.tablaCte.selection()

	#Selecion en tabla Busqueda
	def items_comprobante(self, event=None):
		self.tablaLista.delete(*self.tablaLista.get_children())
		self.seleccion=self.tablaCte.item(self.tablaCte.selection())['values']
		id_compra=self.seleccion[0]
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("""SELECT PR.producto, DC.cantidad 
							FROM detalle_compra as DC
							INNER JOIN productos as PR
								ON PR.id=DC.id_producto
							WHERE DC.id_compra LIKE  ?""", [id_compra])
		resumen=cursor.fetchall()
		for (i,e) in resumen:
			self.tablaLista.insert('', 'end', values=(i,e))

#Ventana Tipo Comprobante
	#Lista de comprobantes
	def lista_cte(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT tipo FROM tipo_cte")
		lista=[]
		for row in cursor.fetchall():
			lista.append(row[0])
			lista.sort()
		return lista
		conexion.commit()
		conexion.close()

	#Agregar tipo de comprobante
	def agregar_tipocte(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			tipo=self.cte.get()
			cursor.execute("INSERT INTO tipo_cte VALUES(NULL,?)",[tipo])
			conexion.commit()
			messagebox.showinfo('Añadido', 'El tipo de comprobante se agregó exitosamente')
			self.cte.set('')
			conexion.close()
			self.lista_cte()
		except sqlite3.IntegrityError:
			messagebox.showerror('ERROR', f'Existe un comprobante\n\n"{tipo}"\n\ningresado anteriormente')
		
	#Eliminar tipo de comprobante
	def eliminar_tipocte(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		tipo=self.cte.get()
		cursor.execute("DELETE FROM tipo_cte WHERE tipo=(?)",[tipo,])
		conexion.commit()
		messagebox.showinfo('Borrado', 'El tipo de comprobante se eliminó exitosamente')
		self.cte.set('')
		conexion.close()
		self.lista_cte()

#Ventana Medios de pago
	#Lista de medios
	def lista_medios(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT tipo FROM medios_pagos")
		lista=[]
		for row in cursor.fetchall():
			lista.append(row[0])
			lista.sort()
		return lista
		conexion.commit()
		conexion.close()

	#Agregar medio
	def agregar_medio(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			tipo=self.pagos.get()
			cursor.execute("INSERT INTO medios_pagos VALUES(NULL,?)",[tipo])
			conexion.commit()
			messagebox.showinfo('Añadido', 'El tipo de comprobante se agregó exitosamente')
			self.pagos.set('')
			conexion.close()
			self.lista_medios()
		except sqlite3.IntegrityError:
			messagebox.showerror('ERROR', f'Existe un medio de pago\n\n"{tipo}"\n\ningresado anteriormente')
		
	#Eliminar medio
	def eliminar_medio(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		tipo=self.pagos.get()
		cursor.execute("DELETE FROM medios_pagos WHERE tipo=(?)",[tipo,])
		conexion.commit()
		messagebox.showinfo('Borrado', 'El tipo de comprobante se eliminó exitosamente')
		self.pagos.set('')
		conexion.close()
		self.lista_medios()

#Ventana Proveedores
	#Lista de proveedores
	def lista_prov(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT proveedor FROM proveedores")
		lista=[]
		for row in cursor.fetchall():
			lista.append(row[0])
			lista.sort()
		return lista
		conexion.commit()
		conexion.close()

	#Mostrar datos proveedor
	def mostrar_datos_proveedor(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		proveedor=self.cb1.get()
		cursor.execute("SELECT * FROM proveedores WHERE proveedor=(?)", [proveedor,])
		admin=cursor.fetchall()
		for datos in admin:
			self.direccion.set(datos[2])
			self.telefono.set(datos[3])
			self.correo.set(datos[4])
		conexion.commit()
		conexion.close()

	#Agregar proveedor
	def agregar_proveedor(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			datos=[
				self.proveedor.get(),
				self.direccion.get(),
				self.telefono.get(),
				self.correo.get()
				]
			cursor.execute("INSERT INTO proveedores VALUES(NULL,?,?,?,?)", (datos))
			conexion.commit()
			messagebox.showinfo('Añadido', 'El artículo se agregó exitosamente')
			self.proveedor.set('')
			self.direccion.set('')
			self.telefono.set('')
			self.correo.set('')
			self.cb1.focus()
			self.cb1['values']=[]
			conexion.close()
			self.cb1['values']=self.lista_prov()
			
		except sqlite3.IntegrityError:
			messagebox.showerror('ERROR', f'Existe proveedor\n\n"{self.proveedor.get()}"\n\ningresado anteriormente')
		
	#Eliminar proveedor
	def eliminar_proveedor(self,event=None):
		eliminar=messagebox.askyesno('Eliminar','Si elimina este proveedor,\ntodos los datos relacionado\ncon el mismo sufriran daños irreparables,\n¿Desea continuar con la eliminación?')
		if eliminar==True:
			eliminar2=messagebox.askyesno('ÚLTIMA ADVERTENCIA','SI ELIMINA ESTE PROVEEDOR,\nTODOS LOS DATOS RELACIONADO\nCON EL MISMO SUFRIRAN DAÑOS IRREPARABLES,\n¿DESEA CONTINUAR CON LA ELIMINACIÓN?')
			if eliminar2==True:
				conexion=self.conectar()
				cursor=conexion.cursor()
				proveedor=self.proveedor.get()
				cursor.execute("DELETE FROM proveedores WHERE proveedor=(?)",[proveedor,])
				conexion.commit()
				messagebox.showinfo('Borrado', 'El artículo se eliminó exitosamente')
				self.proveedor.set('')
				self.direccion.set('')
				self.telefono.set('')
				self.correo.set('')
				self.cb1['values']=[]
				self.cb1.focus()
				conexion.close()
		self.cb1['values']=self.lista_prov()

	#Modificar proveedor
	def modificar_proveedor(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		proveedor=self.proveedor.get()
		cursor.execute('''UPDATE proveedores
		SET proveedor=?, direccion=?, telefono=?, correo=?
		WHERE proveedor=(?)''',
		[self.proveedor.get(),self.direccion.get(),self.telefono.get(),self.correo.get(),proveedor])
		conexion.commit()
		self.proveedor.set('')
		self.direccion.set('')
		self.telefono.set('')
		self.correo.set('')
		self.cb1['values']=[]
		self.cb1.focus()
		conexion.close()
		messagebox.showinfo('Modificado', 'Los datos han sido modificados exitosamente')
		self.cb1['values']=self.lista_prov()
		
#Ventana Clientes
	#Lista de clientes
	def lista_cliente(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT cliente FROM clientes ORDER BY cliente")
		lista=[]
		for row in cursor.fetchall():
			lista.append(row[0])
		return lista
		conexion.commit()
		conexion.close()

	#Mostrar datos clientes
	def mostrar_datos_cliente(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cliente=[self.listaClientes.selection_get()]
		cursor.execute("SELECT * FROM clientes WHERE cliente=(?)", cliente)
		admin=cursor.fetchall()
		for datos in admin:
			self.cliente.set(datos[1])
			self.nombre.set(datos[2])
			self.apellido.set(datos[3])
			self.direccion.set(datos[4])
			self.telefono.set(datos[5])
			self.correo.set(datos[6])
		conexion.commit()
		conexion.close()

	#Agregar cliente
	def agregar_cliente(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cliente=(f'{self.nombre.get()} {self.apellido.get()}')
		datos=[
			cliente,
			self.nombre.get(),
			self.apellido.get(),
			self.direccion.get(),
			self.telefono.get(),
			self.correo.get()
			]
		cursor.execute("INSERT INTO clientes VALUES(NULL,?,?,?,?,?,?)", (datos))
		conexion.commit()
		messagebox.showinfo('Añadido', 'El cliente se agregó exitosamente')
		self.cliente.set('')
		self.nombre.set('')
		self.apellido.set('')
		self.direccion.set('')
		self.telefono.set('')
		self.correo.set('')
		self.entryCliente.focus()
		self.listaClientes.delete(0,'end')
		conexion.close()
		self.lista_cliente()
		
	#Eliminar cliente
	def eliminar_cliente(self,event=None):
		eliminar=messagebox.askyesno('Eliminar','Si elimina este cliente,\ntodos los datos relacionado\ncon el mismo sufriran daños irreparables,\n¿Desea continuar con la eliminación?')
		if eliminar==True:
			eliminar2=messagebox.askyesno('ÚLTIMA ADVERTENCIA','SI ELIMINA ESTE CLIENTE,\nTODOS LOS DATOS RELACIONADO\nCON EL MISMO SUFRIRAN DAÑOS IRREPARABLES,\n¿DESEA CONTINUAR CON LA ELIMINACIÓN?')
			if eliminar2==True:
				conexion=self.conectar()
				cursor=conexion.cursor()
				cliente=[self.cliente.get()]
				cursor.execute("DELETE FROM clientes WHERE cliente LIKE ?", cliente)
				conexion.commit()
				messagebox.showinfo('Borrado', 'El cliente se eliminó exitosamente')
				self.cliente.set('')
				self.nombre.set('')
				self.apellido.set('')
				self.direccion.set('')
				self.telefono.set('')
				self.correo.set('')
				self.entryCliente.focus()
				self.listaClientes.delete(0,'end')
				conexion.close()
		self.lista_cliente()

	#Modificar proveedor
	def modificar_cliente(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cliente=self.cliente.get()
		nvocliente=(f'{self.nombre.get()} {self.apellido.get()}')
		cursor.execute('''UPDATE clientes
		SET cliente=?, nombre=?, apellido=?, direccion=?, telefono=?, correo=?
		WHERE cliente=(?)''',
		[nvocliente,self.nombre.get(),self.apellido.get(),self.direccion.get(),self.telefono.get(),self.correo.get(),cliente])
		conexion.commit()
		messagebox.showinfo('Modificado', 'Los datos han sido modificados exitosamente')
		self.cliente.set('')
		self.nombre.set('')
		self.apellido.set('')
		self.direccion.set('')
		self.telefono.set('')
		self.correo.set('')
		self.entryCliente.focus()
		self.listaClientes.delete(0,'end')
		conexion.close()
		self.lista_cliente()

#Ventana presupuestos
	#Mostrar producto en tabla
	def datos_en_tabla(self,event=None):
		self.tablaPresupuesto.delete(*self.tablaPresupuesto.get_children())
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("""SELECT id_producto, producto, cantidad, precio_venta, cantidad*precio_venta as pretotal
							FROM temporalpresupuesto
					""")
		datos=cursor.fetchall()
		for (id_prod,producto,stock,precio_venta,pretotal) in datos:
			self.tablaPresupuesto.insert('', 'end', values=(id_prod,producto,stock,precio_venta,pretotal))
		conexion.commit()
		conexion.close()

	#Datos del producto seleccionado
	def datos_para_presupuesto(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		producto=[self.list1.selection_get()]
		cursor.execute("SELECT * FROM productos WHERE producto=(?)", producto)
		admin=cursor.fetchall()
		for datos in admin:
			self.id_producto.set(datos[0])
			self.producto.set(datos[3])
			self.precio_venta.set(datos[6])
		conexion.commit()
		conexion.close()
		self.e3.focus()

	#Mostrar datos en tabla
	def agregar_al_presupuesto(self,event=None):
		try:
			id_prod=int(self.id_producto.get())
			producto=str(self.producto.get())
			cant=int(self.cant_presupuesto.get())
			precio_venta=float(self.precio_venta.get())
			pretotal=float(round((cant*precio_venta),2))

			conexion=self.conectar()
			cursor=conexion.cursor()
			datos=[
				id_prod,
				producto,
				cant,
				precio_venta,
				pretotal
			]
			cursor.execute('''CREATE TABLE IF NOT EXISTS temporalpresupuesto 
					(id INTEGER PRIMARY KEY AUTOINCREMENT,
					id_producto INTEGER UNIQUE,
					producto TEXT ,
					cantidad INTERGER,
					precio_venta REAL,
					pretotal REAL,
					FOREIGN KEY ("id_producto") REFERENCES productos (id))
					''')
			cursor.execute('INSERT INTO temporalpresupuesto VALUES (NULL,?,?,?,?,?)', datos )
			conexion.commit()
			self.datos_en_tabla()
			self.suma_subtotales_presupuesto()
			self.sumaTotales_presupuesto()
			self.id_producto.set('')
			self.producto.set('')
			self.cant_presupuesto.set('')
			self.precio_venta.set('')
			self.entryProd_presupuesto.focus()
			conexion.close()
		except IntegrityError:
			messagebox.showerror('Error', 'Ya hay un elemento igual agregado')
			self.producto.set('')
			self.entryProd_presupuesto.focus()
		except TclError:
			pass
		except OperationalError as error:
			print(error)
			messagebox.showerror('Se produjo un error', 'Vuelva a interntar agregar el producto')

	#Recuperar presupuesto incompleto
	def recuperar_presupuesto(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("""SELECT id_producto, producto, cantidad, precio_venta,
								cantidad*precio_venta as "pretotal"
							FROM temporalpresupuesto""")
			datos=cursor.fetchall()
			for (id_prod,producto,stock,precio_venta,pretotal) in datos:
				self.tablaPresupuesto.insert('', 'end', values=(id_prod,producto,stock,precio_venta,pretotal))
			conexion.commit()
			self.datos_en_tabla()
			self.suma_subtotales_presupuesto()
			self.sumaTotales_presupuesto()
			conexion.close()
		except sqlite3.OperationalError:
			messagebox.showinfo('Sin Datos', 'No se registran datos a recuperar')

	#Eliminar presupuesto incompleta
	def descartar_presupuesto(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute('DROP TABLE temporalpresupuesto')
			conexion.close()
			self.limpiar_presupuesto()
			self.suma_subtotales_presupuesto()
			self.sumaTotales_presupuesto()
		except sqlite3.OperationalError:
			messagebox.showinfo('Limpieza', 'No hay mas que limpiar')
		
	#Sacar de lista presupuesto
	def eliminar_de_presupuesto(self,event=None):
		seleccion=self.tablaPresupuesto.item(self.tablaPresupuesto.selection())['values']
		prod_busq=[str(seleccion[1])]
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('DELETE FROM temporalpresupuesto WHERE producto=(?)',prod_busq)					
		conexion.commit()
		conexion.close()

		self.tablaPresupuesto.delete(self.tablaPresupuesto.selection())
		self.datos_en_tabla()
		self.suma_subtotales_presupuesto()
		self.sumaTotales_presupuesto()
		self.id_producto.set('')
		self.producto.set('')
		self.cant_presupuesto.set('')
		self.precio_venta.set('')
		self.entryProd_presupuesto.focus()

	#Finalizar presupuesto 
	def finalizar_presupuesto(self,event=None):
		if self.cliente.get() == '' :
			messagebox.showerror('Error', 'Corroborar que se haya ingresado el cliente')
		elif self.titular.get()== '':
			messagebox.showerror('Error', 'Corroborar que se haya ingresado el CBU')
		else:
			self.sumaTotales_presupuesto()
			conexion=self.conectar()
			cursor=conexion.cursor()
			cliente=str(self.cliente.get())
			cursor.execute("SELECT id FROM clientes WHERE cliente=?",[cliente])
			id_cliente=cursor.fetchone()
			sub_total=self.subtotal.get()
			porc_desc=self.porcentaje_descuento.get()
			monto_desc=self.descuento.get()
			envio=(self.con_envio.get())+1
			try:
				monto_envio=self.envio.get()
			except _tkinter.TclError:
				sinmonto=messagebox.askyesno('Sin datos', 'El casillero está vacio, ¿Desea continuar sin completarlo?')
				if sinmonto==True:
					monto_envio=0.0
					self.envio.set(0)
			total=str(self.total_presupuesto.get())
			estado=6
			datos=[
				self.fecha,
				id_cliente[0],
				sub_total,
				porc_desc,
				monto_desc,
				envio,
				monto_envio,
				total,
				estado
			]
			cursor.execute('INSERT INTO presupuestos VALUES (NULL,?,?,?,?,?,?,?,?,?)', datos )
			cursor.execute("SELECT * FROM presupuestos ORDER BY id DESC LIMIT 1")
			id=[]
			for i in cursor.fetchall():
				id.append(i[0])			
			conexion.commit()
		
			cursor.execute('SELECT * FROM temporalpresupuesto')
			datos=cursor.fetchall()
			for i in datos:
				info=[id[0],i[1],i[3],i[4]]
				cursor.execute('INSERT INTO detalle_presupuestos VALUES (NULL,?,?,?,?)', info)

			#Creacion de PDF
			self.pdf_presupuesto()

			#Envio de mail
			envio_mail=messagebox.askyesno('Enviar mail', '¿Desea mail de confirmación del pedido?')
			if envio_mail == True:
				self.mail_presupuesto()
			else:
				pass

			#Eliminar tabla temporal de presupuestos
			cursor.execute('DROP TABLE temporalpresupuesto')
			conexion.commit()

			#Limpiar datos de pantalla
			self.limpiar_presupuesto()

			conexion.close()	

	#Limpiar pantalla
	def limpiar_presupuesto(self):
		self.tablaPresupuesto.delete(*self.tablaPresupuesto.get_children())
		self.id_presupuesto.set('')
		self.cliente.set('')
		self.producto.set('')
		self.cant_presupuesto.set('')
		self.precio_venta.set('')
		self.subtotal.set('')
		self.porcentaje.set(0.0)
		self.descuento.set(0.0)
		self.envio.set(0.0)
		self.total_presupuesto.set('')
		self.prto_sin_conf()
		self.con_envio.set(0)

#Ventana Buscar Presupuesto
	#Buscar presupuesto
	def buscadorPresupuesto(self,event=None):
		self.tablaCtePrto.delete(*self.tablaCtePrto.get_children())
		conexion=self.conectar()
		cursor=conexion.cursor()
		busqueda=self.buscarPresupuesto.get()
		cursor.execute("""SELECT PR.id, CL.cliente, PR.fecha, PR.total, EN.descripcion, ES.descripcion from presupuestos as PR
				INNER join
				clientes as CL
				on PR.id_cliente=CL.id
					inner JOIN
					envios as EN
					on PR.id_envio=EN.id
						INNER JOIN
						estados as ES
						on PR.id_estado=ES.id
				WHERE CL.cliente LIKE ? or PR.id LIKE ? or PR.fecha LIKE ? or PR.total LIKE ? """, (f'%{busqueda}%',f'%{busqueda}%',f'%{busqueda}%',f'%{busqueda}%',))#LIKE para buscar coincidencias en una columna. %% comodin de busqueda
		datos=cursor.fetchall()
		for (id, cliente, fecha, total, estado, envio) in datos:
				self.tablaCtePrto.insert('','end',values=(id, cliente, fecha, total, estado, envio))
		self.buscarPresupuesto.set('')
		conexion.commit()
		conexion.close()
		self.tablaCtePrto.selection()

		#Selecion en tabla Busqueda
	
	def items_prto(self, event=None):
		self.tablaListaPrto.delete(*self.tablaListaPrto.get_children())
		seleccion=self.tablaCtePrto.item(self.tablaCtePrto.selection())['values']
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("""SELECT PD.producto, DPR.cantidad FROM detalle_presupuestos as DPR
					INNER JOIN
					productos as PD
					on DPR.id_producto =PD.id
						INNER JOIN
						presupuestos as PR
						on DPR.id_presupuesto=PR.id
					WHERE DPR.id_presupuesto LIKE ? """, [int(seleccion[0])])
		elementos=cursor.fetchall()
		for (i,e) in elementos:
			self.tablaListaPrto.insert('', 'end', values=(i,e))

#Ventana Pedidos
	#Presupuestos sin fonfirmar
	def prto_sin_conf(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT * FROM presupuestos WHERE id_estado = 6 ")
		presupuestos=[]
		for i in cursor.fetchall():
			id_prto=i[0]
			id_cliente=i[2]
			cursor.execute("SELECT cliente FROM clientes WHERE id=?", [id_cliente])
			cliente=cursor.fetchone()
			presupuestos.append((id_prto,cliente[0]))
		lista=[]
		for i in presupuestos:
			nombre=f'N° {i[0]} - {i[1]}'
			lista.append(nombre)
		return lista
		conexion.commit()
		conexion.close()

	#Funcion para poner detalles de productos en tabla pedidos
	def prto_en_tabla (self, event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='temporalpedido'")
		if cursor.fetchall() ==[]:
			self.detalle_prto_tabla()
		else:
			sobreescribir=messagebox.askyesno(message='Hay una pedido pre-cargado sin confirmar, ¿Desea sobreescribirlo?', title='Pedido pendiente')
			if sobreescribir==True:
				cursor.execute('DROP TABLE temporalpedido')
				self.detalle_prto_tabla()
			else:
				self.cliente.set(''),
				self.pagos.set(''),
				self.presupuesto.set(''),
				self.cant_pedido.set('')
				self.subtotal.set(''),
				self.porcentaje_descuento.set(0.0)
				self.descuento.set(0.0)		
				self.total_compra.set('')
				self.tablaPedido.delete(*self.tablaPedido.get_children())
				self.cbCliente.focus()

	#Detalle productos del presupuesto 
	def detalle_prto_tabla(self, event=None):
		self.tablaPedido.delete(*self.tablaPedido.get_children())
		conexion=self.conectar()
		cursor=conexion.cursor()
		prto=self.presupuesto.get()
		prto=prto.split('N° ')
		detalle_prto=prto[1].split(' - ')
		id_prto=detalle_prto[0]
		cliente=detalle_prto[1]
		
		cursor.execute("""SELECT DPR.id_producto, PD.producto, DPR.cantidad, DPR.precio_unitario, DPR.cantidad*DPR.precio_unitario as pretotal
				FROM detalle_presupuestos as DPR
					INNER JOIN
					productos as PD
					on DPR.id_producto = PD.id
						INNER JOIN
						presupuestos as PR
						on DPR.id_presupuesto = PR.id
						WHERE DPR.id_presupuesto LIKE ? """, [id_prto])
		
		detalle=cursor.fetchall()
		
		for i in detalle:
			
			cursor.execute('SELECT stock FROM productos WHERE id LIKE ?', [i[0]])
			stock=cursor.fetchone()[0]
			if stock-i[2]<0:
				messagebox.showerror('ERROR', f'No dispone de:\n\n{i[2]} unidades de\n{i[1]},\npara realizar la venta.\n\nSTOCK ACTUAL: {stock} unidades.')
			else:
				for (id_prod,prod,cantidad,unitario,total) in [i]:
					self.tablaPedido.insert('', 'end', values=(id_prod,prod,cantidad,unitario,total))

				cursor.execute('''CREATE TABLE IF NOT EXISTS temporalpedido
						(id INTEGER PRIMARY KEY AUTOINCREMENT,
						id_producto INTEGER UNIQUE,
						cantidad INTEGER,
						precio_venta REAL
						)''')

				cursor.execute('INSERT INTO temporalpedido VALUES (NULL,?,?,?)',(id_prod,cantidad,unitario) )

				cursor.execute('SELECT descuento, id_envio, monto_envio FROM presupuestos WHERE id LIKE ?', [id_prto])
				extras=cursor.fetchone()
				self.porcentaje_descuento.set(extras[0])
				if extras[1]== 2:
					self.con_envio.set(1)
					self.envio.set(extras[2])

		self.cliente.set(cliente)
		conexion.commit()
		conexion.close()
		self.suma_subtotales_pedido()
		self.sumaTotales_pedido()
		self.boton_recargo
		
	#Mostrar producto en tabla
	def datos_en_tabla_pedido(self,event=None):
		try:
			self.tablaPedido.delete(*self.tablaPedido.get_children())
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("""SELECT TP.id_producto, PD.producto, TP.cantidad, TP.precio_venta, TP.cantidad*TP.precio_venta as pretotal
						FROM temporalpedido as TP
							INNER JOIN
							productos as PD
							on TP.id_producto = PD.id""")
			datos=cursor.fetchall()
			for (id_prod, producto,stock,precio_venta,pretotal) in datos:
				self.tablaPedido.insert('', 'end', values=(id_prod, producto,stock,precio_venta,pretotal))
			conexion.commit()
			conexion.close()
		except sqlite3.OperationalError as error:
			print(error)

	#Datos del producto seleccionado
	def datos_para_pedido(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		producto=[self.list1.selection_get()]
		cursor.execute("SELECT * FROM productos WHERE producto=(?)", producto)
		admin=cursor.fetchall()
		for datos in admin:
			self.id_producto.set(datos[0])
			self.producto.set(datos[3])
			self.precio_venta.set(datos[6])
		conexion.commit()
		conexion.close()
		self.cant_pedido_entry.focus()

	#Mostrar datos en tabla
	def agregar_al_pedido(self,event=None):
		try:
			id_prod=int(self.id_producto.get())
			producto=str(self.producto.get())
			cant=int(self.cant_pedido.get())
			precio_venta=float(self.precio_venta.get())
			self.stock_disponible(id_producto=id_prod, cantidad=cant, producto=producto, precio_venta=precio_venta)
			
			self.datos_en_tabla_pedido()
			self.suma_subtotales_pedido()
			self.sumaTotales_pedido()
			self.boton_recargo()
			self.id_producto.set('')
			self.producto.set('')
			self.cant_pedido.set('')
			self.precio_venta.set('')
			self.entryProd_pedido.focus()

		except IntegrityError as error:
			messagebox.showerror('Error', 'Ya hay un elemento igual agregado')
			self.producto.set('')
			self.entryProd_pedido.focus()

	#Corroborar stock
	def stock_disponible(self, id_producto=None, cantidad=None, producto=None, precio_venta=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('SELECT stock FROM productos WHERE id LIKE ?', [id_producto])
		stock=cursor.fetchone()[0]
		#Corroboramos que haya stock suficiente para descontar
		if stock-cantidad<0:
			#Si no hay, avisamos que con el ID seleccionadado no hay suficientes.
			messagebox.showerror('ERROR', f'No dispone de:\n\n{cantidad} unidades de\n{producto},\npara realizar la venta.\n\nSTOCK ACTUAL: {stock} unidades.')
			self.duplicado_en_tabla (id_producto, cantidad, precio_venta)	
		else:
			self.tabla_venta_temporal(id_producto, cantidad, precio_venta)
		conexion.commit()
		conexion.close()

	#Producto duplicado en tabla y cambio de proveedor
	def duplicado_en_tabla (self, id_producto=None, cantidad=None, precio_venta=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('SELECT producto FROM productos WHERE id LIKE ?', [id_producto])
		producto=cursor.fetchone()[0]
		cursor.execute('SELECT id FROM productos WHERE producto LIKE ? ORDER BY stock DESC', [producto])
		nuevo_id_producto=cursor.fetchall()
		if len(nuevo_id_producto)>1:
			cursor.execute('SELECT stock FROM productos WHERE id LIKE ?', nuevo_id_producto[0])
			stock_nuevo_id=cursor.fetchone()[0]
			if stock_nuevo_id-cantidad<0:
				pass
			else:
				cambio_id_producto=messagebox.askyesno('Cambio de proveedor', f'Pero del mismo producto\n hay disponibles: {stock_nuevo_id} unidades\nde otro proveedor\n\n¿Desea continuar cambiando el proveedor del producto?')
				if cambio_id_producto==True:
					self.tabla_venta_temporal(nuevo_id_producto[0][0], cantidad, precio_venta)			
		conexion.commit()
		conexion.close()

	#Crear y agregar a tabla temporal
	def tabla_venta_temporal(self, id_producto=None, cantidad=None, precio_venta=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		datos=[
			id_producto,
			cantidad,
			precio_venta
		]
		cursor.execute('''CREATE TABLE IF NOT EXISTS temporalpedido 
				(id INTEGER PRIMARY KEY AUTOINCREMENT,
				id_producto INTERGER UNIQUE,
				cantidad INTERGER,
				precio_venta REAL)
				''')
		cursor.execute('INSERT INTO temporalpedido VALUES (NULL,?,?,?)', datos )
		conexion.commit()
	
	#Recuperar pedido incompleto
	def recuperar_pedido(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("""SELECT TP.id_producto, PD.producto, TP.cantidad, TP.precio_venta, TP.cantidad*TP.precio_venta as pretotal
						FROM temporalpedido as TP
						INNER JOIN	productos as PD
							on TP.id_producto = PD.id""")
			datos=cursor.fetchall()
			for (id_prod,producto,stock,precio_venta,pretotal) in datos:
				self.tablaPedido.insert('', 'end', values=(id_prod,producto,stock,precio_venta,pretotal))
			conexion.commit()
			self.datos_en_tabla_pedido()
			self.suma_subtotales_pedido()
			self.sumaTotales_pedido()
			conexion.close()
			
		except sqlite3.OperationalError as error:
			print(error)
			messagebox.showinfo('Sin Datos', 'No se registran datos a recuperar')

	#Eliminar pedido incompleto
	def descartar_pedido(self,event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute('DROP TABLE temporalpedido')
			conexion.close()
			self.limpiar_pedido()
		except sqlite3.OperationalError:
			messagebox.showinfo('Limpieza','No hay mas que limpiar')
				
	#Sacar de lista pedido
	def eliminar_de_pedido(self,event=None):
		seleccion=self.tablaPedido.item(self.tablaPedido.selection())['values']
		id_seleccion=[str(seleccion[0])]
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('DELETE FROM temporalpedido WHERE id_producto=(?)',id_seleccion)					
		conexion.commit()
		conexion.close()

		self.tablaPedido.delete(self.tablaPedido.selection())
		self.datos_en_tabla_pedido()
		self.suma_subtotales_pedido()
		self.sumaTotales_pedido()
		self.boton_recargo()
		self.boton_recargo                                                                                                                 
		self.producto.set('')
		self.cant_pedido.set('')
		self.precio_venta.set('')
		self.entryProd_pedido.focus()
	
	#Finalizar pedido
	def comando_finalizar(self, event=None):
		if self.cliente.get()==None or self.cliente.get()=='':
			cliente=messagebox.askyesno('Cliente sin designar', '¿Desea continuar sin incorporar el cliente?')
			if cliente== True:
				if self.pagos.get()==''or self.pagos.get()== None:
					messagebox.showerror('Medios de pago', 'Debe indicar una forma de pago')
		elif self.pagos.get()==''or self.pagos.get()== None:
			messagebox.showerror('Medios de pago', 'Debe indicar una forma de pago')
			
		else:
			self.finalizar_pedido()
		
	#Funcion finalizar
	def finalizar_pedido(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("""SELECT * FROM temporalpedido""")
		datos=cursor.fetchall()
		
		#Datos actualizados del stock de los productos ingresados en la venta
		for i in datos:
			cursor.execute("""UPDATE productos
								SET stock = (SELECT PR.stock - TP.cantidad
										FROM productos as PR
										INNER JOIN temporalpedido as TP
										on PR.id=TP.id_producto)
								WHERE id LIKE ?""",(i[1],))
			conexion.commit()

		#Datos del comprobante de venta
		cliente=self.cliente.get()
		fecha_venta=self.fecha
		try:
			presupuesto=str(self.presupuesto.get()).split(sep=' - ')
			id_presupuesto=str((presupuesto[0].split(sep='N° '))[1])
		except IndexError:
			id_presupuesto=''
		medio_pago=self.pagos.get()
		sub_total=self.subtotal.get()
		descuento=self.porcentaje_descuento.get()
		envio=self.enviobd()
		monto_envio=self.envio.get()
		recargo=self.recargo.get()
		
		cursor.execute(" SELECT id FROM clientes WHERE cliente LIKE ? " ,[cliente])
		id_cliente=cursor.fetchone()[0]
	
		cursor.execute("SELECT id FROM medios_pagos WHERE tipo LIKE ? ",[medio_pago])
		id_medio_pago=cursor.fetchone()[0]

		cursor.execute("SELECT id FROM envios WHERE descripcion LIKE ? ",[envio])
		id_envio=cursor.fetchone()[0]

		datos_venta=[
			fecha_venta,
			id_cliente,
			id_medio_pago,
			id_presupuesto,
			sub_total,
			descuento,
			id_envio,
			monto_envio,
			recargo
		]
		try:
			cursor.execute(""" INSERT INTO pedidos
								(id,
								fecha,
								id_cliente,
								id_pago,
								id_presupuesto,
								sub_total,
								descuento,
								id_envio,
								monto_envio,
								recargo,
								id_estado)
						VALUES (NULL,?,?,?,?,?,?,?,?,?,1) """ ,datos_venta)
			conexion.commit() 
		

			#DETALLE DE LA COMPRA
			cursor.execute(" SELECT id FROM pedidos ORDER BY id DESC")
			id_pedido=cursor.fetchone()[0]

			cursor.execute("SELECT * FROM temporalpedido")
			datos=cursor.fetchall()
			detalle_venta=[]
			for i in datos:
				detalle_venta.append((id_pedido,i[1],i[2],i[3]))
			for i in detalle_venta:
				cursor.execute("""INSERT INTO detalle_pedidos 
							(id, id_pedido, id_producto, cantidad, precio_unitario)
							VALUES (NULL,?,?,?,?)""", i)
			conexion.commit()
			
			#Actualizacion de las cuentas
			id_tipo=2
			datos=[
				id_tipo,
				id_medio_pago,
				self.periodo,
				self.total_pedido.get()
			]
			cursor.execute('INSERT INTO estado_cuentas VALUES (NULL,?,?,?,?)',datos)
			conexion.commit() 

			#Actualizar estado de presupuesto
			if id_presupuesto!='':
				cursor.execute('UPDATE presupuestos SET id_estado=? WHERE id=?', [1,id_presupuesto])
				conexion.commit()
			
		except Error as error:
			print(error)
			
		#Limpiar pantalla finalizado el trabajo
		cursor.execute('DROP TABLE temporalpedido')
		conexion.commit()
		conexion.close()

		#ver pdf del pedido
		self.pdf_pedido()
		#Envio de mail
		mail=messagebox.askyesno('Envío mail','¿Desea enviar mail con el pedido adjunto?')
		if mail==True:
			self.mail_pedido()
		
				
		#Limpiar pantalla
		self.limpiar_pedido()
		
	#Limpiar pantalla
	def limpiar_pedido (self):
		self.tablaPedido.delete(*self.tablaPedido.get_children())
		self.cliente.set(''),
		self.pagos.set(''),
		self.presupuesto.set(''),
		self.cant_pedido.set('')
		self.subtotal.set(''),
		self.porcentaje_descuento.set(0.0)
		self.descuento.set(0.0)		
		self.total_pedido.set('')
		self.prto_sin_conf()
		self.con_envio.set(0)
		self.envio.set('')
		self.con_recargo.set(0)
		self.recargo.set('')
		self.cbCliente.focus()
		self.suma_subtotales_pedido()
		self.sumaTotales_pedido()
		self.boton_recargo()

#Ventana Buscar pedidos
	#Buscar pedidos
	def buscadorPedido(self,event=None):
		self.tablaCtePdo.delete(*self.tablaCtePdo.get_children())
		conexion=self.conectar()
		cursor=conexion.cursor()
		busqueda=self.buscarPedido.get()
		cursor.execute("""SELECT PD.id, CL.cliente, PD.fecha, PD.sub_total+PD.descuento+PD.monto_envio as Total, ES.descripcion, EN.descripcion from pedidos as PD
				INNER join
				clientes as CL
				on PD.id_cliente=CL.id
					inner JOIN
					envios as EN
					on PD.id_envio=EN.id
						INNER JOIN
						estados as ES
						on PD.id_estado=ES.id
				WHERE CL.cliente LIKE ? or PD.id LIKE ? or PD.fecha LIKE ? """,(f'%{busqueda}%',f'%{busqueda}%',f'%{busqueda}%',))#LIKE para buscar coincidencias en una columna. %% comodin de busqueda
		datos=cursor.fetchall()
		for (id, cliente, fecha, total, estado, envio) in datos:
				self.tablaCtePdo.insert('','end',values=(id, cliente, fecha, total, estado, envio))
		self.buscarPedido.set('')
		conexion.commit()
		conexion.close()
		self.tablaCtePdo.selection()

	def items_pdo(self, event=None):
		self.tablaListaPdo.delete(*self.tablaListaPdo.get_children())
		seleccion=self.tablaCtePdo.item(self.tablaCtePdo.selection())['values']
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("""SELECT PD.producto, DPD.cantidad FROM detalle_pedidos as DPD
					INNER JOIN
					productos as PD
					on DPD.id_producto =PD.id
					INNER JOIN
					pedidos as PE
					on DPD.id_pedido=PE.id
					WHERE DPD.id_pedido LIKE ? """, [int(seleccion[0])])
		elementos=cursor.fetchall()
		for (i,e) in elementos:
			self.tablaListaPdo.insert('', 'end', values=(i,e))

#Ventana Cuentas
	#Lista inicial de cuentas
	def listado_cuenta(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT titular FROM cuenta_bancaria")
		lista=[]
		for row in cursor.fetchall():
			lista.append(row[0])
			lista.sort()
		return lista
		conexion.commit()
		conexion.close()

	#Datos de la cuenta seleecionado
	def mostrar_datos_cuenta(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		titular=[self.lista_cuenta.selection_get()]
		cursor.execute("SELECT * FROM cuenta_bancaria WHERE titular=(?)", titular)
		admin=cursor.fetchall()
		for datos in admin:
			self.cbu.set(datos[1])
			self.alias.set(datos[2])
			self.titular.set(datos[3])
			self.dni.set(datos[4])
			self.id_Tribut.set(datos[5])
			self.cuenta.set(datos[6])
		conexion.commit()
		conexion.close()

	#Agregar cuenta
	def nva_cuenta(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		datos=[
			self.cbu.get(),
			self.alias.get(),
			self.titular.get(),
			self.dni.get(),
			self.id_Tribut.get(),
			self.cuenta.get()
			]
		cursor.execute("INSERT INTO cuenta_bancaria VALUES(NULL,?,?,?,?,?,?)", (datos))
		conexion.commit()
		messagebox.showinfo('Añadido', 'La cuenta se agregó exitosamente')
		self.cbu.set('')
		self.alias.set('')
		self.titular.set('')
		self.dni.set('')
		self.id_Tribut.set('')
		self.cuenta.set('')
		conexion.close()
		self.ver_lista_cuenta()
		
	#Eliminar Cuenta
	def elim_cuenta(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		titular=self.titular.get()
		cursor.execute("DELETE FROM cuenta_bancaria WHERE titular=(?)",[titular,])
		conexion.commit()
		messagebox.showinfo('Borrado', 'La cuenta se eliminó exitosamente')
		self.cbu.set('')
		self.alias.set('')
		self.titular.set('')
		self.dni.set('')
		self.id_Tribut.set('')
		self.cuenta.set('')
		conexion.close()
		self.ver_lista_cuenta()

	#Modificar proveedor
	def modif_cuenta(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		titular=self.titular.get()
		cursor.execute('''UPDATE cuenta_bancaria
			SET cbu=?, alias=?, titular=?, dni=?, id_tribut=?,cuenta=?
			WHERE titular=(?)''',
			[self.cbu.get(),
			self.alias.get(),
			self.titular.get(),
			self.dni.get(),
			self.id_Tribut.get(),
			self.cuenta.get(),
			titular])
		conexion.commit()
		conexion.close()
		messagebox.showinfo('Modificado', 'Los datos han sido modificados exitosamente')

#Ventana Configurar mail de envio
	#Lista de mails
	def lista_mail(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT mails FROM master_mails")
		lista=[]
		for row in cursor.fetchall():
			lista.append(row[0])
			lista.sort()
		return lista
		conexion.commit()
		conexion.close()

	#Mostrar datos proveedor
	def mostrar_datos_mail(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		mails=self.mail_principal.get()
		cursor.execute("SELECT * FROM master_mails WHERE mails=(?)", [mails,])
		admin=cursor.fetchall()
		for datos in admin:
			self.contrasenha.set(datos[2])
		conexion.commit()
		conexion.close()

	#Agregar proveedor
	def agregar_mail(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		estado='No activo'
		datos=[
			self.mail_principal.get(),
			self.contrasenha.get(),
			estado
			]
		cursor.execute("INSERT INTO master_mails VALUES(NULL,?,?,?)", (datos))
		conexion.commit()
		messagebox.showinfo('Añadido', 'El artículo se agregó exitosamente')
		self.mail_principal.set('')
		self.contrasenha.set('')
		self.master_mail_cb.focus()
		conexion.close()
		self.lista_mail()
		
	#Eliminar proveedor
	def eliminar_mail(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		mails=self.mail_principal.get()
		cursor.execute("DELETE FROM master_mails WHERE mails=(?)",[mails,])
		conexion.commit()
		messagebox.showinfo('Borrado', 'El artículo se eliminó exitosamente')
		self.mail_principal.set('')
		self.contrasenha.set('')
		self.master_mail_cb.focus()
		conexion.close()
		self.lista_mail()

	#Modificar proveedor
	def modificar_mail(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		mails=self.mail_principal.get()
		cursor.execute('''UPDATE master_mails
		SET mails=?, pass=?,
		WHERE mails=(?)''',
		[self.mail_principal.get(),self.contrasenha.get(),mails])
		conexion.commit()
		conexion.close()
		messagebox.showinfo('Modificado', 'Los datos han sido modificados exitosamente')

	def activar_mail(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("UPDATE master_mails  SET estado='No activo'")
		conexion.commit()
		mails=self.mail_principal.get()
		cursor.execute('''UPDATE master_mails
		SET estado='Activo'
		WHERE mails=(?)''',
		[mails])
		messagebox.showinfo('Activado', 'El mail seleccionado está configurado como predeterminado')
		self.mail_principal.set('')
		self.contrasenha.set('')
		self.master_mail_cb.focus()
		conexion.commit()
		self.mail_activo.set(self.mostrar_mail_master())
		conexion.close()
		
		
	def mostrar_mail_master(self):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT mails FROM master_mails WHERE estado='Activo'")
		mail=cursor.fetchall()
		for x in mail:
			return x[0]
		conexion.commit()
		conexion.close()

#Ventada Estados
	#Listas de segun opción busqueda
	def config_busqueda(self, event=None):
		if self.opcion.get()==1:
			id=self.buscarEstados.get()
			#Presupuestos
			self.tablaCtePrto.delete(*self.tablaCtePrto.get_children())
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("""SELECT PR.id, CL.cliente, PR.fecha, PR.total, ES.descripcion, EN.descripcion
							FROM presupuestos as PR
							INNER JOIN clientes as CL
								ON CL.id=PR.id_cliente
							INNER JOIN estados as ES
								ON ES.id=PR.id_estado
							INNER JOIN envios as EN
								ON EN.id=PR.id_envio
							WHERE PR.id LIKE ?""",([f'%{id}%']))
			datos=cursor.fetchall()
			for (id, proveedor, fecha, total, estado, envio) in datos:
				self.tablaCtePrto.insert('','end',values=(id, proveedor, fecha, total, estado, envio))
			#Pedidos
			self.tablaCtePdo.delete(*self.tablaCtePdo.get_children())
			cursor.execute("""SELECT PD.id, CL.cliente, PD.fecha, PD.sub_total+PD.descuento+PD.monto_envio as total, ES.descripcion, EN.descripcion
							FROM pedidos as PD
							INNER JOIN clientes as CL
								ON CL.id=PD.id_cliente
							INNER JOIN estados as ES
								ON ES.id=PD.id_estado
							INNER JOIN envios as EN
								ON EN.id=PD.id_envio
							WHERE PD.id LIKE ?""",([f'%{id}%']))
			datos=cursor.fetchall()
			if datos!=[]:
				for (id, proveedor, fecha, total, estado, envio) in datos:
					self.tablaCtePdo.insert('','end',values=(id, proveedor, fecha, total, estado, envio))
			else:
				cursor.execute("""SELECT PD.id, CL.cliente, PD.fecha, PD.sub_total+PD.descuento+PD.monto_envio as total, ES.descripcion, EN.descripcion
							FROM pedidos as PD
							INNER JOIN clientes as CL
								ON CL.id=PD.id_cliente
							INNER JOIN estados as ES
								ON ES.id=PD.id_estado
							INNER JOIN envios as EN
								ON EN.id=PD.id_envio""")
				datos=cursor.fetchall()
				for (id, proveedor, fecha, total, estado, envio) in datos:
					self.tablaCtePdo.insert('','end',values=(id, proveedor, fecha, total, estado, envio))
				

			conexion.commit()
		else:
			cliente=str(self.buscarEstados.get())
			#Presupuestos
			self.tablaCtePrto.delete(*self.tablaCtePrto.get_children())
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("""SELECT PR.id, CL.cliente, PR.fecha, PR.total, ES.descripcion, EN.descripcion
							FROM presupuestos as PR
							INNER JOIN clientes as CL
								ON CL.id=PR.id_cliente
							INNER JOIN estados as ES
								ON ES.id=PR.id_estado
							INNER JOIN envios as EN
								ON EN.id=PR.id_envio
							WHERE CL.cliente LIKE ?""",(f'%{cliente}%',))
			datos=cursor.fetchall()
			for (id, proveedor, fecha, total, estado, envio) in datos:
					self.tablaCtePrto.insert('','end',values=(id, proveedor, fecha, total, estado, envio))
			#Pedidos
			self.tablaCtePdo.delete(*self.tablaCtePdo.get_children())
			cursor.execute("""SELECT PD.id, CL.cliente, PD.fecha, PD.sub_total+PD.descuento+PD.monto_envio as total, ES.descripcion, EN.descripcion
							FROM pedidos as PD
							INNER JOIN clientes as CL
								ON CL.id=PD.id_cliente
							INNER JOIN estados as ES
								ON ES.id=PD.id_estado
							INNER JOIN envios as EN
								ON EN.id=PD.id_envio
							WHERE CL.cliente LIKE ?""",(f'%{cliente}%',))
			datos=cursor.fetchall()
			for (id, proveedor, fecha, total, estado, envio) in datos:
				self.tablaCtePdo.insert('','end',values=(id, proveedor, fecha, total, estado, envio))
			conexion.commit()
			conexion.close()
	
	#cambio de estados Presupuesto
	def cambiar_presupuesto (self, event=None):
		if self.estado_presupuesto.get()==1:
			self.Pedidos()
		elif self.estado_presupuesto.get()==2:
			seleccion=self.tablaCtePrto.item(self.tablaCtePrto.selection())['values']
			id=seleccion[0]
			cambio=2
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("UPDATE presupuestos SET id_estado=(?) WHERE id=(?)",(cambio,id))
			conexion.commit()
			self.config_busqueda()
		elif self.estado_presupuesto.get()==0:
			messagebox.showerror('Error','Debe seleccionar una opción de cambio de estado')
			pass
		else:
			#Cambio de estado
			seleccion=self.tablaCtePrto.item(self.tablaCtePrto.selection())['values']
			try:
				id=seleccion[0]
				cliente=seleccion[1]
				cambio=3
				conexion=self.conectar()
				cursor=conexion.cursor()
				cursor.execute("UPDATE presupuestos SET id_estado=(?) WHERE id=(?)",(cambio,id))
				conexion.commit()
				#Actualización lista
				self.config_busqueda()
			except IndexError:
				pass

	#cambio de estados Presupuesto
	def cambiar_pedido (self, event=None):
		if self.estado_pedido.get()==1:
			seleccion=self.tablaCtePdo.item(self.tablaCtePdo.selection())['values']
			id=seleccion[0]
			cambio=4
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("UPDATE pedidos SET id_estado=(?) WHERE id=(?)",(cambio,id))
			conexion.commit()
			self.tablaCtePrto.delete(*self.tablaCtePrto.get_children())
			self.tablaCtePdo.delete(*self.tablaCtePdo.get_children())
			self.config_busqueda()
			
		elif self.estado_pedido.get()==0:
			messagebox.showerror('Error','Debe seleccionar una opción de cambio de estado')
			pass
		else:
			seleccion=self.tablaCtePdo.item(self.tablaCtePdo.selection())['values']
			id=seleccion[0]
			cambio=5
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute("UPDATE pedidos SET id_estado=(?) WHERE id=(?)",(cambio,id))
			conexion.commit()
			self.config_busqueda()
			conexion.commit()

#Ventana estados de cuentas
	#Periodos
	def periodos_cuentas(self, event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('SELECT fecha FROM estado_cuentas GROUP BY fecha ORDER By fecha')
		periodos=['Todos']
		for i in cursor.fetchall():
			periodos.append(i)
		return periodos
			
	#Totales
	def totales_cuenta(self,event=None):
		periodo=self.rango_periodos.get()
		self.ing_efec.set(self.montos_por_medio_pago(medio_pago=2 , cuenta=2 , periodo=periodo ))
		self.ing_trans.set(self.montos_por_medio_pago(medio_pago=1 , cuenta=2 , periodo=periodo ))
		self.ing_debit.set(self.montos_por_medio_pago(medio_pago=5 , cuenta=2 , periodo=periodo ))
		self.ing_cred.set(self.montos_por_medio_pago(medio_pago=4 , cuenta=2 , periodo=periodo ))
		self.ing_mercado.set(self.montos_por_medio_pago(medio_pago=6 , cuenta=2 , periodo=periodo ))
		self.egre_efec.set(self.montos_por_medio_pago(medio_pago=2 , cuenta=1 , periodo=periodo ))
		self.egre_tran.set(self.montos_por_medio_pago(medio_pago= 1, cuenta= 1, periodo=periodo ))
		self.egre_debit.set(self.montos_por_medio_pago(medio_pago=5 , cuenta=1 , periodo=periodo ))
		self.egre_cred.set(self.montos_por_medio_pago(medio_pago=4 , cuenta=1 , periodo=periodo ))
		self.egre_mercado.set(self.montos_por_medio_pago(medio_pago=6 , cuenta=1 , periodo=periodo ))
		totales=round(float(self.montos_por_medio_pago(medio_pago='%%', cuenta=2, periodo=periodo))-float(self.montos_por_medio_pago(medio_pago='%%', cuenta=1, periodo=periodo)),2)
		if totales >=0.0:
			self.totales_cuentas.config(fg='green')
		else:
			self.totales_cuentas.config(fg='red')
		self.total_cuentas.set(totales)

	#Montos de las cuentas
	def montos_por_medio_pago (self, medio_pago=None, cuenta=None, periodo=None):
		periodo=self.rango_periodos.get()
		if periodo == 'Todos':
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute('SELECT SUM(monto) FROM estado_cuentas WHERE id_cuenta LIKE ? AND id_medio_pago LIKE ?',(cuenta,medio_pago) )
			total=cursor.fetchone()[0]
			if total==None:
				total=0
				return float(total)
			else:
				return float(total)
			
		else:
			conexion=self.conectar()
			cursor=conexion.cursor()
			total=0
			cursor.execute('SELECT monto FROM estado_cuentas WHERE id_cuenta LIKE ? AND id_medio_pago LIKE ? AND fecha LIKE ?',(cuenta,medio_pago,periodo))
			for monto in cursor.fetchall():
				total+=monto[0]
			if total==None:
				total=0
				return float(total)
			else:
				return float(total)

#Ventana Recargo tarjetas
	#Guardar datos ventana 
	def guardar_recargo(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		datos=[
			self.debito.get(),
			self.credito.get()
		]
		id_tarjeta=1
		for i in datos:
			cursor.execute('UPDATE recargo_tarjetas SET monto=? WHERE id=?', [datos[id_tarjeta-1],id_tarjeta])
			id_tarjeta+=1
		messagebox.showinfo('Correcto', 'Se guardo ajuste correctamente')
		
		conexion.commit()
		conexion.close()

	#Mostrar debito
	def mostrar_recargo(self,tipo_tarjeta=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT monto FROM recargo_tarjetas WHERE id LIKE ?", [tipo_tarjeta])
		monto=cursor.fetchone()[0]
		conexion.commit()
		conexion.close()
		return monto

#Ventana Modificación cuerpo de mail predeterminado
	#Lista de otras opciones
	def otras_opciones (self, event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('SELECT varios FROM opciones_mail WHERE opcion="Otros" ')
		lista=[]
		for i in cursor.fetchall() :
			lista.append(i[0])
		conexion.commit()
		conexion.close()
		return lista

	#Seleccion de opción
	def seleccion (self, event=None):
		try:
			conexion=self.conectar()
			cursor=conexion.cursor()
			if self.opcion.get()==1:
				self.cuerpo_mail.delete(1.0, 'end')
				self.opciones_otros.config(state='disabled')
				cuerpo=[]
				cursor.execute('SELECT cuerpo FROM opciones_mail WHERE opcion="Presupuestos" ')
				cuerpo.append(cursor.fetchone()[0])
				self.cuerpo_mail.insert(1.0,cuerpo[0])
			elif self.opcion.get()==2:
				self.cuerpo_mail.delete(1.0, 'end')
				self.opciones_otros.config(state='disabled')
				cuerpo=[]
				cursor.execute('SELECT cuerpo FROM opciones_mail WHERE opcion="Pedidos" ')
				cuerpo.append(cursor.fetchone()[0])
				self.cuerpo_mail.insert(1.0,cuerpo[0])
			elif self.opcion.get()==3:
				self.cuerpo_mail.delete(1.0, 'end')
				self.opciones_otros.config(state='disabled')
				cuerpo=[]
				cursor.execute('SELECT cuerpo FROM opciones_mail WHERE opcion="Listas de precios" ')
				cuerpo.append(cursor.fetchone()[0])
				self.cuerpo_mail.insert(1.0,cuerpo[0])
			else:
				self.opciones_otros.config(state='normal')
				self.cuerpo_mail.delete(1.0, 'end')
			conexion.commit()
			conexion.close()
		except TypeError as error:
			print(error)
	
	#Seleccion de Otras opciones
	def seleccion_otros (self,event=None):
		self.cuerpo_mail.delete(1.0, 'end')
		conexion=self.conectar()
		cursor=conexion.cursor()
		varios=[self.otros.get()]
		cuerpo=[]
		cursor.execute('SELECT cuerpo FROM opciones_mail WHERE opcion="Otros" AND varios=?', (varios))
		cuerpo.append(cursor.fetchone()[0])
		self.cuerpo_mail.insert(1.0,cuerpo[0])

	#Eliminar otros
	def eliminar_otros(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		otro=self.otros.get()
		cursor.execute("DELETE FROM opciones_mail WHERE varios=(?)",[otro,])
		conexion.commit()
		messagebox.showinfo('Borrado', 'Se eliminó la opción seleccionada')
		conexion.close()
		self.otras_opciones()
		self.opcion.set(0)
		self.otros.set('')
		self.cuerpo_mail.delete(1.0, 'end')
		

	#Guardado del cuerpo del mail
	def guardar_mail(self,event=None):
		cuerpo=self.cuerpo_mail.get(1.0,'end')#.replace('\n','<br>')
		opciones=self.opcion.get()
		varios=self.otros.get()
		seleccion=[]
		if opciones == 1:
			seleccion.append(('Presupuestos',''))
		elif opciones==2:
			seleccion. append(('Pedidos',''))
		elif opciones==3:
			seleccion.append(('Listas de precios',''))
		else:
			seleccion.append(('Otros',varios))
		
		self.datos_mail(seleccion=seleccion[0], opcion=seleccion[0][0], varios=seleccion[0][1], cuerpo=cuerpo)
				
		self.otras_opciones()
		self.opcion.set(0)
		self.otros.set('')
		self.cuerpo_mail.delete(1.0, 'end')

	#Guardar o actualizar cuerpo de mail
	def datos_mail (self,seleccion=None, opcion=None, varios=None, cuerpo=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('SELECT opcion, varios FROM opciones_mail WHERE opcion LIKE ? AND varios LIKE ?',(seleccion[0],seleccion[1]))
		resultado=cursor.fetchone()
		try:
			cursor.execute("INSERT INTO opciones_mail VALUES(NULL,?,?,?)", (opcion, varios, cuerpo))
			conexion.commit()
			messagebox.showinfo('Guardado', 'Se guardó correctamente el cuerpo del mail')
		except sqlite3.IntegrityError:
			cursor.execute('UPDATE opciones_mail SET cuerpo=? WHERE opcion LIKE ? AND varios LIKE ?',(cuerpo, opcion, varios))
			conexion.commit()
			messagebox.showinfo('Guardado', 'Se guardó correctamente el cuerpo del mail')
		conexion.close()

		
	#Formula generica para luego reemplazarlo por el nombre del cliente en el mail de envio
	def insertar_cliente(self, event=None):
		cliente='<i><b>{}</i></b>'
		self.cuerpo_mail.insert(self.cuerpo_mail.index("insert"),cliente)#posición del cursor en el texto
		
#Ventana envios de mail con adjuntos
	#Seleccion de opción
	def seleccion_para_enviar (self, event=None):
		if self.opcion.get()==1:
			self.opciones_otros.config(state='disabled')
			self.seleccion_cuerpo_mail(opcion='Presupuestos', varios='')
		elif self.opcion.get()==2:
			self.opciones_otros.config(state='disabled')
			self.seleccion_cuerpo_mail(opcion='Pedidos', varios='')
		elif self.opcion.get()==3:
			self.opciones_otros.config(state='disabled')
			self.seleccion_cuerpo_mail(opcion='Lista de precios', varios='')
		else:
			self.opciones_otros.config(state='normal')
	
	#Seleccion de Otras opciones
	def seleccion_otros_para_enviar(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		varios=self.otros.get()
		try:
			self.seleccion_cuerpo_mail(opcion='Otros', varios=varios)
		except sqlite3.InterfaceError:
			messagebox.showinfo(f'Otros {varios}','El cuerpo de mail no está configurado. Se enviará vacio.')
		
	#seleccion cuerpo
	def seleccion_cuerpo_mail(self, opcion=None, varios=None):
		cuerpo=[]
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('SELECT cuerpo FROM opciones_mail WHERE opcion LIKE ? AND varios LIKE ? AND EXISTS (SELECT * FROM opciones_mail WHERE opcion LIKE ? AND varios LIKE ?)', (opcion, varios,opcion, varios))
		cuerpo=cursor.fetchone()
		if cuerpo!=None:
			return str(cuerpo[0].replace('\n','<br>\n\t\t'))
		else:
			messagebox.showinfo(f'{opcion} {varios}','El cuerpo de mail no está configurado. Se enviará vacio.')
			return cuerpo

	#Mostrar mail cliente
	def mostrar_mail_cliente(self,event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cliente=[self.listaClientes.selection_get()]
		cursor.execute("SELECT * FROM clientes WHERE cliente=(?)", cliente)
		dato=cursor.fetchall()
		self.direcion_mail.insert('end',f'{dato[0][6]}, ')
		self.cliente.set(cliente[0])
		conexion.commit()
		conexion.close()
			
#----------------Funciones para tabla--------------	
#Busqueda
	#Selecion en tabla Busqueda
	def seleccionar_buscador(self,event=None):
		self.seleccion=self.tabla.item(self.tabla.selection())['values']

#Compras
	#Busqueda por letra
	def busq_list(self,event=None): 
		value = event.widget.get() 
		if value == '': 
			lista = self.lista_prod() 
		else: 
			lista = [] 
			for item in self.lista_prod(): 
				if value.lower() in item.lower(): 
					lista.append(item)				 
		
		self.lista_busq_prod(lista) 

	#Actualización lista de productos
	def lista_busq_prod(self, lista):
		self.list1.delete(0, 'end')
		for item in lista:
			self.list1.insert('end', item)

	#Selecion en tabla Compras
	def seleccionar_compra(self,event=None):
		self.seleccion=self.tablaCompras.item(self.tablaCompras.selection())['values']

#Clientes
	#Busqueda por letra de clientes
	def busq_cliente(self,event=None): 
		value = event.widget.get() 
		if value == '': 
			lista = self.lista_cliente() 
		else: 
			lista = [] 
			for item in self.lista_cliente(): 
				if value.lower() in item.lower(): 
					lista.append(item)				 
		
		self.lista_busq_cliente(lista) 

	#Actualización lista de clientes
	def lista_busq_cliente(self, lista):
		self.listaClientes.delete(0, 'end')
		for item in lista:
			self.listaClientes.insert('end', item)

#Cuentas
	#Actualización lista de productos
	def ver_lista_cuenta(self, lista):
		self.lista_cuenta.delete(0, 'end')
		for item in lista:
			self.lista_cuenta.insert('end', item)

	#Selecion en tabla Compras
	def seleccionar_compra(self,event=None):
		self.seleccion=self.tablaCompras.item(self.tablaCompras.selection())['values']

#Ventada Estados
	#Tabla Presupuestos
	def selecion_presupuesto (self,event=None):
		seleccion=self.tablaCtePrto.item(self.tablaCtePrto.selection())['values']
		estado=seleccion[4]

		if estado=='Sin confirmación':
			self.reconsultado_radio.config(state='normal')
			self.cancelar_radio.config(state='normal')
			self.confirmar_radio.config(state='normal')
		elif estado=='Reconsultado':
			self.reconsultado_radio.config(state='disabled')
			self.cancelar_radio.config(state='normal')
			self.confirmar_radio.config(state='normal')
		else:
			self.reconsultado_radio.config(state='disabled')
			self.cancelar_radio.config(state='disabled')
			self.confirmar_radio.config(state='disabled')

	#Tabla Pedido
	def selecion_pedido (self,event=None):
		seleccion=self.tablaCtePdo.item(self.tablaCtePdo.selection())['values']
		envio=seleccion[5]
		estado=seleccion[4]
		if envio=='Con envio' and estado=='Confirmado':
			self.retirado_radio.config(state='disabled')
			self.enviado_radio.config(state='normal')
		elif envio=='Sin envio' and estado=='Confirmado':
			self.retirado_radio.config(state='normal')
			self.enviado_radio.config(state='disabled')
		else:
			self.retirado_radio.config(state='disabled')
			self.enviado_radio.config(state='disabled')
		
#----------------Funciones extras------------------
#Funciones varias
	#Ubicación del programa	
	def ubicacion (self, event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute('SELECT ubicacion FROM ubicacion WHERE estado="activo"')
		if cursor.fetchall()== []:
			messagebox.showinfo('Definir ubicacion', 'Para continuar debe seleccionar donde se ubica el programa')
			self.definir_ubicacion()
			conexion=self.conectar()
			cursor=conexion.cursor()
			cursor.execute('SELECT ubicacion FROM ubicacion WHERE estado="activo"')
			ubicacion=cursor.fetchall()
			conexion.commit()
			return (ubicacion[0])[0]
		else:
			cursor.execute('SELECT ubicacion FROM ubicacion WHERE estado="activo"')
			ubicacion=cursor.fetchall()
			conexion.commit()
			return (ubicacion[0])[0]

	def definir_ubicacion (self, event=None):
		conexion=self.conectar()
		cursor=conexion.cursor()
		directorio=filedialog.askdirectory()
		if directorio!='':
			os.chdir(directorio)
		ubicacion=os.getcwd()
		estado='activo'
		datos=[ubicacion, estado]
		cursor.execute("INSERT INTO ubicacion VALUES(NULL,?,?)", (datos))
		conexion.commit()
		conexion.close()
		
	#Precio de venta
	def calculo_venta(self,costo=None,redondeo=None,porcentaje=None):
		valor_venta=(costo*(1+(porcentaje/100)))
		final=int(redondeo*ceil(valor_venta/redondeo))
		final=float(final)
		return final

	#Boton nuevo articulo
	def nuevo_articulo(self,event=None):
		self.id_producto.set('')
		self.codigo.set('')
		self.proveedor.set('')
		self.producto.set('')
		self.stock.set('')
		self.costo.set('')
		self.precio_venta.set('')
		self.Producto()

	#Menú Buscar PDF
	def buscar_pdf(self, event=None):
		directorio=filedialog.askopenfilename(initialdir="PDF's",title='Seleccionar archivo',filetypes=[("PDF files","*.pdf"),('all files', '.*')])
		os.system(directorio)

	#Menú Buscar Lista backup
	def buscar_backup(self, event=None):
		directorio=filedialog.askopenfilename(initialdir='Backup_stock',title='Seleccionar archivo',filetypes=[("xlsx files","*.xlsx"),('all files', '.*')])
		os.system(directorio)

#Armado de lista de precios publico
	def lista_pdf(self):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT fecha FROM lista_publico")
		lista=self.lista_venta()
		if lista!=[]:
			comprobar_existencia=cursor.fetchall()
			n=0
			for i in comprobar_existencia:
				if i[0]==self.fecha:
					n+=1
			if n>0:
				messagebox.showerror('Lista existente',f'Ya existe una lista del día de la fecha: {self.fecha}')
			else:
				cursor.execute("INSERT INTO lista_publico VALUES(NULL,?)", [self.fecha])
				cursor.execute("SELECT * FROM lista_publico ORDER BY id DESC LIMIT 1")
				id_lista=[]
				for i in cursor.fetchall():
					id_lista.append(i[0])			
				conexion.commit()
				id_lista=id_lista[0]
				nombre=f'n_{id_lista}'
				#Creación de archivo
				pdf= canvas.Canvas(f"PDF's\Lista_publico\{nombre}.pdf",pagesize=A5)#tamaño A5 = 420x595px
				styles = getSampleStyleSheet() 
				E1=[]
				for i in lista:
					E1.append([(Paragraph(i[0], styles["BodyText"]))])
				for i in range(0,len(lista)):
					lista[i][0]=E1[i]
					i+=1

				#Generación de lista de PDF

				min=0 #inicio de la lista
				max=15 #final de la lista
				c=15 #Elementos por lista
				div=(len(lista)//c) #Cantidad de listas
				r=0 #Repetición del bucle
				s=(len(lista)%c) #Elementos libres

				while len(lista)%c!=0 and len(lista)>=c:
					self.encabezado_lista_pdf(pdf)
					self.detalle_lista_pdf(pdf, lista[min:max],len(lista))
					min+=c
					max+=c
					r+=1
					pdf.showPage()
					if r==div:
						self.encabezado_lista_pdf(pdf)
						self.detalle_lista_pdf(pdf, lista[min:min+s],len(lista))
						break
					
				while len(lista)%c==0 :
					self.encabezado_lista_pdf(pdf)
					self.detalle_lista_pdf(pdf, lista[min:max],len(lista))
					min+=c
					max+=c
					r+=1
					pdf.showPage()
					if r==div:
						break

				if len(lista)<c:
					self.encabezado_lista_pdf(pdf)
					self.detalle_lista_pdf(pdf, lista[min:min+s],len(lista))

				pdf.save()

				os.system(f"{self.ubicacion()}\PDF's\Lista_publico\{nombre}.pdf")
		else:
			messagebox.showinfo('Lista vacia','No se encontraron artículos para ingresar en la lista')

	#Encabezado
	def encabezado_lista_pdf(self,pdf):
		pdf.drawImage("pdf_logo.png",30 ,510,width=60, height=61, mask='auto')
		pdf.setStrokeColorRGB(0.6171875,0.79296875,0.703125)
		pdf.setLineWidth(3)#ancho de la linea
		pdf.roundRect(15,490+10,390,80,10,stroke = 1, fill=0)
		pdf.setStrokeColorRGB(0.6171875,0.79296875,0.703125)
		pdf.setLineWidth(1)
		pdf.roundRect(20,495+10,380,70,8,stroke = 1, fill=0)
		pdf.drawCentredString(230,550,f"{self.fecha}")
		pdf.drawCentredString(230,530,"LISTA DE PRECIOS FARFALLA")
		pdf.setFont("Helvetica", 8)
		pdf.drawCentredString(230,515,"*Precio y stock sujeto a modificaciones sin previo aviso.")
		
	#Detalle
	def detalle_lista_pdf(self,pdf, detalle,n):
		#Tabla con detalle de pedido
		width, height = A5	
		cabecera=[
			['Producto','En stock', 'P. Unit.'],
			]
		
		pedido=Table(cabecera+detalle, colWidths=[280,50,60],rowHeights=30)
		pedido.setStyle(TableStyle([
	 		 	 		 ('LINEBEFORE', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones verticales
	 		 	 		 ('BOX', (0,0), (-1,-1), 3, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #recuadro del la tabla
	 		 	 		 ('LINEBELOW',(0,0), (-1,-1), 1,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones horizontales
					 ('LINEBELOW',(0,0), (-1,0), 2,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)) #division entre cabecera y detalle
	 		 	 			 ]))

		pedido.wrapOn(pdf, width, height)
		w,h=pedido.wrap(0,0)
		pedido.drawOn(pdf, 15,height-(465-(30*(11-len(detalle)))))   

#Productos
	def boton_precio_venta(self):
		proveedor=self.proveedor.get()
		costo=float(self.costo.get())
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute(""" SELECT id FROM proveedores WHERE proveedor LIKE ? """,[proveedor])
		id_proveedor=cursor.fetchall()
		cursor.execute(""" SELECT porcentaje,redondeo FROM precio_venta WHERE id_proveedor LIKE ? """,id_proveedor[0])
		datos=cursor.fetchone()
		if datos!=None:
			redondeo=float(datos[1])
			porcentaje=float(datos[0])
			precio_venta=self.calculo_venta(costo,redondeo,porcentaje)
			self.precio_venta.set(precio_venta)
		else:
			messagebox.showerror('Sin datos','No se configuraron datos para calcular precio de venta')

#Compras
	#Configuracion para escribir fecha
	def escribaFecha(self,event=None):
		numeros=len(self.fechaentry.get())
		if numeros == 8 and str(self.fechaentry.get()).count('/')==0:
			self.fechaentry.insert(2,"/")
			self.fechaentry.insert(5,"/")
		elif len(self.fechaentry.get())==10 and str(self.fechaentry.get())[2]=='/'and str(self.fechaentry.get())[5]=='/':
			self.e1.focus()
		else:
			messagebox.showerror('Error', 'Formato de fecha dd/mm/aaaa')
			self.fechacte.set('')
			self.fechaentry.focus()

	#Suma sub-totales tabla Compras
	def suma_subtotales(self):
		total = 0.0
		for pretotal in self.tablaCompras.get_children():
			total += float(self.tablaCompras.item(pretotal, "values")[6])
		self.subtotal.set(round(total,2))

	#Porcentaje de descuento y total
	def descuento_compra(self,event=None):
		descueto=0.0
		porcentaje=float(self.porcentaje_descuento.get())
		sub_total=float(self.entry_subtotal.get())
		desc=sub_total*(porcentaje*0.01)
		descuento=round(desc,2)
		self.descuento.set(float(descuento))
		
	def sumaTotales(self,event=None):
		total=0.0
		sub=float(self.entry_subtotal.get())
		desc=float(self.descuento.get())
		total=round((sub-desc),2)
		self.total_compra.set(total)

#Presupuesto
	#Suma sub-totales tabla Presupuesto
	def suma_subtotales_presupuesto(self):
		try:
			total = 0.0
			for pretotal in self.tablaPresupuesto.get_children():
				total += float(self.tablaPresupuesto.item(pretotal, "values")[4])
			self.subtotal.set(round(total,2))
		except TclError:
			pass

	#Porcentaje de descuento y total Presupuesto
	def descuento_presupuesto(self,event=None):
		try:
			descueto=0
			porcentaje=float(self.porcentaje_descuento.get())
			sub_total=float(self.entry_subtotal.get())
			desc=sub_total*(porcentaje*0.01)
			descuento=round(desc,2)
			self.descuento.set(float(descuento))
		except TclError:
			pass
		
	def sumaTotales_presupuesto(self,event=None):
		try:
			total=0.0
			sub=float(self.entry_subtotal.get())
			desc=float(self.descuento.get())
			envio=float(self.envio.get())
			total=round((sub-desc+envio),2)
			self.total_presupuesto.set(total)
		except TclError:
			pass

	def boton_envio (self, event=None,):
		try:
			if self.con_envio.get()==1:
				self.envio.set('')
				self.envio_entry.config(state='normal')
				self.envio_entry.focus()
				self.sumaTotales_presupuesto()
			else:
				self.envio.set('0.0')
				self.envio_entry.config(state='readonly')
				self.sumaTotales_presupuesto()
		except TclError:
			pass

	def enviobd(self):
		if self.con_envio.get()==1:
			envio='Con envio'
		else:
			envio='Sin envio'
		return envio

#PDF Presupuesto
	#Archivo
	def pdf_presupuesto(self):
		#Id para nombre del archivo
		conexion=self.conectar()
		cursor=conexion.cursor()
		
		#Nombre del archivo
		nombre=self.nombre_pdf_presupuesto()
   		
		#Creación de archivo
		pdf= canvas.Canvas(f"PDF's\Presupuestos\{nombre}.pdf",pagesize=A5)#tamaño A5 = 420x595px
		
		styles = getSampleStyleSheet() 
		detalle=[]
		for i in self.tablaPresupuesto.get_children():
			detalle.append(self.tablaPresupuesto.item([i], "values"))
		detalle=list(map(list, detalle))
		
		E1=[]
		for i in detalle:
			E1.append([(Paragraph(i[1], styles["BodyText"]))])
		for i in range(0,len(detalle)):
			detalle[i][1]=E1[i]
			i+=1
		
		#Generación de lista de PDF

		min=0 #inicio de la lista
		max=11 #final de la lista
		c=11 #Elementos por lista
		div=(len(detalle)//c) #Cantidad de listas
		r=0 #Repetición del bucle
		s=(len(detalle)%c) #Elementos libres

		while len(detalle)%c!=0 and len(detalle)>=c:
			self.encabezado_presupuesto(pdf)
			self.detalle_presupuesto_pdf(pdf, detalle[min:max],len(detalle))
			min+=c
			max+=c
			r+=1
			self.total_pdf_presupuesto(pdf)
			self.transferencia_pdf(pdf)
			self.validez(pdf)
			pdf.showPage()
			if r==div:
				self.encabezado_presupuesto(pdf)
				self.detalle_presupuesto_pdf(pdf, detalle[min:min+s],len(detalle))
				self.total_pdf_presupuesto(pdf)
				self.transferencia_pdf(pdf)
				self.validez(pdf)
				break
			
		while len(detalle)%c==0 :
			self.encabezado_presupuesto(pdf)
			self.detalle_presupuesto_pdf(pdf, detalle[min:max],len(detalle))
			min+=c
			max+=c
			r+=1
			self.total_pdf_presupuesto(pdf)
			self.transferencia_pdf(pdf)
			self.validez(pdf)
			pdf.showPage()
			if r==div:
				break
			
		if len(detalle)<c:
			self.encabezado_presupuesto(pdf)
			self.detalle_presupuesto_pdf(pdf, detalle[min:min+s],len(detalle))
			self.total_pdf_presupuesto(pdf)
			self.transferencia_pdf(pdf)
			self.validez(pdf)

		pdf.save()

		archivo=messagebox.askokcancel('Abrir', '¿Desea abrir el archivo pdf?')
		if archivo==True:
			os.system(f"{self.ubicacion()}\PDF's\Presupuestos\{nombre}.pdf")

	#Encabezado
	def encabezado_presupuesto(self,pdf):
		pdf.drawImage("pdf_logo.png",30 ,510,width=60, height=61, mask='auto')
		pdf.setStrokeColorRGB(0.6171875,0.79296875,0.703125)
		pdf.setLineWidth(3)#ancho de la linea
		pdf.roundRect(15,490+10,390,80,10,stroke = 1, fill=0)
		pdf.setStrokeColorRGB(0.6171875,0.79296875,0.703125)
		pdf.setLineWidth(1)
		pdf.roundRect(20,495+10,380,70,8,stroke = 1, fill=0)
		pdf.drawCentredString(230,545+10,f"{self.fecha}")
		pdf.drawCentredString(230,525+10,"PRESUPUESTO")
		pdf.drawCentredString(230,505+10,f"{self.cliente.get()}")
	
	#Detalle
	def detalle_presupuesto_pdf(self,pdf, detalle,n):
		#Tabla con detalle de presupuesto
		width, height = A5	
		cabecera=[
			['ID','Producto','Cant', 'P. Unit.', 'Importe'],
			]
		
		presupuesto=Table(cabecera+detalle, colWidths=[30,250,30,40,40],rowHeights=30)
		presupuesto.setStyle(TableStyle([
	 		 	 		 ('LINEBEFORE', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones verticales
	 		 	 		 ('BOX', (0,0), (-1,-1), 3, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #recuadro del la tabla
	 		 	 		 ('LINEBELOW',(0,0), (-1,-1), 1,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones horizontales
					 ('LINEBELOW',(0,0), (-1,0), 2,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)) #division entre cabecera y detalle
	 		 	 			 ]))

		presupuesto.wrapOn(pdf, width, height)
		w,h=presupuesto.wrap(0,0)
		presupuesto.drawOn(pdf, 15,height-(465-(30*(11-len(detalle)))))   
				
		
	#totales 
	def total_pdf_presupuesto(self,pdf):
		width, height = A5	
		#Total
		pretotal=[['Subtotal',f'{self.subtotal.get()}']]
		descuento=[['Desc.',f'{self.descuento.get()}']]
		envio=[['Envío',f'{self.envio.get()}']]
		final=[['Total',f'{self.total_presupuesto.get()}']]
		total=Table(pretotal+descuento+envio+final, colWidths=[50,50])
		total.setStyle(TableStyle([
	 	 	 		 ('LINEBEFORE', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)),
	 	 	 		 ('BOX', (0,0), (-1,-1), 3, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)),
	 	 	 			]))

		total.wrapOn(pdf, width, height)
		w,h=total.wrap(0,0)
		total.drawOn(pdf, width-115,height-545)

	#Datos de transferencia	
	def transferencia_pdf(self,pdf):
		#Transferencia
		width, height = A5	
		conexion=self.conectar()
		cursor=conexion.cursor()
		titular=[self.titular.get()]
		cursor.execute("SELECT * FROM cuenta_bancaria WHERE titular=(?)", titular)
		datos=cursor.fetchall()
		cuadro=[]
		for e in datos:
			cuadro.append(list(e))
		cbu=[['CBU',f'{cuadro[0][1]}']]
		alias=[['Alias',f'{cuadro[0][2]}']]
		titular=[['Titular',f'{cuadro[0][3]}']]
		dni=[['DNI',f'{cuadro[0][4]}']]
		id_tribut=[['Id. Tributaria',f'{cuadro[0][5]}']]
		cuenta=[['Tipo de cuenta',f'{cuadro[0][6]}']]

		transferencia=Table(cbu+alias+titular+dni+id_tribut+cuenta,colWidths=[75,210] )
		transferencia.setStyle(TableStyle([
	 		 	 		 ('LINEBEFORE', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)),
	 		 	 		 ('BOX', (0,0), (-1,-1), 3, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)),
	 		 	 			]))
					
		transferencia.wrapOn(pdf, width, height)
		w,h=transferencia.wrap(0,0)
		transferencia.drawOn(pdf,15,height-580)

	def validez(self,pdf):
		width, height = A5	
		estilos = getSampleStyleSheet()
		estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
		detalle=[]
		detalle.append([Paragraph('Presupuesto válido por 10 días.', estilos["Justify"])])
		
		validez=Table(detalle,colWidths=100 ,rowHeights=30)
		validez.setStyle(TableStyle([
	 		 	 		 ('BOX', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)),
	 		 	 			]))
					
		validez.wrapOn(pdf, width, height)
		w,h=validez.wrap(0,0)
		validez.drawOn(pdf,305,15)

#Nombre presupuesto
	def nombre_pdf_presupuesto(self):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT * FROM presupuestos ORDER BY id DESC LIMIT 1")
		id_presupuesto=[]
		for i in cursor.fetchall():
			id_presupuesto.append(i[0])			
		conexion.commit()
		id_presupuesto=id_presupuesto[0]

		#Reemplazo de item no soportados por el encode
		nombre=str(f'N° {id_presupuesto} - {self.cliente.get()}')
		cambios={' ':'_','-':'','°':'','Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'nh','Ñ':'Nh' }
		for a,b in cambios.items():
			nombre=nombre.replace(a, b)
		return nombre

#Mail con presupuesto
	def mail_presupuesto(self, evento=None):
	#Datos del mail
		conexion=self.conectar()
		cursor=conexion.cursor()
		usuario=[]
		contrasenha =[]
		destinatario=[]
		asunto='Presupuesto Farfalla'
		cursor.execute("SELECT * FROM master_mails WHERE estado='Activo'")
		admin=cursor.fetchall()
		for e in admin:
			usuario.append(e[1])
			contrasenha.append(e[2])
		conexion.commit()
		cliente=str(self.cliente.get())
		cursor.execute("SELECT correo FROM clientes WHERE cliente=(?)",[cliente] )
		destinatario=cursor.fetchall()[0]
		
		cuerpo=[]
		try:
			cursor.execute('SELECT cuerpo FROM opciones_mail WHERE opcion="Presupuestos" ')
			cuerpo.append(cursor.fetchone()[0])
			cuerpo=str(cuerpo[0].replace('\n','<br>\n\t\t'))
		except TypeError:
			messagebox.showinfo('Presupuestos','El cuerpo de mail no está configurado. Se enviará vacio.')
		

		if destinatario==None or destinatario== '':
			messagebox.showinfo('Sin mail', 'El cliente seleccionado no posee mail configurado')
		
		else:
			#Contenido del mail
			mensaje=MIMEMultipart('alternative') #Formato standar
			mensaje['Subject']=asunto #Asunto
			mensaje['From']=str(usuario[0]) #Desde que mail se manda
			mensaje['To']=str(destinatario[0]) # A quien se lo envia

			html=f"{cuerpo}".format(cliente)

			#Formato html al mensaje
			parte_html=MIMEText(html, 'html')

			#Agregar contenido del mensaje
			mensaje.attach(parte_html)

			#Archivo adjunto
			pdf=self.nombre_pdf_presupuesto()
			ruta=f"PDF's\Presupuestos\{pdf}.pdf"

			#asi se crea el archivo adjunto a enviar
			with open(ruta) as adjunto:
				contenido_adjunto=MIMEBase('application', 'octet-stream')
				contenido_adjunto.set_payload(adjunto.read())

			encoders.encode_base64(contenido_adjunto) #codificación del archivo
			nombre='Presupuesto Farfalla'
			contenido_adjunto.add_header(
				'Content-Disposition',
				f'attachment; filename={nombre}.pdf'
			)
			mensaje.attach(contenido_adjunto)
			mensaje_final=mensaje.as_string()

			#Conexión segura
			conexion=ssl.create_default_context()

			#Envio de mail
			with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=conexion) as server:
				server.login(str(usuario[0]),str(contrasenha[0]))
				server.sendmail(usuario,destinatario,mensaje_final)
			messagebox.showinfo('Correcto''El envío se realizó de forma exitosa')

#Pedido
	#Suma sub-totales tabla pedido
	def suma_subtotales_pedido(self):
		total = 0.0
		for pretotal in self.tablaPedido.get_children():
			total += float(self.tablaPedido.item(pretotal, "values")[4])
		self.subtotal.set(round(total,2))
		self.boton_recargo()
		

	#Porcentaje de descuento y total Presupuesto
	def descuento_pedido(self,event=None):
		try:
			descuento=0
			porcentaje=float(self.porcentaje_descuento.get())
			sub_total=float(self.entry_subtotal.get())
			desc=sub_total*(porcentaje*0.01)
			descuento=round(desc,2)
			self.descuento.set(float(descuento))
			self.boton_recargo()
		except TclError:
			pass
		
		
	def sumaTotales_pedido(self,event=None):
		try:
			total=0.0
			sub=float(self.entry_subtotal.get())
			desc=float(self.descuento.get())
			envio=float(self.envio.get())
			total=round((sub-desc+envio),2)
			self.total_pedido.set(total)
			self.boton_recargo()
		except TclError:
			pass

	def boton_recargo (self, event=None,):
		try:
			if self.pagos.get()== 'Tarjeta Débito':
				self.con_recargo.set(1)
				debito=float(self.debito.get())
				total=self.total_pedido.get()
				recargo=round(total*(debito*0.01),2)
				self.recargo.set(recargo)
			elif self.pagos.get()== 'Tarjeta Crédito':
				self.con_recargo.set(1)
				credito=float(self.credito.get())
				total=self.total_pedido.get()
				recargo=round(total*(credito*0.01),2)
				self.recargo.set(recargo)

			else:
				self.con_recargo.set(0)
				self.recargo.set('0.0')
		except TclError:
			pass
			
#PDF Pedido
	#Archivo 
	def pdf_pedido(self):
		#Id para nombre del archivo
		conexion=self.conectar()
		cursor=conexion.cursor()

		#Nombre del archivo
		nombre=self.nombre_pdf_pedido()
   		
		#Creación de archivo
		pdf= canvas.Canvas(f"PDF's\Pedidos\{nombre}.pdf",pagesize=A5)#tamaño A5 = 420x595px
		self.encabezado_pdf(pdf)

		styles = getSampleStyleSheet() 
		detalle=[]
		for i in self.tablaPedido.get_children():
			detalle.append(self.tablaPedido.item([i], "values"))
		detalle=list(map(list, detalle))
		E1=[]
		for i in detalle:
			E1.append([(Paragraph(i[1], styles["BodyText"]))])
		for i in range(0,len(detalle)):
			detalle[i][1]=E1[i]
			i+=1

		#Generación de lista de PDF

		min=0 #inicio de la lista
		max=12 #final de la lista
		c=12 #Elementos por lista
		div=(len(detalle)//c) #Cantidad de listas
		r=0 #Repetición del bucle
		s=(len(detalle)%c) #Elementos libres

		while len(detalle)%c!=0 and len(detalle)>=c:
			self.encabezado_pdf(pdf)
			self.detalle_pedido_pdf(pdf, detalle[min:max],len(detalle))
			min+=c
			max+=c
			r+=1
			self.total_pdf_pedido(pdf)
			self.gracias(pdf)
			pdf.showPage()
			if r==div:
				self.encabezado_pdf(pdf)
				self.detalle_pedido_pdf(pdf, detalle[min:min+s],len(detalle))
				self.total_pdf_pedido(pdf)
				self.gracias(pdf)
				break
			
		while len(detalle)%c==0 :
			self.encabezado_pdf(pdf)
			self.detalle_pedido_pdf(pdf, detalle[min:max],len(detalle))
			min+=c
			max+=c
			r+=1
			self.total_pdf_pedido(pdf)
			self.gracias(pdf)
			pdf.showPage()
			if r==div:
				break
			
		if len(detalle)<c:
			self.encabezado_pdf(pdf)
			self.detalle_pedido_pdf(pdf, detalle[min:min+s],len(detalle))
			self.total_pdf_pedido(pdf)
			self.gracias(pdf)
		pdf.save()

		archivo=messagebox.askokcancel('Abrir', '¿Desea abrir el archivo pdf?')
		if archivo==True:
			os.system(f"{self.ubicacion()}\PDF's\Pedidos\{nombre}.pdf")
		

	#Encabezado
	def encabezado_pdf(self,pdf):
		pdf.drawImage("pdf_logo.png",30 ,510,width=60, height=61, mask='auto')
		pdf.setStrokeColorRGB(0.6171875,0.79296875,0.703125)
		pdf.setLineWidth(3)#ancho de la linea
		pdf.roundRect(15,490+12,390,80,10,stroke = 1, fill=0)
		pdf.setStrokeColorRGB(0.6171875,0.79296875,0.703125)
		pdf.setLineWidth(1)
		pdf.roundRect(20,495+12,380,70,8,stroke = 1, fill=0)
		pdf.drawCentredString(230,545+12,f"{self.fecha}")
		pdf.drawCentredString(230,525+12,"PEDIDO")
		pdf.drawCentredString(230,505+12,f"{self.cliente.get()}")
	
	#Detalle
	def detalle_pedido_pdf(self,pdf, detalle,n):
		#Tabla con detalle de pedido
		width, height = A5	
		cabecera=[
			['ID','Producto','Cant', 'P. Unit.', 'Importe'],
			]
		
		pedido=Table(cabecera+detalle, colWidths=[30,250,30,40,40],rowHeights=30)
		pedido.setStyle(TableStyle([
	 		 	 		 ('LINEBEFORE', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones verticales
	 		 	 		 ('BOX', (0,0), (-1,-1), 3, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #recuadro del la tabla
	 		 	 		 ('LINEBELOW',(0,0), (-1,-1), 1,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)), #divisiones horizontales
					 ('LINEBELOW',(0,0), (-1,0), 2,colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)) #division entre cabecera y detalle
	 		 	 			 ]))

		pedido.wrapOn(pdf, width, height)
		w,h=pedido.wrap(0,0)
		pedido.drawOn(pdf, 15,height-(460-(30*(11-len(detalle)))))   
				
		
	#totales 
	def total_pdf_pedido(self,pdf):
		width, height = A5	
		#Total
		pretotal=[['Subtotal',f'{self.subtotal.get()}']]
		descuento=[['Desc.',f'{self.descuento.get()}']]
		envio=[['Envío',f'{self.envio.get()}']]
		recargo=[['Recargo',f'{self.recargo.get()}']]
		final=[['Total',f'{self.total_pedido.get()+self.recargo.get()}']]
		total=Table(pretotal+descuento+envio+recargo+final, colWidths=[50,50])
		total.setStyle(TableStyle([
	 	 	 		 ('LINEBEFORE', (0,0), (-1,-1), 2, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)),
	 	 	 		 ('BOX', (0,0), (-1,-1), 3, colors.Color(red=0.6171875,green=0.79296875,blue=0.703125)),
	 	 	 			]))

		total.wrapOn(pdf, width, height)
		w,h=total.wrap(0,0)
		total.drawOn(pdf, width-114,height-580)

	def gracias(self,pdf):
		texto = pdf.beginText(40,40)
		texto.setFont("Helvetica",10)
		texto.textLines('Le agradecemos su compra. Estamos a su dispocisión')
		pdf.drawText(texto)
		
#Mail con Pedido
	def mail_pedido(self, evento=None):
		#Datos del mail
		conexion=self.conectar()
		cursor=conexion.cursor()
		usuario=[]
		contrasenha =[]
		destinatario=[]
		asunto='Pedido Farfalla'
		cursor.execute("SELECT * FROM master_mails WHERE estado='Activo'")
		admin=cursor.fetchall()
		for e in admin:
			usuario.append(e[1])
			contrasenha.append(e[2])
		conexion.commit()
		cliente=str(self.cliente.get())
		cursor.execute("SELECT correo FROM clientes WHERE cliente LIKE ?",[cliente] )
		destinatario=cursor.fetchone()[0]
		
		cuerpo=[]
		cursor.execute('SELECT * FROM opciones_mail WHERE opcion="Pedidos" ')
		cuerpo.append(cursor.fetchall()[0][3])
		cuerpo=str(cuerpo[0].replace('\n','<br>\n\t\t'))

		if destinatario==None or destinatario== '':
			messagebox.showinfo('Sin mail', 'El cliente seleccionado no posee mail configurado')
		else:
			#Contenido del mail
			mensaje=MIMEMultipart('alternative') #Formato standar
			mensaje['Subject']=asunto #Asunto
			mensaje['From']=str(usuario[0]) #Desde que mail se manda
			mensaje['To']=str(destinatario) # A quien se lo envia

			html=f"{cuerpo}".format(cliente)

			#Formato html al mensaje
			parte_html=MIMEText(html, 'html')

			#Agregar contenido del mensaje
			mensaje.attach(parte_html)

			#Archivo adjunto
			pdf=self.nombre_pdf_pedido()
			ruta=f"PDF's\Pedidos\{pdf}.pdf"

			#asi se crea el archivo adjunto a enviar
			with open(ruta) as adjunto:
				contenido_adjunto=MIMEBase('application', 'octet-stream')
				contenido_adjunto.set_payload(adjunto.read())

			encoders.encode_base64(contenido_adjunto) #codificación del archivo
			nombre='Pedido Farfalla'
			contenido_adjunto.add_header(
				'Content-Disposition',
				f'attachment; filename={nombre}.pdf'
			)
			mensaje.attach(contenido_adjunto)
			mensaje_final=mensaje.as_string()

			#Conexión segura
			conexion=ssl.create_default_context()

			#Envio de mail
			with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=conexion) as server:
				server.login(str(usuario[0]),str(contrasenha[0]))
				server.sendmail(usuario,destinatario,mensaje_final)
			messagebox.showinfo('Mail', 'El mail se envio satisfactoriamente')

#Nombre pedido
	def nombre_pdf_pedido(self):
		conexion=self.conectar()
		cursor=conexion.cursor()
		cursor.execute("SELECT * FROM pedidos ORDER BY id DESC LIMIT 1")
		id_pedido=[]
		for i in cursor.fetchall():
			id_pedido.append(i[0])			
		conexion.commit()
		id_pedido=id_pedido[0]

		#Reemplazo de item no soportados por el encode
		nombre=str(f'N_{id_pedido}_{self.cliente.get()}')
		cambios={' ':'_','-':'','°':'','Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','á':'a','é':'e','í':'i','ó':'o','ú':'u','ñ':'nh','Ñ':'Nh' }
		for a,b in cambios.items():
			nombre=nombre.replace(a, b)
		return nombre

#Ventana envios de mail con adjuntos
	#Adjuntar archivo 
	def adjuntar_pdf(self, event=None):
		directorio=filedialog.askopenfilename(initialdir="PDF's",title='Seleccionar archivo',filetypes=[("PDF files","*.pdf"),('all files', '.*')])
		self.archivo.set(str(directorio))
		
	# Enviar mail
	def mail_personalizado(self, evento=None):
	#Datos del mail
		conexion=self.conectar()
		cursor=conexion.cursor()
		
		#Usuario y contraseña
		usuario=[]
		contrasenha =[]
		cursor.execute("SELECT * FROM master_mails WHERE estado='Activo'")
		admin=cursor.fetchall()
		for e in admin:
			usuario.append(e[1])
			contrasenha.append(e[2])
		conexion.commit()

		#Cliente
		cliente=self.cliente.get()

		#Mail destinatarios
		mails=self.direcion_mail.get(1.0, 'end')
		destinatario=mails.replace('\n','')
		
		#Asunto
		if self.opcion.get()==1:
			asunto="Presupuestos"
		elif self.opcion.get()==2:
			asunto="Pedidos" 
		elif self.opcion.get()==3:
			asunto="Listas de precios"
		else:
			asunto=self.otros.get()
			
		#Cuerpo
		cuerpo=[]
		if self.opcion.get()!=4:
			cuerpo=self.seleccion_para_enviar()
		else:
			cuerpo=self.seleccion_otros_para_enviar()
			
		#Construccion del envio de mail
		if destinatario==None or destinatario== '':
			messagebox.showinfo('Sin destinatario', 'Debe seleccionar un destinatario')
		elif asunto==None or asunto =='':
			messagebox.showinfo('Sin asunto', 'Debe seleccionar un asunto')
		else:
			#Contenido del mail
			mensaje=MIMEMultipart('alternative') #Formato standar
			mensaje['Subject']=asunto #Asunto
			mensaje['From']=str(usuario[0]) #Desde que mail se manda
			mensaje['CCO']=destinatario # A quien se lo envia
			
			html=f"{cuerpo}".format(cliente)
			
			#Formato html al mensaje
			parte_html=MIMEText(html, 'html')

			#Agregar contenido del mensaje
			mensaje.attach(parte_html)

			if self.archivo.get()==None or self.archivo.get()=='Archivo' or self.archivo.get()=='':
				mensaje_final=mensaje.as_string()

				#Conexión segura
				conexion=ssl.create_default_context()

				#Envio de mail
				with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=conexion) as server:
			 	   server.login(str(usuario[0]),str(contrasenha[0]))
			 	   server.sendmail(usuario,destinatario.split(','),mensaje_final)
				messagebox.showinfo('Correcto','El envío se realizó de forma exitosa')
			else:
			#Archivo adjunto
				ruta=self.archivo.get()

				#asi se crea el archivo adjunto a enviar
				with open(ruta) as adjunto:
					contenido_adjunto=MIMEBase('application', 'octet-stream')
					contenido_adjunto.set_payload(adjunto.read())

				encoders.encode_base64(contenido_adjunto) #codificación del archivo
				contenido_adjunto.add_header(
					'Content-Disposition',
					f'attachment; filename={asunto}.pdf'
				)
				mensaje.attach(contenido_adjunto)
				mensaje_final=mensaje.as_string()

				#Conexión segura
				conexion=ssl.create_default_context()

				#Envio de mail
				with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=conexion) as server:
					server.login(str(usuario[0]),str(contrasenha[0]))
					server.sendmail(usuario,destinatario.split(','),mensaje_final)
				messagebox.showinfo('Correcto','El envío se realizó de forma exitosa')

			
			#Limpiar pantalla
			self.archivo.set('Archivo')
			self.opcion.set(0)
			self.otros.set('')
			self.cliente.set('')
			self.direcion_mail.delete(1.0, 'end')

if __name__ == '__main__':
	inicio = Tk()
	app = Farfalla(inicio)
	inicio.mainloop()
	