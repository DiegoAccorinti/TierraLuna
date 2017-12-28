#!/usr/bin/env python
# -*- coding: utf-8


import pilasengine
from globales import *


# Declaramos Luna. Este actor es utilizado en la presentación.

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
		self.z = 30

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
		self.z = 20

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

