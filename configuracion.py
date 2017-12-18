#!/usr/bin/env python
# -*- coding: utf-8

import pilasengine
import os

# Definimos la ruta hasta los archivos de las dos tipografías que utilizaremos en el juego. 

ruta = os.path.dirname(os.path.realpath(__file__))
url_fuente = ruta + '/Tentacles.ttf'
url_fuente2 = ruta + '/Oswald-Regular.ttf'

class PantallaConfig(pilasengine.escenas.Escena):

	mostre_huevo_pascua = False

	def iniciar(self):

		fondo = self.pilas.fondos.Galaxia(dx=0, dy=0)
		fondo.imagen = ruta + '/imagenes/fondo-config.png'
		texto_personalizado = self.pilas.actores.Texto(u'¡no hay nada que configurar!', magnitud=55, fuente= url_fuente,
		 y= 0, x = 0)
		texto_personalizado2 = self.pilas.actores.Texto(u'presione ESPACIO para continuar', magnitud=14, fuente= url_fuente2, y= -230, x = 0)
		texto_personalizado2.color =  self.pilas.colores.gris



		self.pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)

	def al_pulsar_tecla(self, tecla):

		if tecla.codigo == 32:
			self.pilas.escenas.PantallaMenu()
		else:
			if (self.mostre_huevo_pascua == False):
				texto_personalizado3 = pilas.actores.Texto(u'Un juego de Diego Accorinti para Huayra gnu/linux', magnitud=12, fuente= url_fuente2, y= -200, x = 0)
				self.mostre_huevo_pascua = True


