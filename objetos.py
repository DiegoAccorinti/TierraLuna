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
		self.z = -1

	def actualizar(self):
		self.x += 0.6
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 600:
			self.eliminar()
		

