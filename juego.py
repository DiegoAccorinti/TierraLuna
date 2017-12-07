#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine
from emisorHUMO import *
import os

# Inicializamos PILAS-ENGINE
# pasando como parámetros la resolución gráfica de la ventana y el título de la misma:

pilas = pilasengine.iniciar(ancho=900, alto=550, titulo='TierraLuna')


# Habilitando el Audio en PILAS: 

try:
  pilas.forzar_habilitacion_de_audio()
except AttributeError:
  print u"Omitiendo Habilitación forzada de audio, version anterior a 1.4.8".encode('utf-8')


# Definimos la ruta hasta los archivos de las dos tipografías que utilizaremos en el juego. 

ruta = os.path.dirname(os.path.realpath(__file__))
url_fuente = ruta + '/Tentacles.ttf'
url_fuente2 = ruta + '/Oswald-Regular.ttf'


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


class Arsat(pilasengine.actores.Actor):
	
	def iniciar(self):
		url = ruta + '/imagenes/ARSAT-2.png'
		self.imagen = url

	def actualizar(self):
		self.rotacion -= 0.06
		self.x += 0.6
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 600:
			self.eliminar()
		

			
class HUDArsat(pilasengine.actores.Actor):
	
	def iniciar(self):
		url = ruta + '/imagenes/ARSAT-2-HUD.png'
		self.imagen = url
		self.x = -600
		self.y = pilas.azar(-50, 150)
		self.escala = 1
		self.z = -1

	def actualizar(self):
		self.x += 0.6
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 600:
			self.eliminar()
		


# Esta escena es el juego propiamente. Es lo que comenzará cuando elijamos "iniciar juego" en el menú principal

