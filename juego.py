#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine
from emisorHUMO import *
import os

pilas = pilasengine.iniciar(ancho=900, alto=550, titulo='TierraLuna')
contador_texto = 0
ruta = os.path.dirname(os.path.realpath(__file__))
url_fuente = ruta + '/Tentacles.ttf'

class Luna(pilasengine.actores.Actor):
	''' Este actor es para la presentación y para el final del juego '''

	def iniciar(self):
		url = ruta + '/imagenes/luna.jpg'
		self.imagen = url
		self.x = 0
		self.y = -700
		self.escala = 1.3
		self.z = -1

	def actualizar(self):
		self.rotacion -= 0.05


''' Esta escena es el juego propiamente. Es lo que comenzará cuando elijamos "iniciar juego" en el menú principal '''

class PantallaJuego(pilasengine.escenas.Escena):

	puntaje = pilas.actores.Puntaje(280, 200, color=pilas.colores.blanco, texto="0")
	choques = pilas.actores.Puntaje(600, 600, color=pilas.colores.blanco, texto="0") # uso 600,600 para que no se vea.
	velocidad_asteroides = 2


	class Asteroide(pilasengine.actores.Actor):

		def iniciar(self):

			self.imagen = ruta + '/imagenes/asteroide.png'
			self.escala = 0.3
			self.x = -500
			self.y = pilas.azar(-300, 300)
			self.giro = 1
			self.z = self.y

		def actualizar(self):
			self.rotacion += self.giro
			self.x += PantallaJuego.velocidad_asteroides
			# Elimina el objeto cuando sale de la pantalla.
			if self.x > 500:
				self.eliminar()
				PantallaJuego.puntaje.aumentar()

	#defino un grupo de enemigos
	enemigos = pilas.actores.Grupo()

	def crear_asteroide(self):
		#creo el actor enemigo
		asteroide = self.Asteroide(pilas);
		#creo un objeto para la física
		c1 = pilas.fisica.Circulo(asteroide.x, asteroide.y, 150, restitucion=1, amortiguacion=2)
		asteroide.imitar(c1)
		#lo agrego al grupo
		self.enemigos.agregar(asteroide)

	def iniciar(self):

		fondo = pilas.fondos.Galaxia(dx=-2, dy=0)
		# MUSICA
		url = ruta + '/data/Dreams-Become-Real.ogg'
		musica = pilas.sonidos.cargar(url)
		musica.reproducir(repetir=True)

		# Boton de sonido ON / OFF
		boton_musica = pilas.actores.Boton();
		url = ruta + '/imagenes/sonidoON.png'
		boton_musica.imagen = url
		boton_musica.x = 410
		boton_musica.y = 240
		boton_musica.z = -1000
		boton_musica.sonidoOnOff = True

		def cambio(sonidoOnOff):

			if boton_musica.sonidoOnOff:
				# apago la musica
				print "entro en true."
				musica.detener()
				url = ruta + '/imagenes/sonidoOFF.png'
				boton_musica.imagen = url
				boton_musica.sonidoOnOff = False
				print boton_musica.sonidoOnOff

			else:
				print "entro en false."
				#enciendo la música
				musica.reproducir(repetir=True)
				url = ruta + '/imagenes/sonidoON.png'
				boton_musica.imagen = url
				boton_musica.sonidoOnOff = True

		boton_musica.conectar_presionado(cambio, boton_musica.sonidoOnOff)

		# LOS TEXTOS
		#Le pido la biblioteca de textos contenido en textos.py
		from textos import textos

		texto_personalizado = pilas.actores.Texto('', magnitud=30, fuente= url_fuente, y= -230, ancho = 230)
		sombra_texto_personalizado = pilas.actores.Texto('', magnitud=30, fuente= url_fuente, y= -233, x=1, ancho = 230)

		sombra_texto_personalizado.color = pilas.colores.negro
		sombra_texto_personalizado.z = 4

		class Nave(pilasengine.actores.Actor):

			def iniciar(self):
				url = ruta + '/imagenes/lanave.png'
				self.imagen = url

		class Astronauta(pilasengine.actores.Actor):

			def iniciar(self):
				url = ruta + '/imagenes/astronauta.png'
				self.imagen = url

			def actualizar(self):
				self.rotacion += 1

		minave = Nave(pilas);
		minave.z = -2


		c2 = pilas.fisica.Circulo(minave.x, minave.y, 70, restitucion=0.1, amortiguacion=0.5)
		def seguir(evento):
			print "X: " + str(evento.x)
			print "Y: " + str(evento.y)
			if (evento.x < 390) or (evento.y < 219):
				# Solo sigo si el click es fuera del icono de sonido
				empujarx = (evento.x - c2.x) / 8
				empujary = (evento.y - c2.y) / 8
				c2.empujar(empujarx,empujary)

		def frenar():
			c2.velocidad_x /= 2
			c2.velocidad_y /= 2

		self.frenar = frenar
		pilas.tareas.siempre(0.1, self.frenar)


		self.seguir = seguir
		pilas.eventos.click_de_mouse.conectar(self.seguir)

		minave.imitar(c2, con_rotacion=False)

		emisor = EmisorHUMO(pilas, 0, 0)
		url = ruta + '/imagenes/humo.png'
		emisor.imagen_particula = pilas.imagenes.cargar_grilla(url)
		emisor.constante = True
		emisor.composicion = "blanco"
		emisor.duracion = 2
		emisor.frecuencia_creacion = 0.05
		emisor.vida = 3
		emisor.aceleracion_x_min = 36
		emisor.aceleracion_x_max = 50
		emisor.x_min = 171
		emisor.y_min = 2
		emisor.transparencia_min = 30
		emisor.transparencia_max = 50


		emisor.aprender(pilas.habilidades.Imitar, minave)

		minave.aprender(pilas.habilidades.MoverseConElTeclado)
		minave.aprender(pilas.habilidades.LimitadoABordesDePantalla)


		def imprimir_texto():

			global contador_texto

			if (contador_texto < len(textos)):

				#cambio el texto
				texto_personalizado.texto = textos[contador_texto]
				sombra_texto_personalizado.texto = textos[contador_texto]
				#oculto el texto y su sombra
				texto_personalizado.transparencia = 100
				sombra_texto_personalizado.transparencia = 100
				#lo hago visible nuevamente
				texto_personalizado.transparencia = [0]
				sombra_texto_personalizado.transparencia = [0]

				# Centro los textos en la pantalla
				texto_personalizado.ancho = 900
				sombra_texto_personalizado.ancho = 900
				factor = texto_personalizado.imagen.obtener_area_de_texto(texto_personalizado.texto)[0] + 4
				texto_personalizado.x = 450 - factor
				sombra_texto_personalizado.x = 451 - factor


				contador_texto += 1 # incremento el contador para que la próxima vez muestre el siguiente texto.
			else:
				# si no quedan textos que mostar, no muestro nada.
				texto_personalizado.texto = ''
				sombra_texto_personalizado.texto = ''


		# Creo una tarea para que aparezcan los textos, cada 5 segundos.
		pilas.tareas.siempre(5, imprimir_texto)



		def nave_choco():#Cuando un asteroide choca nave

			pilas.camara.vibrar(3, 0.5)
			self.choques.aumentar()
			if self.choques.obtener() == 3:
				minave.imagen = ruta + '/imagenes/lanave_01.png'
				emisor.frecuencia_creacion = 0.07
			if self.choques.obtener() == 6:
				minave.imagen = ruta + '/imagenes/lanave_02.png'
				emisor.frecuencia_creacion = 0.10
			if self.choques.obtener() == 8:
				minave.imagen = ruta + '/imagenes/lanave_03.png'
				emisor.frecuencia_creacion = 0.13
			if self.choques.obtener() == 10:
				minave.imagen = ruta + '/imagenes/lanave_04.png'
				emisor.eliminar()
				minave.rotacion = [360], 2
			if self.choques.obtener() == 11:
				pilas.camara.x = minave.x
				pilas.camara.y = minave.y
				perdido = Astronauta(pilas);
				minave.eliminar()
				#musica.detener()
				pilas.camara.escala = [1.2, 1.5, 1]
				perdido.escala = [1, 0.4]
				self.puntaje.eliminar()


		# Creo un control de coliciones para saber cuando perdes
		pilas.colisiones.agregar(minave, self.enemigos, nave_choco)

		#Elimino los límites laterales y la gravedad
		pilas.fisica.gravedad_x = 0
		pilas.fisica.gravedad_y = 0
		pilas.fisica.eliminar_paredes()
		pilas.fisica.eliminar_techo()
		pilas.fisica.eliminar_suelo()


	flag = [False, False, False, False, False] # esta bandera es para crear la tarea una sola vez


	def actualizar(self):
		''' Acá definimos las distintas etapas del juego, según van avanzando los textos
		    podemos ir cambiando los enemigos, el fondo, etc.  '''
		global contador_texto

		def cambio_nivel(nivel, leyenda):# Cuando pasamos de nivel

			pilas.camara.vibrar(4, 1)
			texto_nivel = pilas.actores.Texto(cadena_de_texto="Nivel " + str(nivel) + ": " + leyenda,
			 magnitud = 40, x = -100, y = -200)
			texto_nivel.transparencia = 0
			texto_nivel.transparencia = [100],5

		if contador_texto == 1:
			''' Recien al segundo texto comienzan a venir los asteroides '''
			# Creo una tarea para que aparezca un asteroide cada 2 segundos.
			if (self.flag[0]) == False:
				print "NIVEL 1"
				PantallaJuego.tarea1 = pilas.tareas.siempre(2, self.crear_asteroide)
				self.flag[0] = True
				cambio_nivel(1, "Cinco puntos de luz")

		if contador_texto == 34:
			''' ###  NIVEL 2 ###
			Llegamos al segundo nivel.  Aumentamos la velocidad de los enemigos y cambiamos el fondo. '''
			# Creo una tarea para que aparezca un asteroide cada 2 segundos.
			if (self.flag[1]) == False:
				print "NIVEL 2"
				PantallaJuego.tarea1.terminar()
				tarea2 = pilas.tareas.siempre(1, self.crear_asteroide)
				PantallaJuego.velocidad_asteroides = 6
				fondo = pilas.fondos.Galaxia(dx=-3, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_02.png'
				cambio_nivel(2, "Constelaciones")
				self.flag[1] = True

		if contador_texto == 63: #63
			''' ###  NIVEL 3 ### '''
			if (self.flag[2]) == False:
				print "NIVEL 3"
				PantallaJuego.velocidad_asteroides = 4
				fondo = pilas.fondos.Galaxia(dx=-2, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_03.png'
				cambio_nivel(3, "leyenda 3")
				self.flag[2] = True
		if contador_texto == 102:
			''' ###  NIVEL 4 ### '''
			if (self.flag[3]) == False:
				PantallaJuego.velocidad_asteroides = 2
				fondo = pilas.fondos.Galaxia(dx=-1, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_04.png'
				cambio_nivel(4, "leyenda 4")
				self.flag[3] = True
		if contador_texto == 240:
			''' ###  NIVEL 5 ### '''
			if (self.flag[4]) == False:
				PantallaJuego.velocidad_asteroides = 6
				fondo = pilas.fondos.Galaxia(dx=-3, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_05.png'
				cambio_nivel(5, "La llegada")
				self.flag[4] = True


# Escena Menu
def cargar_escena_juego():
	pilas.escenas.PantallaJuego()

def salir_del_juego():
	pilas.terminar()

class PantallaMenu(pilasengine.escenas.Escena):

	def iniciar(self):
		fondo = pilas.fondos.Color(pilas.colores.negro)
		fondo = pilas.fondos.Fondo()
		url = ruta + '/imagenes/intro.png'
		fondo.imagen = pilas.imagenes.cargar(url)
		fondo.z = -2

		luna = Luna(pilas);

		menu = pilas.actores.Menu([
					('iniciar juego', cargar_escena_juego),
					('salir', salir_del_juego),
				], fuente = url_fuente, y=0)
		menu.escala = 3
		menu.escala = [1]

pilas.escenas.vincular(PantallaJuego)
pilas.escenas.vincular(PantallaMenu)
pilas.escenas.PantallaMenu()

pilas.ejecutar()
