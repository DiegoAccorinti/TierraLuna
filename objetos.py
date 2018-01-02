#!/usr/bin/env python
# -*- coding: utf-8


import pilasengine
from globales import *
from emisorHUMO import *


# Declaramos Luna. Este actor es utilizado en la presentación.
class Tierra(pilasengine.actores.Actor):
	def iniciar(self):
		url = ruta + '/imagenes/tierra.png'
		self.imagen = url
		self.x = 250
		self.y = 50
		self.escala = 1.3
		self.z = 80
	def actualizar(self):
		self.x += 0.1
		if self.x > 600:
			self.eliminar()		
			
class LunaFinal(pilasengine.actores.Actor):
	def iniciar(self):
		url = ruta + '/imagenes/luna_final.png'
		self.imagen = url
		self.x = -800
		self.y = 50
		self.escala = 1.3
		self.z = 80
		self.transparencia = 15
	def actualizar(self):
		self.x += 0.1
		if self.x > -400:
			self.x = -400 #deja fija la luna si llegó a la mitad de la pantalla
			
class Luna(pilasengine.actores.Actor):
	
	def iniciar(self):
		url = ruta + '/imagenes/luna.jpg'
		self.imagen = url
		self.x = 0
		self.y = -700
		self.escala = 1.3
		self.z = -1

	def actualizar(self):
		self.rotacion -= 0.05


class Arsat(pilasengine.actores.Actor):
	
	def iniciar(self):
		url = ruta + '/imagenes/ARSAT-2.png'
		self.imagen = url
		self.z = 20

	def actualizar(self):
		self.rotacion -= 0.06
		self.x += 0.6
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 600:
			self.eliminar()
		

			
class HUDArsat(pilasengine.actores.Actor):
	
	def iniciar(self):
		url = ruta + '/imagenes/ARSAT-2-HUD.png'
		self.imagen = url
		self.x = -600
		self.y = self.pilas.azar(-50, 150)
		self.escala = 1
		self.z = 21

	def actualizar(self):
		self.x += 0.6
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 600:
			self.eliminar()
		