class PantallaJuego(pilasengine.escenas.Escena):

	velocidad_asteroides = 2


	class Asteroide(pilasengine.actores.Actor):

		def iniciar(self, tipo):
			self.tipo = tipo
			if self.tipo == "uno":
				self.imagen = ruta + '/imagenes/asteroide.png'
				self.giro = 1
			if self.tipo == "dos":
				self.imagen = ruta + '/imagenes/asteroide2.png'
				self.giro = 3
			if self.tipo == "tres":
				self.imagen = ruta + '/imagenes/asteroide3.png'
				self.giro = 2
			if self.tipo == "cuatro":
				self.imagen = ruta + '/imagenes/asteroide4.png'
				self.giro = 3


			self.escala = 0.3
			self.x = -500
			self.y = pilas.azar(-300, 300)
			self.z = self.y

		def actualizar(self):
			self.rotacion += self.giro
			self.x += PantallaJuego.velocidad_asteroides
			# Elimina el objeto cuando sale de la pantalla.
			if self.x > 500:
				self.eliminar()

	#defino un grupo de enemigos
	enemigos = pilas.actores.Grupo()

	def crear_asteroide_uno(self):
		#creo el actor enemigo
		asteroide = self.Asteroide(pilas, tipo="uno");
		#creo un objeto para la física
		c1 = pilas.fisica.Circulo(asteroide.x, asteroide.y, 150, restitucion=1, amortiguacion=2)
		asteroide.imitar(c1)
		#lo agrego al grupo
		self.enemigos.agregar(asteroide)
		
	def crear_asteroide_dos(self):
		asteroide = self.Asteroide(pilas, tipo="dos");
		c1 = pilas.fisica.Circulo(asteroide.x, asteroide.y, 150, restitucion=1, amortiguacion=1)
		asteroide.imitar(c1)
		self.enemigos.agregar(asteroide)

	def crear_asteroide_tres(self):
		asteroide = self.Asteroide(pilas, tipo="tres");
		c1 = pilas.fisica.Circulo(asteroide.x, asteroide.y, 150, restitucion=1, amortiguacion=3)
		asteroide.imitar(c1)
		self.enemigos.agregar(asteroide)
		
	def crear_asteroide_cuatro(self):
		asteroide = self.Asteroide(pilas, tipo="cuatro");
		c1 = pilas.fisica.Circulo(asteroide.x, asteroide.y, 150, restitucion=1, amortiguacion=2)
		asteroide.imitar(c1)
		self.enemigos.agregar(asteroide)
		
	def iniciar(self):

		global contador_texto
		global contador_choques
		global flag
		global flagEspeciales
		flag = [False, False, False, False, False]
		flagEspeciales = [False]


		contador_texto = 0
		contador_choques = 0

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

		texto_personalizado = pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -230, ancho = 230)
		sombra_texto_personalizado = pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -233, x=1, ancho = 230)

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
		tareaMostrarTextos = pilas.tareas.siempre(5, imprimir_texto)


		def nave_choco():



			global contador_choques

			pilas.camara.vibrar(3, 0.5)

			contador_choques += 1

			if contador_choques == 2:
				minave.imagen = ruta + '/imagenes/lanave_01.png'
				emisor.frecuencia_creacion = 0.07
			if contador_choques == 4:
				minave.imagen = ruta + '/imagenes/lanave_02.png'
				emisor.frecuencia_creacion = 0.10
			if contador_choques == 8:
				minave.imagen = ruta + '/imagenes/lanave_03.png'
				emisor.frecuencia_creacion = 0.13
			if contador_choques == 16:
				minave.imagen = ruta + '/imagenes/lanave_04.png'
				emisor.eliminar()
				minave.rotacion = [360], 2
			if contador_choques == 20:
				pilas.camara.x = minave.x
				pilas.camara.y = minave.y
				perdido = Astronauta(pilas);
				minave.eliminar()
				musica.detener()
				pilas.camara.escala = [1.2, 1.5, 1]
				perdido.escala = [1, 0.4]
				texto_personalizado3 = pilas.actores.Texto(u'por miles de años flotarás exánime en el espacio · presiona ESPACIO', magnitud=18, fuente= url_fuente2, y= -230, x = 0)
				texto_personalizado3.color =  pilas.colores.blanco
				tareaMostrarTextos.terminar()
				texto_personalizado.transparencia = 100
				sombra_texto_personalizado.transparencia = 100
				pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)



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
		pilas.colisiones.agregar(minave, self.enemigos, nave_choco)

		#Elimino los límites laterales y la gravedad
		pilas.fisica.gravedad_x = 0
		pilas.fisica.gravedad_y = 0
		pilas.fisica.eliminar_paredes()
		pilas.fisica.eliminar_techo()
		pilas.fisica.eliminar_suelo()

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

			if (nivel <> 1): pilas.camara.vibrar(4, 1)
			texto_nivel = pilas.actores.Texto(cadena_de_texto="Nivel " + str(nivel) + ": " + leyenda,
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
				PantallaJuego.tareaAsteroides = pilas.tareas.siempre(2, self.crear_asteroide_uno)
				flag[0] = True
				cambio_nivel(1, "Cinco puntos de luz")

		if contador_texto == 34:
			''' ###  NIVEL 2 ###
			Llegamos al segundo nivel.  Aumentamos la velocidad de los enemigos y cambiamos el fondo. '''
			# Creo una tarea para que aparezca un asteroide cada 1.5 segundos.
			if (flag[1]) == False:
				print "NIVEL 2"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = pilas.tareas.siempre(1.5, self.crear_asteroide_dos)
				PantallaJuego.velocidad_asteroides = 6
				fondo = pilas.fondos.Galaxia(dx=-3, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_02.png'
				cambio_nivel(2, "Constelaciones")
				flag[1] = True

		if contador_texto == 68:
			''' ###  NIVEL 3 ### '''
			if (flag[2]) == False:
				print "NIVEL 3"
				PantallaJuego.velocidad_asteroides = 4
				fondo = pilas.fondos.Galaxia(dx=-2, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_03.png'
				cambio_nivel(3, "Nuestra casa")
				flag[2] = True
		if contador_texto == 102:
			''' ###  NIVEL 4 ### '''
			if (flag[3]) == False:
				print "NIVEL 4"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = pilas.tareas.siempre(2, self.crear_asteroide_tres)
				PantallaJuego.velocidad_asteroides = 2
				fondo = pilas.fondos.Galaxia(dx=-1, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_04.png'
				cambio_nivel(4, "Mirando al pasado")
				flag[3] = True
		if contador_texto == 130:
			''' ###  NIVEL 5 ### '''
			if (flag[4]) == False:
				print "NIVEL 5"
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = pilas.tareas.siempre(1.5, self.crear_asteroide_cuatro)
				PantallaJuego.velocidad_asteroides = 6
				fondo = pilas.fondos.Galaxia(dx=-3, dy=0)
				fondo.imagen = ruta + '/imagenes/galaxia_05.png'
				cambio_nivel(5, "La llegada")
				flag[4] = True
		if contador_texto == 141:
			''' FINAL! Ganó el juego '''
			pilas.escenas.PantallaFinal()



		''' Eventos únicos especiales durante el juego '''	

		# paso de ARSAT-2
		if contador_texto == 16:
			if flagEspeciales[0] == False:
				
				hudarsat = HUDArsat(pilas)
				hudarsat.z = 1000
				arsat = Arsat(pilas)
				arsat.x = hudarsat.x
				arsat.y = hudarsat.y
				arsat.z = 999
				flagEspeciales[0] = True
			



			

class PantallaFinal(pilasengine.escenas.Escena):
	def iniciar(self):
		fondo = pilas.fondos.Fondo()
		url = ruta + '/imagenes/final.jpg'
		fondo.imagen = pilas.imagenes.cargar(url)
		texto_personalizado = pilas.actores.Texto(u'¡ganaste!', magnitud=60, fuente= url_fuente,
		 y= -50, x = 20)



class PantallaConfig(pilasengine.escenas.Escena):

	mostre_huevo_pascua = False

	def iniciar(self):

		fondo = pilas.fondos.Galaxia(dx=0, dy=0)
		fondo.imagen = ruta + '/imagenes/fondo-config.png'
		texto_personalizado = pilas.actores.Texto(u'¡no hay nada que configurar!', magnitud=55, fuente= url_fuente,
		 y= 0, x = 0)
		texto_personalizado2 = pilas.actores.Texto(u'presione ESPACIO para continuar', magnitud=14, fuente= url_fuente2, y= -230, x = 0)
		texto_personalizado2.color =  pilas.colores.gris



		pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)

	def al_pulsar_tecla(self, tecla):

		if tecla.codigo == 32:
			pilas.escenas.PantallaMenu()
		else:
			if (self.mostre_huevo_pascua == False):
				texto_personalizado3 = pilas.actores.Texto(u'Un juego de Diego Accorinti para Huayra gnu/linux', magnitud=12, fuente= url_fuente2, y= -200, x = 0)
				self.mostre_huevo_pascua = True

# Escena Menu
def cargar_escena_juego():
	pilas.escenas.PantallaJuego()

def cargar_escena_config():
	pilas.escenas.PantallaConfig()

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
					('JUGAR', cargar_escena_juego),
					(u'CONFIG', cargar_escena_config),
					('SALIR', salir_del_juego),
				], fuente = url_fuente2, y = 150)
		menu.escala = 1
		menu.x = [300],3
		menu.transparencia = 100
		menu.transparencia = [0],3


pilas.escenas.vincular(PantallaJuego)
pilas.escenas.vincular(PantallaMenu)
pilas.escenas.vincular(PantallaConfig)
pilas.escenas.vincular(PantallaFinal)
pilas.escenas.PantallaMenu()

pilas.ejecutar()
