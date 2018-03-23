#!/usr/bin/env python
# -*- coding: utf-8

import pilasengine
from globales import *
from objetos import *

		''' Eventos únicos especiales durante el juego '''	
class evento_arsat2:
	def iniciar(self):
		# paso de ARSAT-2
		hudarsat = HUDArsat(self.pilas, tema=self.mitema[1])
		arsat = Arsat(self.pilas, tema=self.mitema[1])
		arsat.x = hudarsat.x
		arsat.y = hudarsat.y


class evento_estacion:
	def iniciar(self):
		# Crea una estacion de reparacion para reparar un poco la nave
		estacion_reparacion = Reparacion(self.pilas, tema=self.mitema[1]) 
		rep_colision = self.pilas.fisica.Circulo(estacion_reparacion.x, estacion_reparacion.y, 70, restitucion=0.1, amortiguacion=0.5)
		estacion_reparacion.imitar(rep_colision)
		self.pilas.colisiones.agregar(self.minave, estacion_reparacion, self.minave.choque_repara)
		
