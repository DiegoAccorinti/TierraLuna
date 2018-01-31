#!/usr/bin/env python
# -*- coding: utf-8

import pilasengine
from temas_dic import temas # Importa diccionario con datos sobre los temas disponibles.
from globales import *
# Para que funcionen mis propias clases de interfaz modificadas
# hay que cargarlas explicitamente primero.
from pilasengine.interfaz import selector 
from pilasengine.interfaz import lista_seleccion
from pilasengine.interfaz import boton
from pilasengine import colores

#Clase especial de selector para poder ponerle el texto en blanco
class MiSelector(pilasengine.interfaz.selector.Selector):
	def _cargar_imagenes(self):
		self.imagen_selector = self.pilas.imagenes.cargar(ruta + "/imagenes/selector-deseleccionado.png")
		self.imagen_selector_seleccionado = self.pilas.imagenes.cargar(ruta + "/imagenes/selector-seleccionado.png")
	def pintar_texto(self):
		self.imagen.texto(self.texto, 35, 2, magnitud=12, fuente=url_fuente2, color= self.pilas.colores.Color(119,255,92))
	
class MiListaSeleccion(pilasengine.interfaz.lista_seleccion.ListaSeleccion):
	def _pintar_opciones(self, opcion_debajo_del_cursor=None):
		self.imagen.pintar(self.pilas.colores.Color(5,5,5)) # Fondo Oscuro

		if self.opcion_seleccionada != None:
			self.imagen.rectangulo(0, self.opcion_seleccionada * (self.alto_opcion + (self.separacion_entre_opciones * 2)), self.imagen.ancho(), self.alto_opcion + (self.separacion_entre_opciones * 2), relleno=True, color=self.pilas.colores.Color(0,63,0))

		if opcion_debajo_del_cursor != None:
			self.imagen.rectangulo(0, opcion_debajo_del_cursor * (self.alto_opcion + (self.separacion_entre_opciones * 2)), self.imagen.ancho(), self.alto_opcion + (self.separacion_entre_opciones * 2), relleno=True, color=self.pilas.colores.Color(0,20,0))

		for indice, opcion in enumerate(self.opciones):
			self.imagen.texto(opcion, 15, y=self.alto_opcion * indice + 1 +(self.separacion_entre_opciones * 2 * indice), magnitud=12, fuente=url_fuente2, color=self.pilas.colores.Color(119,255,92))

	def dibujar_recuadro(self):
		#recuadro_img = self.pilas.imagenes.cargar(ruta + "/imagenes/recuadro-lista.png")
		#print "La lista tiene ancho=", self.imagen.ancho()
		#print "La lista tiene altura=", self.imagen.alto()
		#print "La lista esta en: ", self.x, self.y
		
		ancho_lista = self.imagen.ancho() + 2
		alto_lista = self.imagen.alto() + 2
		
		#print "Area de ", ancho_lista, alto_lista
		area = self.pilas.imagenes.cargar_superficie(ancho_lista , alto_lista )
		area.rectangulo (0, 0, ancho_lista - 1, alto_lista -1, color = self.pilas.colores.Color(119, 255, 92), relleno = False, grosor = 1)
	
		self.recuadro = self.pilas.actores.Actor(imagen = area)
		self.recuadro.x = self.x 
		self.recuadro.y = self.y 
		
		
			
class MiBoton(pilasengine.interfaz.boton.Boton):
	def _crear_imagenes_de_botones(self):
		"Genera las 3 imagenes de los botones."
		ancho, alto = (10, 3)
		#tema = self.pilas.imagenes.cargar("boton/tema.png")

		self.imagen_normal = self.pilas.imagenes.cargar(ruta + "/imagenes/volver.png")
		self.imagen_sobre =  self.pilas.imagenes.cargar(ruta + "/imagenes/volver-resaltado.png")
		self.imagen_click =  self.pilas.imagenes.cargar(ruta + "/imagenes/volver-presionado.png")

		self.imagen = self.imagen_normal

		
		
class ConfigHud(pilasengine.actores.Actor):
	def iniciar(self):
		self.imagen = ruta + '/imagenes/hud-configuracion.png'
		self.transparencia = 40
		self.x = 0
		self.y = 0
	
				       
