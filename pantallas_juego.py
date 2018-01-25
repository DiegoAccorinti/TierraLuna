#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine
from globales import *
from objetos import Luna

class PantallaFinal(pilasengine.escenas.Escena):
	def iniciar(self):
		fondo = self.pilas.fondos.Fondo()
		url = ruta + '/imagenes/final.jpg'
		fondo.imagen = self.pilas.imagenes.cargar(url)
		texto_personalizado = self.pilas.actores.Texto(u'¡ganaste!', magnitud=60, fuente= url_fuente,
		 y= -50, x = 20)
		self.pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)
	def al_pulsar_tecla(self, tecla):
			global flag
			if tecla.codigo == 32:
				flag = [False, False, False, False, False]
				self.pilas.escenas.PantallaMenu()


class PantallaMenu(pilasengine.escenas.Escena):
	# Escena Menu
	
	
	def cargar_escena_juego(self):
		self.pilas.escenas.PantallaJuego(self.tema_actual, self.tema_sprites, self.tema_fondos, self.tema_textos)

	def cargar_escena_config(self):
		self.pilas.escenas.PantallaConfig(self.tema_actual, self.tema_sprites, self.tema_fondos, self.tema_textos)

	def cargar_escena_demo(self):
		self.pilas.escenas.PantallaDemo(self.tema_actual, self.tema_sprites, self.tema_fondos, self.tema_textos)
		
	def salir_del_juego(self):
		self.pilas.terminar()
	
	def iniciar(self, tema_actual, tema_sprites, tema_fondos, tema_textos):
		
		self.tema_sprites = tema_sprites
		self.tema_fondos = tema_fondos
		self.tema_textos = tema_textos
		self.tema_actual = tema_actual 
		
		fondo = self.pilas.fondos.Color(self.pilas.colores.negro)
		fondo = self.pilas.fondos.Fondo()
		url = ruta + '/imagenes/intro.png'
		fondo.imagen = self.pilas.imagenes.cargar(url)
		fondo.z = -2

		luna = Luna(self.pilas);

		menu = self.pilas.actores.Menu([
					('JUGAR', self.cargar_escena_juego),
					('DEMO', self.cargar_escena_demo),
					(u'CONFIG', self.cargar_escena_config),
					('SALIR', self.salir_del_juego),
				], fuente = url_fuente2, y = 150)
		menu.escala = 1
		menu.x = [300],3
		menu.transparencia = 100
		menu.transparencia = [0],3

