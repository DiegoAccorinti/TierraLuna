#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine

from globales import *
from objetos import *
from fondos import *
# Pantallas adicionales
from pantallas_juego import *
from juego_tierraluna import *

from movimiento_de_nave import MovimientoDeNave

# Esta escena es una demo. Hereda los métodos de PantallaJuego y modifica el comportamiento de la nave
# Es lo que comenzará cuando elijamos "Demo" en el menú principal


class PantallaDemo(PantallaJuego):
	
	def iniciar_nave(self):
		self.minave = Nave(self.pilas, self.mitema, pilotoAutomatico = True);	

	def iniciar_colisiones(self):
		print "Modo Demo, colisiones desactivadas"
		
	def cargarTextos(self):
		''' Carga el archivo con la definicion de la aventura y lo guarda en una lista'''
		self.textos = []
		nombre_archivo = ruta + "/texto-demo.txt"
		archivo = codecs.open(nombre_archivo, "r", "utf8")


		self.textos = [line.rstrip('\n') for line in archivo]
			

	def actualizar(self):
		''' Acá definimos las distintas etapas del juego, según van avanzando los textos
		    podemos ir cambiando los enemigos, el fondo, etc.  '''
			
				
				
		''' Eventos únicos especiales durante el juego '''	


