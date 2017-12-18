#!/usr/bin/env python
# -*- coding: utf-8

import pilasengine
import os

# Definimos la ruta hasta los archivos de las dos tipografías que utilizaremos en el juego. 

ruta = os.path.dirname(os.path.realpath(__file__))
url_fuente = ruta + '/Tentacles.ttf'
url_fuente2 = ruta + '/Oswald-Regular.ttf'


# Escena Menu de Tierra-Luna

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


#def cargar_escena_juego():
#	self.pilas.escenas.PantallaJuego()

#def cargar_escena_config():
#	self.pilas.escenas.PantallaConfig()

#def salir_del_juego():
#	self.pilas.terminar()


class PantallaMenu(pilasengine.escenas.Escena):
	def iniciar(self):
		fondo = self.pilas.fondos.Color(self.pilas.colores.negro)
		fondo = self.pilas.fondos.Fondo()
		url = ruta + '/imagenes/intro.png'
		fondo.imagen = self.pilas.imagenes.cargar(url)
		fondo.z = -2

		luna = Luna(self.pilas);

		menu = self.pilas.actores.Menu([
					('JUGAR', self.pilas.escenas.PantallaJuego),
					(u'CONFIG', self.pilas.escenas.PantallaConfig),
					('SALIR', self.pilas.terminar()),
				], fuente = url_fuente2, y = 150)
		menu.escala = 1
		menu.x = [300],3
		menu.transparencia = 100
		menu.transparencia = [0],3

