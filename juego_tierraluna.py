#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine

from globales import *
from objetos import *
from fondos import *
# Pantallas adicionales
from pantallas_juego import *
# LOS TEXTOS
# Le pido la biblioteca de textos contenido en textos.py
from textos import textos

# Esta escena es el juego propiamente. Es lo que comenzará cuando elijamos "iniciar juego" en el menú principal


class PantallaJuego(pilasengine.escenas.Escena):
	def crearFondosNivel(self, lvl):
		self.lvl = lvl
		if self.lvl=="NIVEL1":
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, img="fondo_01.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = 0
			espacio_medio = capa(self.pilas, img="medio_01.png", tipo="medio", flip=False)
			espacio_frente = capa(self.pilas, img="frente_01.png", tipo="frente", flip=False)
			#Ahora la mitad inferior de la pantalla
			#fondo_1_flip = capa(self.pilas, img="fondo_01.jpg", tipo="fondo", flip=True)
			#medio_1_flip = capa(self.pilas, img="medio_01.png", tipo="medio", flip=True)
			#frente_1_flip = capa(self.pilas, img="frente_01.png", tipo="frente", flip=True)
			espacio_fondo.transparencia = [0], 5

		elif self.lvl=="NIVEL2":
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, img="fondo_02.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = [0], 5
			
		elif self.lvl=="NIVEL3":
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, img="fondo_03.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = [0], 5 
		elif self.lvl=="NIVEL4":
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, img="fondo_04.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = [0], 5 
		elif self.lvl=="NIVEL5":
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, img="fondo_05.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = [0], 5 
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
		global flag
		global flagEspeciales
		global pausa 
		pausa = False
		flag = [False, False, False, False, False]
		flagEspeciales = [False, False]
		self.crear_grupo_enemigos()
		
		self.pilas.eventos.pulsa_tecla.conectar(self.pausar_juego)
		self.crearFondosNivel(lvl="NIVEL1")
		tierra = Tierra(self.pilas)
		
		
		
		contador_texto = 33  #0




		# MUSICA
		url = ruta + '/data/Dreams-Become-Real.ogg'
		self.musica = self.pilas.sonidos.cargar(url)
		self.musica.reproducir(repetir=True)

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
				self.musica.detener()
				url = ruta + '/imagenes/sonidoOFF.png'
				boton_musica.imagen = url
				boton_musica.sonidoOnOff = False

			else:
				#enciendo la música
				self.musica.reproducir(repetir=True)
				url = ruta + '/imagenes/sonidoON.png'
				boton_musica.imagen = url
				boton_musica.sonidoOnOff = True

		boton_musica.conectar_presionado(cambio, boton_musica.sonidoOnOff)



		self.texto_personalizado = self.pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -230, ancho = 230)
		self.sombra_texto_personalizado = self.pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -233, x=1, ancho = 230)
		self.sombra_texto_personalizado.color = self.pilas.colores.negro
		self.sombra_texto_personalizado.z = 4

		self.minave = Nave(self.pilas, pilotoAutomatico = False);
		
		c2 = self.pilas.fisica.Circulo(self.minave.x, self.minave.y, 70, restitucion=0.1, amortiguacion=0.5)
		
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

		self.minave.imitar(c2, con_rotacion=False)
		self.minave.emisor.aprender(self.pilas.habilidades.Imitar, self.minave)

		self.minave.aprender(self.pilas.habilidades.MoverseConElTeclado)
		self.minave.aprender(self.pilas.habilidades.LimitadoABordesDePantalla)


		def imprimir_texto():

			global contador_texto

			#cambio el texto
			self.texto_personalizado.ancho = 900
			self.sombra_texto_personalizado.ancho = 900
			self.texto_personalizado.texto = textos[contador_texto]
			self.sombra_texto_personalizado.texto = textos[contador_texto]
			#oculto el texto y su sombra
			self.texto_personalizado.transparencia = 100
			self.sombra_texto_personalizado.transparencia = 100
			#lo hago visible nuevamente
			self.texto_personalizado.transparencia = [0]
			self.sombra_texto_personalizado.transparencia = [0]

			# Centro los textos en la pantalla

			factor = len(textos[contador_texto]) * 7

			self.texto_personalizado.x = 450 - factor
			self.sombra_texto_personalizado.x = 450 - factor

			contador_texto += 1 # incremento el contador para que la próxima vez muestre el siguiente texto.


		# Creo una tarea para que aparezcan los textos, cada 5 segundos.
		self.tareaMostrarTextos = self.pilas.tareas.siempre(5, imprimir_texto)
		
		# Creo un control de coliciones para saber cuando perdes
		self.pilas.colisiones.agregar(self.minave, self.enemigos, self.minave.choque)

		#Elimino los límites laterales y la gravedad
		self.pilas.fisica.gravedad_x = 0
		self.pilas.fisica.gravedad_y = 0
		self.pilas.fisica.eliminar_paredes()
		self.pilas.fisica.eliminar_techo()
		self.pilas.fisica.eliminar_suelo()

	# Cuando pierdo, si presiono una tecla termina el juego y se cierra
	def al_pulsar_tecla(self, tecla):
		global flag
		if tecla.codigo == 32:
			flag = [False, False, False, False, False]
			self.pilas.escenas.PantallaMenu()

	def pausar_juego(self, tecla):
		global pausa 
		#print tecla.codigo
		if tecla.codigo == "p":
			pausa = not pausa 
			if pausa:
				self.pilas.widget.pausar()
			else:
				self.pilas.widget.continuar()
			

	def actualizar(self):
		''' Acá definimos las distintas etapas del juego, según van avanzando los textos
		    podemos ir cambiando los enemigos, el fondo, etc.  '''
		global contador_texto
		global flag

		if self.minave.choques == 12:
			self.tareaMostrarTextos.terminar()
			self.texto_personalizado.transparencia = 100
			self.sombra_texto_personalizado.transparencia = 100
			self.musica.detener()
			self.minave.choques +=1 # Hack para evitar que vuelva a terminar la lista de tareas

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

		if contador_texto == 35: #35
			''' ###  NIVEL 2 ###
			Llegamos al segundo nivel. Aumentamos la velocidad de los enemigos y cambiamos el fondo. '''
			# Creo una tarea para que aparezca un asteroide cada 1.3 segundos.
			if (flag[1]) == False:
				print "NIVEL 2"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.3, self.crear_asteroide, "dos", 110) # A "crear_asteroide" le paso el tipo que tiene que crear y el radio de colisión.
				self.crearFondosNivel(lvl="NIVEL2")
				cambio_nivel(2, "Constelaciones")
				flag[1] = True

		if contador_texto == 69: #69
			''' ###  NIVEL 3 ### '''
			if (flag[2]) == False:
				print "NIVEL 3"
				PantallaJuego.tareaAsteroides.terminar()

				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.5, self.crear_asteroide, "tres", 150)
				self.crearFondosNivel(lvl="NIVEL3")				
				cambio_nivel(3, "Nuestra casa")
				flag[2] = True
		if contador_texto == 103: #103
			''' ###  NIVEL 4 ### '''
			if (flag[3]) == False:
				print "NIVEL 4"
				PantallaJuego.tareaAsteroides.terminar()
				
				
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(2, self.crear_asteroide, "cuatro", 150)
				self.crearFondosNivel(lvl="NIVEL4")
				cambio_nivel(4, "Mirando al pasado")
				flag[3] = True
		if contador_texto == 137: #137
			''' ###  NIVEL 5 ### '''
			if (flag[4]) == False:
				print "NIVEL 5"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.1, self.crear_asteroide, "cinco", 150)
				self.crearFondosNivel(lvl="NIVEL5")
				cambio_nivel(5, "La llegada")
				flag[4] = True
				luna_final = LunaFinal(self.pilas)
				
				
		if contador_texto == 170: #170
			''' FINAL! Ganó el juego '''
			self.pilas.escenas.PantallaFinal()



		''' Eventos únicos especiales durante el juego '''	

		# paso de ARSAT-2
		if contador_texto == 16:
			if flagEspeciales[0] == False:
				hudarsat = HUDArsat(self.pilas)
				arsat = Arsat(self.pilas)
				arsat.x = hudarsat.x
				arsat.y = hudarsat.y
				flagEspeciales[0] = True
		
		# Crea una estacion de reparacion para reparar un poco la nave
		if contador_texto == 100:
			if flagEspeciales[1] == False:
				estacion_reparacion = Reparacion(self.pilas) 
				rep_colision = self.pilas.fisica.Circulo(estacion_reparacion.x, estacion_reparacion.y, 70, restitucion=0.1, amortiguacion=0.5)
				estacion_reparacion.imitar(rep_colision)
				self.pilas.colisiones.agregar(self.minave, estacion_reparacion, self.minave.choque_repara)
				flagEspeciales[1] = True
					
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