class Nave(pilasengine.actores.Actor):

	def iniciar(self):
		url = ruta + '/imagenes/lanave.png'
		self.imagen = url
		self.z = -50
		self.choques = 0
		#Crea un objeto asociado que emite particulas
		self.emisor = EmisorHUMO(self.pilas, 0, 0)
		url = ruta + '/imagenes/humo.png'
		self.emisor.imagen_particula = self.pilas.imagenes.cargar_grilla(url)
		self.emisor.constante = True
		self.emisor.composicion = "blanco"
		self.emisor.duracion = 2
		self.emisor.frecuencia_creacion = 0.05
		self.emisor.vida = 3
		self.emisor.aceleracion_x_min = 36
		self.emisor.aceleracion_x_max = 50
		self.emisor.x_min = 171
		self.emisor.y_min = 2
		self.emisor.transparencia_min = 30
		self.emisor.transparencia_max = 50
		
		#self.nave_energia = self.pilas.actores.Energia(color_relleno = self.pilas.colores.verde)
		self.nave_energia = self.pilas.actores.Energia(progreso = 100, color_relleno = self.pilas.colores.Color(56,255,75),
	ancho=190, alto=20, con_sombra = False, con_brillo = False)
		self.nave_energia.x = 250
		self.nave_energia.y = 240
		self.nave_energia.z = 0
		
	def choque(self):
			self.pilas.camara.vibrar(3, 0.5)
			self.choques += 1
			self.valor = self.nave_energia.progreso - (100/11)
			self.nave_energia.progreso = [self.valor]
			if int(self.nave_energia.progreso) in range(20, 40):
				self.nave_energia.color_relleno = self.pilas.colores.Color(230,200,0) #amarillo
			elif self.nave_energia.progreso <= 20:
				self.nave_energia.color_relleno = self.pilas.colores.Color(230,49,0) # rojo 
			if self.choques == 2:
				self.imagen = ruta + '/imagenes/lanave_01.png'
				self.emisor.frecuencia_creacion = 0.07
			if self.choques == 4:
				self.imagen = ruta + '/imagenes/lanave_02.png'
				self.emisor.frecuencia_creacion = 0.10
			if self.choques == 7:
				self.imagen = ruta + '/imagenes/lanave_03.png'
				self.emisor.frecuencia_creacion = 0.13
			if self.choques == 9:
				self.imagen = ruta + '/imagenes/lanave_04.png'
				self.emisor.eliminar()
				self.rotacion = [360], 2
			if self.choques == 11:	
				self.nave_energia.progreso = [2]
			if self.choques == 12: # MUERE
				self.pilas.camara.x = self.x
				self.pilas.camara.y = self.y
				self.morir() #Llamar a astronauta flotando o coso.
				self.eliminar()
				
				

			mensajeNeo = [False, False]
			print "Choques = " + str(self.choques)
			if (self.choques == 8) and (mensajeNeo[0] == False):
				os.system('clear')
				print "Despierta, Neo."
				print "La Matrix te tiene."
				print "Sigue al conejo blanco."
				print "Toc toc, Neo."
				mensajeNeo[0] = True
			if (self.choques == 9) and (mensajeNeo[1] == False):
				os.system('clear')
				print "Choques = " + str(self.choques)
				mensajeNeo[1] = True
	def morir(self):
			self.perdido = Astronauta(self.pilas);
			self.pilas.camara.escala = [1.2, 1.5, 1]
			self.perdido.escala = [1, 0.4]
			self.texto_personalizado3 = self.pilas.actores.Texto(u'por miles de años flotarás exánime en el espacio · presiona ESPACIO', magnitud=18, fuente= url_fuente2, y= -230, x = 0)
			self.texto_personalizado3.color =  self.pilas.colores.blanco
			self.pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)		

	def al_pulsar_tecla(self, tecla):
			global flag
			if tecla.codigo == 32:
				flag = [False, False, False, False, False]
				self.pilas.escenas.PantallaMenu()

class Astronauta(pilasengine.actores.Actor):

	def iniciar(self):
		url = ruta + '/imagenes/astronauta.png'
		self.imagen = url

	def actualizar(self):
		self.rotacion += 1

class Asteroide(pilasengine.actores.Actor):

	def iniciar(self, tipo):
		self.tipo = tipo

		if self.tipo == "uno":
			self.imagen = ruta + '/imagenes/asteroide.png'
			self.giro = 1
			self.velocidad = 2
		if self.tipo == "dos":
			self.imagen = ruta + '/imagenes/asteroide2.png'
			self.giro = 3
			self.velocidad = 6

		if self.tipo == "tres":
			self.imagen = ruta + '/imagenes/asteroide3.png'
			self.giro = 2
			self.velocidad = 4
		if self.tipo == "cuatro":
			self.imagen = ruta + '/imagenes/asteroide4.png'
			self.giro = -2
			self.velocidad = 2
		if self.tipo == "cinco":
			self.imagen = ruta + '/imagenes/asteroide5.png'
			self.giro = 3
			self.velocidad = 6
		self.escala = 0.3
		self.x = -500
		self.y = self.pilas.azar(-300, 300)
		self.z = self.pilas.azar(-100, 10)

	def actualizar(self):
		self.rotacion += self.giro
		self.x += self.velocidad
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 500:
			self.eliminar()

class Reparacion(pilasengine.actores.Actor):

	def iniciar(self):
		url = ruta + '/imagenes/reparacion.png'
		self.imagen = url
		self.x = 100
		self.z = 0
		self.velocidad = 0.3
		self.delta_escala = 0.005
		self.escala = 0.3
		
	def actualizar(self):
		self.x += self.velocidad
		self.escala += self.delta_escala
		if self.escala > 0.4 or self.escala < 0.3:
			self.delta_escala = -self.delta_escala
			#deberia agrandar o achicar entre 0.6 y 1
