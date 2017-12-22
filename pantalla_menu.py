#!/usr/bin/env python
# -*- coding: utf-8

import pilasengine
from globales import *
from objetos import Luna

# Escena Menu
#def cargar_escena_juego():
#	pilas.escenas.PantallaJuego()

#def cargar_escena_config():
#	pilas.escenas.PantallaConfig()

#def salir_del_juego():
#	pilas.terminar()


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

