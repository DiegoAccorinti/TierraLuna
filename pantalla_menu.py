#!/usr/bin/env python
# -*- coding: utf-8

import pilasengine
from globales import *
from objetos import Luna


class PantallaMenu(pilasengine.escenas.Escena):
	# Escena Menu
	def cargar_escena_juego(self):
		self.pilas.escenas.PantallaJuego()

	def cargar_escena_config(self):
		self.pilas.escenas.PantallaConfig()

	def salir_del_juego(self):
		self.pilas.terminar()
	
	def iniciar(self):
		fondo = self.pilas.fondos.Color(self.pilas.colores.negro)
		fondo = self.pilas.fondos.Fondo()
		url = ruta + '/imagenes/intro.png'
		fondo.imagen = self.pilas.imagenes.cargar(url)
		fondo.z = -2

		luna = Luna(self.pilas);

		menu = self.pilas.actores.Menu([
					('JUGAR', self.cargar_escena_juego),
					(u'CONFIG', self.cargar_escena_config),
					('SALIR', self.salir_del_juego),
				], fuente = url_fuente2, y = 150)
		menu.escala = 1
		menu.x = [300],3
		menu.transparencia = 100
		menu.transparencia = [0],3

