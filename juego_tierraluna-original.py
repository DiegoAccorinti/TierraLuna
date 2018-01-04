#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine
from emisorHUMO import *
from globales import *
from objetos import *

# Esta escena es el juego propiamente. Es lo que comenzará cuando elijamos "iniciar juego" en el menú principal

class PantallaJuego(pilasengine.escenas.Escena):


	#defino un grupo de enemigos
	def crear_grupo_enemigos(self):
		self.enemigos = self.pilas.actores.Grupo()

	def crear_asteroide(self, tipo, radColision):
		asteroide = Asteroide(self.pilas, tipo=tipo);
		#creo un objeto para la física
		c1 = self.pilas.fisica.Circulo(asteroide.x, asteroide.y, radColision, restitucion=1, amortiguacion=2)
		asteroide.imitar(c1)
		#lo agrego al grupo
		self.enemigos.agregar(asteroide)

	def iniciar(self):

		global contador_texto
		global contador_choques
		global flag
		global flagEspeciales
		flag = [False, False, False, False, False]
		flagEspeciales = [False]
		self.crear_grupo_enemigos()


		contador_texto = 0
		contador_choques = 0

		fondo = self.pilas.fondos.Galaxia(dx=-2, dy=0)
		# MUSICA
		url = ruta + '/data/Dreams-Become-Real.ogg'
		musica = self.pilas.sonidos.cargar(url)
		musica.reproducir(repetir=True)

		# Boton de sonido ON / OFF
		boton_musica = self.pilas.actores.Boton();
		url = ruta + '/imagenes/sonidoON.png'
		boton_musica.imagen = url
		boton_musica.x = 410
		boton_musica.y = 240
		boton_musica.z = -1000
		boton_musica.sonidoOnOff = True

		def cambio(sonidoOnOff):

			if boton_musica.sonidoOnOff:
				# apago la musica
				musica.detener()
				url = ruta + '/imagenes/sonidoOFF.png'
				boton_musica.imagen = url
				boton_musica.sonidoOnOff = False

			else:
				#enciendo la música
				musica.reproducir(repetir=True)
				url = ruta + '/imagenes/sonidoON.png'
				boton_musica.imagen = url
				boton_musica.sonidoOnOff = True

		boton_musica.conectar_presionado(cambio, boton_musica.sonidoOnOff)

		# LOS TEXTOS
		#Le pido la biblioteca de textos contenido en textos.py
		from textos import textos

		texto_personalizado = self.pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -230, ancho = 230)
		sombra_texto_personalizado = self.pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -233, x=1, ancho = 230)

		sombra_texto_personalizado.color = self.pilas.colores.negro
		sombra_texto_personalizado.z = 4


		minave = Nave(self.pilas);
		minave.z = -2


		c2 = self.pilas.fisica.Circulo(minave.x, minave.y, 70, restitucion=0.1, amortiguacion=0.5)
		def seguir(evento):
			#print "X: " + str(evento.x)
			#print "Y: " + str(evento.y)
			if (evento.x < 390) or (evento.y < 219):
				# Solo sigo si el click es fuera del icono de sonido
				empujarx = (evento.x - c2.x) / 8
				empujary = (evento.y - c2.y) / 8
				c2.empujar(empujarx,empujary)

		def frenar():
			c2.velocidad_x /= 2
			c2.velocidad_y /= 2

		self.frenar = frenar
		self.pilas.tareas.siempre(0.1, self.frenar)


		self.seguir = seguir
		self.pilas.eventos.click_de_mouse.conectar(self.seguir)

		minave.imitar(c2, con_rotacion=False)

		emisor = EmisorHUMO(self.pilas, 0, 0)
		url = ruta + '/imagenes/humo.png'
		emisor.imagen_particula = self.pilas.imagenes.cargar_grilla(url)
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


		emisor.aprender(self.pilas.habilidades.Imitar, minave)

		minave.aprender(self.pilas.habilidades.MoverseConElTeclado)
		minave.aprender(self.pilas.habilidades.LimitadoABordesDePantalla)


		def imprimir_texto():

			global contador_texto

			#cambio el texto
			texto_personalizado.ancho = 900
			sombra_texto_personalizado.ancho = 900
			texto_personalizado.texto = textos[contador_texto]
			sombra_texto_personalizado.texto = textos[contador_texto]
			#oculto el texto y su sombra
			texto_personalizado.transparencia = 100
			sombra_texto_personalizado.transparencia = 100
			#lo hago visible nuevamente
			texto_personalizado.transparencia = [0]
			sombra_texto_personalizado.transparencia = [0]

			# Centro los textos en la pantalla

			factor = len(textos[contador_texto]) * 7

			texto_personalizado.x = 450 - factor
			sombra_texto_personalizado.x = 450 - factor

			contador_texto += 1 # incremento el contador para que la próxima vez muestre el siguiente texto.


		# Creo una tarea para que aparezcan los textos, cada 5 segundos.
		tareaMostrarTextos = self.pilas.tareas.siempre(5, imprimir_texto)


		def nave_choco():



			global contador_choques

			self.pilas.camara.vibrar(3, 0.5)

			contador_choques += 1

			if contador_choques == 2:
				minave.imagen = ruta + '/imagenes/lanave_01.png'
				emisor.frecuencia_creacion = 0.07
			if contador_choques == 4:
				minave.imagen = ruta + '/imagenes/lanave_02.png'
				emisor.frecuencia_creacion = 0.10
			if contador_choques == 7:
				minave.imagen = ruta + '/imagenes/lanave_03.png'
				emisor.frecuencia_creacion = 0.13
			if contador_choques == 9:
				minave.imagen = ruta + '/imagenes/lanave_04.png'
				emisor.eliminar()
				minave.rotacion = [360], 2
			if contador_choques == 12:
				self.pilas.camara.x = minave.x
				self.pilas.camara.y = minave.y
				perdido = Astronauta(self.pilas);
				minave.eliminar()
				musica.detener()
				self.pilas.camara.escala = [1.2, 1.5, 1]
				perdido.escala = [1, 0.4]
				texto_personalizado3 = self.pilas.actores.Texto(u'por miles de años flotarás exánime en el espacio · presiona ESPACIO', magnitud=18, fuente= url_fuente2, y= -230, x = 0)
				texto_personalizado3.color =  self.pilas.colores.blanco
				tareaMostrarTextos.terminar()
				texto_personalizado.transparencia = 100
				sombra_texto_personalizado.transparencia = 100
				self.pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)



			mensajeNeo = [False, False]
			print "Choques = " + str(contador_choques)
			if (contador_choques == 8) and (mensajeNeo[0] == False):
				os.system('clear')
				print "Despierta, Neo."
				print "La Matrix te tiene."
				print "Sigue al conejo blanco."
				print "Toc toc, Neo."
				mensajeNeo[0] = True
			if (contador_choques == 9) and (mensajeNeo[1] == False):
				os.system('clear')
				print "Choques = " + str(contador_choques)
				mensajeNeo[1] = True


		# Creo un control de coliciones para saber cuando perdes
		self.pilas.colisiones.agregar(minave, self.enemigos, nave_choco)

		#Elimino los límites laterales y la gravedad
		self.pilas.fisica.gravedad_x = 0
		self.pilas.fisica.gravedad_y = 0
		self.pilas.fisica.eliminar_paredes()
		self.pilas.fisica.eliminar_techo()
		self.pilas.fisica.eliminar_suelo()

	# Cuando pierdo, si presiono una tecla termina el juego y se cierra
	def al_pulsar_tecla(self, tecla):
		global flag
		#print tecla.codigo
		#pilas.escenas.PantallaMenu()
		if tecla.codigo == 32:
			flag = [False, False, False, False, False]
			self.pilas.escenas.PantallaMenu()


	def actualizar(self):
		''' Acá definimos las distintas etapas del juego, según van avanzando los textos
		    podemos ir cambiando los enemigos, el fondo, etc.  '''
		global contador_texto
		global flag

		def cambio_nivel(nivel, leyenda):# Cuando pasamos de nivel

			if (nivel <> 1): self.pilas.camara.vibrar(4, 1)
			texto_nivel = self.pilas.actores.Texto(cadena_de_texto="Nivel " + str(nivel) + ": " + leyenda,
			 magnitud = 40, x = -400, y = 230)
			texto_nivel.centro = ("izquierda", "centro")
			texto_nivel.transparencia = 0
			texto_nivel.transparencia = [100],15
			texto_nivel.escala = [0.7],10
			texto_nivel.x = [-400,-430],10
			texto_nivel.y = [240],10


		if contador_texto == 1:
			''' Recien al segundo texto comienzan a venir los asteroides '''
			# Creo una tarea para que aparezca un asteroide cada 2 segundos.

		if (flag[0]) == False:
				print "NIVEL 1"
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(2, self.crear_asteroide, "uno", 150)
				flag[0] = True
				cambio_nivel(1, "Cinco puntos de luz")

		if contador_texto == 35:
			''' ###  NIVEL 2 ###
			Llegamos al segundo nivel.  Aumentamos la velocidad de los enemigos y cambiamos el fondo. '''
			# Creo una tarea para que aparezca un asteroide cada 1.3 segundos.
			if (flag[1]) == False:
				print "NIVEL 2"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.3, self.crear_asteroide, "dos", 110) # A "crear_asteroide" le paso el tipo que tiene que crear y el radio de colisión.
				fondo = self.pilas.fondos.Galaxia(dx=-3, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_02.png'
				cambio_nivel(2, "Constelaciones")
				flag[1] = True

		if contador_texto == 69:
			''' ###  NIVEL 3 ### '''
			if (flag[2]) == False:
				print "NIVEL 3"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.5, self.crear_asteroide, "tres", 150)
				fondo = self.pilas.fondos.Galaxia(dx=-2, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_03.png'
				cambio_nivel(3, "Nuestra casa")
				flag[2] = True
		if contador_texto == 103:
			''' ###  NIVEL 4 ### '''
			if (flag[3]) == False:
				print "NIVEL 4"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(2, self.crear_asteroide, "cuatro", 150)
				fondo = self.pilas.fondos.Galaxia(dx=-1, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_04.png'
				cambio_nivel(4, "Mirando al pasado")
				flag[3] = True
		if contador_texto == 137:
			''' ###  NIVEL 5 ### '''
			if (flag[4]) == False:
				print "NIVEL 5"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.1, self.crear_asteroide, "cinco", 150)
				fondo = self.pilas.fondos.Galaxia(dx=-3, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_05.png'
				cambio_nivel(5, "La llegada")
				flag[4] = True
		if contador_texto == 170:
			''' FINAL! Ganó el juego '''
			self.pilas.escenas.PantallaFinal()



		''' Eventos únicos especiales durante el juego '''	

		# paso de ARSAT-2
		if contador_texto == 16:
			if flagEspeciales[0] == False:
				
				hudarsat = HUDArsat(self.pilas)
				hudarsat.z = 1000
				arsat = Arsat(self.pilas)
				arsat.x = hudarsat.x
				arsat.y = hudarsat.y
				arsat.z = 999
				flagEspeciales[0] = True
			



			

class PantallaFinal(pilasengine.escenas.Escena):
	def iniciar(self):
		fondo = self.pilas.fondos.Fondo()
		url = ruta + '/imagenes/final.jpg'
		fondo.imagen = self.pilas.imagenes.cargar(url)
		texto_personalizado = self.pilas.actores.Texto(u'¡ganaste!', magnitud=60, fuente= url_fuente,
		 y= -50, x = 20)