class PantallaConfig(pilasengine.escenas.Escena):
	
	mostre_huevo_pascua = False

	def presionar_boton(self):
		self.pilas.escenas.PantallaMenu(self.tema_actual, self.tema_sprites, self.tema_fondos, self.tema_textos)

	def iniciar(self, tema_actual, tema_sprites, tema_fondos, tema_textos):
		#Parametros que se le pasan al cargar
		self.tema_sprites = tema_sprites 
		self.tema_fondo = tema_fondos
		self.tema_textos = tema_textos 
		self.tema_actual = tema_actual 
		
		self.temas = temas
		
		fondo = self.pilas.fondos.Galaxia(dx=0, dy=0)
		fondo.imagen = ruta + '/imagenes/fondo-config.png'
		
		hud = ConfigHud(self.pilas)
		
		volver = MiBoton(self.pilas, "Volver")
		volver.x = -300
		volver.y = 0
		volver.escala = 0.3
		volver.conectar(self.presionar_boton)
		volver.texto = "Volver"
		
		PantallaConfig.ConfiguracionTemas(self)
		
		self.pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)
		
	def IniciarEstadosCheckbox(self):
		self.estados = []
		for v in self.temas.values():
			self.estados.append(v[:])  # v[:] crea una nueva lista sin referenciar a la original
		
		
	def IniciarFlagsCheckbox(self, nombre):
		'''
		Lee los valores de los flags del diccionario de temas.py
		'''
		flags = []
		tema = nombre
		flags = [ self.temas[tema][1], self.temas[tema][2], self.temas[tema][3] ]
		return flags
		
	def BuscarEstadosCheckbox(self, nombre_tema):
		estados = []
		for e in self.estados:
			if e[0] == nombre_tema:
				estados = [e[1], e[2], e[3]]
		return estados	

	def ToggleSprites(self, estado):
		for e in self.estados:
			if self.BuscarOpcionEnDic(e[0]) == self.tema_actual:
				e[1] = estado

	def ToggleFondos(self, estado):
		for e in self.estados:
			if self.BuscarOpcionEnDic(e[0]) == self.tema_actual:
				e[2] = estado

	def ToggleTextos(self, estado):
		for e in self.estados:
			if self.BuscarOpcionEnDic(e[0]) == self.tema_actual:
				e[3] = estado

	def SetTema(self, tema_elegido):
		#Define el tema si está chequeada la opcion
		
		self.tema_actual = self.BuscarOpcionEnDic(tema_elegido)
		
		self.opcion = self.tema_actual
		
		#Leo los flags del tema elegido 
		self.flags = self.IniciarFlagsCheckbox(self.tema_actual) 
		
		if self.flags[0]:
			self.tema_sprites = '/temas/' + self.opcion + '/sprites'

		if self.flags[1]:
			self.tema_fondos = '/temas/' + self.opcion + '/fondos'

		if self.flags[2]:
			self.tema_textos = '/temas/' + self.opcion
	
		
		e = self.BuscarEstadosCheckbox(tema_elegido)
		
		#self.InfoStatus(self.flags, e) # Imprime estado actual de selecciones.
		
		self.DibujarCheckboxes(self.flags, e) #Redibuja checkboxes de acuerdo a eleccion de nuevo tema
		#self.texto_personalizado3.texto = self.temas[self.tema_actual][4]
		self.descripcion_tema.eliminar()
		self.descripcion_tema = self.pilas.actores.Texto(self.temas[self.tema_actual][4], magnitud=12, fuente= url_fuente2, ancho=380, y= -200, x = 0)
		
		
	def BuscarOpcionEnDic(self, opcion):
		'''
		Devuelve el nombre del tema que debe usarse para la carpeta donde
		está guardado buscando por su nombre de fantasia
		
		Ej: Si opcion es = "Original", devuelve "original"
		'''
		
		
		for k, v in temas.items():
			if opcion == v[0]:
				nombre = k
		return nombre
		
	def DibujarCheckboxes(self, flags, estados):
		"""
		En el diccionario de temas, la Key es el nombre de carpeta del tema, 
		y Value es una lista de 4 elementos donde el elemento 0 es el nombre de fantasia del Tema, 
		el 1, 2 y 3 son flags para Sprites, Fondos y Textos
		si el valor es False no debe mostrarse el checkbox (independientemente de su estado)
		si el valor es True, debe mostrarse el checkbox y ademas debe ponerse como tildado inicialmente
		"""
		
		if flags[0]: # Flag para sprites
			self.selector_sprites.mostrar()
			if estados[0]:
				self.selector_sprites.seleccionar()
			else:
				self.selector_sprites.deseleccionar()
		else:
			self.selector_sprites.ocultar()
			
		if flags[1]: # Flag para fondos
			self.selector_fondos.mostrar()
			if estados[1]:
				self.selector_fondos.seleccionar()
			else:
				self.selector_fondos.deseleccionar()
		else:
			self.selector_fondos.ocultar()
		
		if flags[2]: # Flag para textos
			self.selector_textos.mostrar()
			if estados[2]:
				self.selector_textos.seleccionar()
			else:
				self.selector_textos.deseleccionar()
		else:
			self.selector_textos.ocultar()			
			
		#self.InfoStatus(flags, estados) # Imprime resultados para debug
	
	def InfoStatus(self, f, e):
		print "############### RESUMEN #################"
		print "El tema es", self.temas[self.tema_actual][0]
		print "Los estados de los checks son:", e[0], e[1], e[2]
		print "Las flags para Sprites, Fondos y Texto para el tema:", f[0], f[1], f[2]
		


	def SetOpcionElegida(self, opcion):
		'''
			Resalta en la lista de temas el tema actual elegido
		'''
		ndx = 0
		for t in self.Temas:
			if t == opcion:
				encontrado = ndx
			ndx += 1
		return(encontrado)
		
	def ConfiguracionTemas(self):
		#De cada tema se pueden cargar independientemente los fondos, la nave, los enemigos y los textos.
		
		combo_x = 195
		combo_y = 90
		
		#Estados iniciales para los checkboxes. Si la opcion está disponible, entonces se la pone a True.
		self.IniciarEstadosCheckbox()		
		self.flags = self.IniciarFlagsCheckbox(self.tema_actual)
		
		self.Temas = []
				
		for k, v in sorted(temas.items()):
			self.Temas.append(v[0]) # Toma el valor del nombre de fantasia de cada tema y lo agrega a una lista de opciones
		
		#Lista desplegable de temas
		self.selector_tema = MiListaSeleccion(self.pilas, self.Temas, self.SetTema)
		self.selector_tema.dibujar_recuadro() # Hay que reescribir esta funcion para que haga un recuadro adaptable
		#self.selector_tema.definir_centro((-self.selector_tema.x / 2, -self.selector_tema.y / 2))
		a = self.selector_tema.imagen.ancho()/2
		b = self.selector_tema.imagen.alto()/2
		self.selector_tema.x =  combo_x - 120 - a
		self.selector_tema.y =  combo_y + 12 - b
		
		self.selector_tema.recuadro.x = combo_x - 120 - a
		self.selector_tema.recuadro.y = combo_y + 12 - b
		#Fuerza la seleccion de la opcion que coincida con el tema actual
		self.selector_tema.opcion_seleccionada = self.SetOpcionElegida(self.temas[self.tema_actual][0]) # la seleccion es un numero entero empezando en 0
		
		
		
		#Labels
		
		self.etiqueta_tema = self.pilas.actores.Texto(cadena_de_texto="Elige Tema: ", fuente = url_fuente2, magnitud = 24, x = -120, y = 100)
		self.etiqueta_tema.color = self.pilas.colores.blanco
		
		#Checkboxes
		self.selector_sprites = MiSelector(self.pilas, "Sprites")
		self.selector_sprites.definir_accion(self.ToggleSprites)
		self.selector_sprites.x = combo_x
		self.selector_sprites.y = combo_y
				
		self.selector_fondos = MiSelector(self.pilas, "Fondos")
		self.selector_fondos.definir_accion(self.ToggleFondos)
		self.selector_fondos.x = combo_x
		self.selector_fondos.y = combo_y - 30
					
		self.selector_textos = MiSelector(self.pilas, "Textos")
		self.selector_textos.definir_accion(self.ToggleTextos)
		self.selector_textos.x = combo_x
		self.selector_textos.y = combo_y - 60
		
		e = self.BuscarEstadosCheckbox(self.temas[self.tema_actual][0])
		
		self.DibujarCheckboxes(self.flags, e)

		self.descripcion_tema = self.pilas.actores.Texto(self.temas[self.tema_actual][4], magnitud=12, fuente= url_fuente2, ancho=380, y= -200, x = 0)
	
	def al_pulsar_tecla(self, tecla):

		if tecla.codigo == 32:
			self.pilas.escenas.PantallaMenu(self.tema_actual, self.tema_sprites, self.tema_fondos, self.tema_textos)
		'''
		else:
			if (self.mostre_huevo_pascua == False):
			
				#texto_personalizado3 = self.pilas.actores.Texto(u'Un juego de Diego Accorinti para Huayra gnu/linux', magnitud=12, fuente= url_fuente2, y= -200, x = 0)
				self.mostre_huevo_pascua = True
		'''
