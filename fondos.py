#!/usr/bin/env python
# -*- coding: utf-8

import pilasengine
from globales import *

#def set_escala_y(self, s):
#    self.pilas.utils.interpretar_propiedad_numerica(self, 'escala_y', s)
#    self._escala_y = s

#get_escala_y = pilasengine.actores.Actor.obtener_escala_y
#pilasengine.actores.Actor.escala_y = property(get_escala_y, set_escala_y)

# El fondo puede incluir 3 capas de distinta velocidad para generar el efecto de paralaje
# las capas se indican con el parametro "tipo" que puede valer "frente", "medio" y "fondo"
class capa(pilasengine.actores.Actor):
	def iniciar(self, img, tipo, flip):
		self.tipo = tipo
		self.flip = flip
		self.imagen = ruta + '/imagenes/fondos/' + img
		self.escala_y = 1
		self.imagen.repetir_horizontal = True
		self.x = 250
		self.y = 10
		if self.tipo=="frente":
			self.velocidad = 3
			self.z = 50
		elif self.tipo=="medio":
			self.velocidad = 1
			self.z = 200
		elif self.tipo =="fondo":
			self.velocidad = 0.5
			self.z = 250
		if self.flip: # Uso una imagen para la mitad superior de la pantalla, la otra la inventamos
			self.escala_y = -self.escala_y
			self.y = -self.y
	def actualizar(self):
		self.x += self.velocidad #scroll lateral, cada capa se movera con la velocidad que le corresponda

