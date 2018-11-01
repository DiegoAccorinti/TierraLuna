#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine
import codecs # Libreria para importar textos con distintos encodeados, como utf-8

from globales import *
from objetos import *
from fondos import *
# Pantallas adicionales
from pantallas_juego import *

from movimiento_de_nave import MovimientoDeNave



# Esta escena es el juego propiamente. Es lo que comenzará cuando elijamos "iniciar juego" en el menú principal


class PantallaJuego(pilasengine.escenas.Escena):
	
	def crearFondosNivel(self, tema):
		tema = self.tema_fondos 
		if self.nivel==1:
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, tema=tema, img="fondo_01.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = 0
			espacio_medio = capa(self.pilas, tema=tema, img="medio_01.png", tipo="medio", flip=False)
			espacio_frente = capa(self.pilas, tema=tema, img="frente_01.png", tipo="frente", flip=False)
			#Ahora la mitad inferior de la pantalla
			#fondo_1_flip = capa(self.pilas, img="fondo_01.jpg", tipo="fondo", flip=True)
			#medio_1_flip = capa(self.pilas, img="medio_01.png", tipo="medio", flip=True)
			#frente_1_flip = capa(self.pilas, img="frente_01.png", tipo="frente", flip=True)
			espacio_fondo.transparencia = [0], 5

		elif self.nivel==2:
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, tema=tema, img="fondo_02.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = [0], 5
			
		elif self.nivel==3:
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, tema=tema, img="fondo_03.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = [0], 5 
		elif self.nivel==4:
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, tema=tema, img="fondo_04.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = [0], 5 
		elif self.nivel==5:
			#Crea el fondo del nivel 1 usando tres capas
			#capa(self, img, depth, flip)
			espacio_fondo = capa(self.pilas, tema=tema, img="fondo_05.jpg", tipo="fondo", flip=False)
			espacio_fondo.transparencia = [0], 5 
	#defino un grupo de enemigos
	def crear_grupo_enemigos(self):
		self.enemigos = self.pilas.actores.Grupo()

	def crear_asteroide(self, tipo, radColision):
		asteroide = Asteroide(self.pilas, tema=self.tema_sprites, tipo=tipo);
		#creo un objeto para la física
		c1 = self.pilas.fisica.Circulo(asteroide.x, asteroide.y, radColision, restitucion=1, amortiguacion=2)
		asteroide.imitar(c1)
		#lo agrego al grupo
		self.enemigos.agregar(asteroide)

	def cambio(self, sonidoOnOff):
		if self.boton_musica.sonidoOnOff:
			# apago la musica
			self.musica.detener()
			url = ruta + '/imagenes/sonidoOFF.png'
			self.boton_musica.imagen = url
			self.boton_musica.sonidoOnOff = False
		else:
			#enciendo la música
			self.musica.reproducir(repetir=True)
			url = ruta + '/imagenes/sonidoON.png'
			self.boton_musica.imagen = url
			self.boton_musica.sonidoOnOff = True		

	def iniciarMusica(self):
		# MUSICA
		url = ruta + '/data/Dreams-Become-Real.ogg'
		self.musica = self.pilas.sonidos.cargar(url)
		self.musica.reproducir(repetir=True)

		# Boton de sonido ON / OFF
		self.boton_musica = self.pilas.actores.Boton();
		url = ruta + '/imagenes/sonidoON.png'
		self.boton_musica.imagen = url
		self.boton_musica.x = 410
		self.boton_musica.y = 240
		self.boton_musica.z = -1000
		self.boton_musica.sonidoOnOff = True
		self.boton_musica.conectar_presionado(self.cambio, self.boton_musica.sonidoOnOff)

	def cargarTextos(self):
		''' Carga el archivo con la definicion de la aventura y lo guarda en una lista'''
		self.textos = []
		nombre_archivo = ruta + "/" + self.tema_textos + "/aventura.txt"
		archivo = codecs.open(nombre_archivo, "r", "utf8")


		self.textos = [line.rstrip('\n') for line in archivo]


	def analizarLinea(self, linea):
		global flag
		global flagEspeciales
		
		''' Solo entra aqui si se trata de un tag '''
		if linea[:6] == "<NIVEL": # Los primeros 6 caracteres
			self.nivel = int(linea[6]) # convierte en entero la cadena con el numero de nivel
			#print "cambio de nivel: ", self.nivel
			findelinea = "</NIVEL" + linea[6] + ">"
			self.leyenda = linea[7:].rstrip(findelinea) # Elimina el tag de cierre de la linea
			self.leyenda = self.leyenda.lstrip(">")
			#print "Leyenda: ", self.leyenda
			self.iniciar_nivel()
			
		elif linea[:7] == "<EVENTO":
			#print "Hay que hacer algo"
			if linea[7]=="1":
				self.lanzarEvento("satelite")
			elif linea[7]=="2":
				self.lanzarEvento("reparacion")
			else:
				print "No hay evento de tipo: ", linea[7]
						
		elif linea[:5] == "<FIN>":
			#print "Debemos terminar el juego"
			self.finalizarJuego()
		elif linea[:6] == "<LOOP>":
			#print "Vuelve a mostrar desde el comienzo"
			self.contador_texto = 0 # Resetea contador de lineas
			flag = [False, False, False, False, False]
			flagEspeciales = [False, False]
			
	def obtenerLinea(self):
		linea = self.textos[self.contador_texto] 
		print linea 
		if len(linea)> 0: #Puede ser que se trate de una linea nula en lugar de un espacio
			if linea[0] == "<":
				#print "Es una palabra clave"
				self.analizarLinea(linea)
			else:
				self.imprimirTexto(linea)
		self.contador_texto += 1 # incremento el contador para que la próxima vez muestre el siguiente texto.
		
	def imprimirTexto(self, linea):

		self.texto_personalizado.ancho = 900
		self.sombra_texto_personalizado.ancho = 900
		
		self.texto_personalizado.texto = linea #self.textos[self.contador_texto]
		self.sombra_texto_personalizado.texto = linea #self.textos[self.contador_texto]
		#oculto el texto y su sombra
		self.texto_personalizado.transparencia = 100
		self.sombra_texto_personalizado.transparencia = 100
		#lo hago visible nuevamente
		self.texto_personalizado.transparencia = [0]
		self.sombra_texto_personalizado.transparencia = [0]

		# Centro los textos en la pantalla
		factor = len(linea) * 7
		#factor = len(self.textos[self.contador_texto]) * 7

		self.texto_personalizado.x = 450 - factor
		self.sombra_texto_personalizado.x = 450 - factor

	def finalizarJuego(self):
		''' FINAL! Ganó el juego '''
		self.pilas.escenas.PantallaFinal(self.mitema)
	
	def lanzarEvento(self, evento):
		'''Iniciar los eventos esporádicos en el juego, como el paso de un satelite'''
		if evento=="satelite":
			# paso de ARSAT-2
			etiqueta = HUDArsat(self.pilas, tema=self.mitema[1])
			satelite = Arsat(self.pilas, tema=self.mitema[1])
			satelite.x = etiqueta.x
			satelite.y = etiqueta.y
		elif evento=="reparacion":
			# Crea una estacion de reparacion para reparar un poco la nave
			estacion_reparacion = Reparacion(self.pilas, tema=self.mitema[1]) 
			rep_colision = self.pilas.fisica.Circulo(estacion_reparacion.x, estacion_reparacion.y, 70, restitucion=0.1, amortiguacion=0.5)
			estacion_reparacion.imitar(rep_colision)
			self.pilas.colisiones.agregar(self.minave, estacion_reparacion, self.minave.choque_repara)
			
	def iniciar(self, tema_actual, tema_sprites, tema_fondos, tema_textos):

		#global contador_texto
		global flag
		global flagEspeciales
		global pausa
		
		self.nivel = 1 #Nivel inicial
		self.leyenda = ""
		
		self.contador_texto = 0 #0
		self.textos = []
		
		self.tema_sprites = tema_sprites
		self.tema_fondos = tema_fondos
		self.tema_textos = tema_textos 
		self.tema_actual = tema_actual
		
		self.mitema = [ tema_actual, tema_sprites, tema_fondos, tema_textos ]
		pausa = False
		flag = [False, False, False, False, False]
		flagEspeciales = [False, False]
		self.crear_grupo_enemigos()
		
		self.pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)
		self.pilas.eventos.pulsa_tecla_escape.conectar(self.salir_juego)
		
		self.crearFondosNivel(tema=self.tema_fondos)
		tierra = Tierra(self.pilas, tema=self.tema_sprites)
		
		self.iniciarMusica()
		self.cargarTextos()
		#self.iniciar_nivel()
		
		self.texto_personalizado = self.pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -230, ancho = 230)
		self.sombra_texto_personalizado = self.pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -233, x=1, ancho = 230)
		self.sombra_texto_personalizado.color = self.pilas.colores.negro
		self.sombra_texto_personalizado.z = 4

		self.iniciar_nave()
		
		
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

		self.minave.aprender(MovimientoDeNave, velocidad_maxima=3)
		self.minave.aprender(self.pilas.habilidades.LimitadoABordesDePantalla)


		# Creo una tarea para que aparezcan los textos, cada 5 segundos.
		self.tareaMostrarTextos = self.pilas.tareas.siempre(5, self.obtenerLinea)
		
		self.iniciar_colisiones()

		#Elimino los límites laterales y la gravedad
		self.pilas.fisica.gravedad_x = 0
		self.pilas.fisica.gravedad_y = 0
		self.pilas.fisica.eliminar_paredes()
		self.pilas.fisica.eliminar_techo()
		self.pilas.fisica.eliminar_suelo()

	def iniciar_colisiones(self):
		# Creo un control de coliciones para saber cuando perdes
		self.pilas.colisiones.agregar(self.minave, self.enemigos, self.minave.choque)

	def iniciar_nave(self):
		self.minave = Nave(self.pilas, self.mitema, pilotoAutomatico = False);
		
	# Cuando pierdo, si presiono una tecla termina el juego y se cierra
	def al_pulsar_tecla(self, tecla):
		global flag
		global pausa
		if tecla.codigo == 32 or tecla.codigo =="p": #barra espaciadora
			if self.minave.choques < 12: # Si estamos vivos
				pausa = not pausa 
				if pausa:
					self.pilas.widget.pausar()
				else:
					self.pilas.widget.continuar()
			else: #Si nos mataron debe salir del juego
				self.salir_juego(tecla)
				
	def salir_juego(self, tecla):
		global pausa
		#Sale del juego hacia la pantalla del menu principal
		if pausa:
			self.pilas.widget.continuar()
			pausa = not pausa
		self.musica.detener()
		self.pilas.escenas.PantallaMenu(self.tema_actual, self.tema_sprites, self.tema_fondos, self.tema_textos)
			
	def intro_nivel(self):# Cuando pasamos de nivel
		'''Muestra la leyenda que acompaña a la definicion del nivel'''
		if self.nivel <> 1: 
			self.pilas.camara.vibrar(4, 1)
		texto_nivel = self.pilas.actores.Texto(cadena_de_texto="Nivel " + str(self.nivel) + ": " + self.leyenda, magnitud = 40, x = -400, y = 230)
		texto_nivel.centro = ("izquierda", "centro")
		texto_nivel.transparencia = 0
		texto_nivel.transparencia = [100],15
		texto_nivel.escala = [0.7],10
		texto_nivel.x = [-400,-430],10
		texto_nivel.y = [240],10
	
	def iniciar_nivel(self):	
		'''Define las caracteristicas de los niveles y el tipo de enemigo y lo inicia'''
		global flag
		if self.nivel == 1:
			if (flag[0]) == False:
				#print "NIVEL ", self.nivel
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(2, self.crear_asteroide, "uno", 150)
				flag[0] = True
		elif self.nivel == 2:
			if (flag[1]) == False:
				#print "NIVEL ", self.nivel
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.3, self.crear_asteroide, "dos", 110) # A "crear_asteroide" le paso el tipo que tiene que crear y el radio de colisión.
				self.crearFondosNivel(tema=self.tema_fondos) #argumentos originales: lvl="NIVEL2", tema=self.tema_fondos 
				flag[1] = True
		elif self.nivel == 3:
			if (flag[2]) == False:
				#print "NIVEL ", self.nivel
				PantallaJuego.tareaAsteroides.terminar()

				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.5, self.crear_asteroide, "tres", 150)
				self.crearFondosNivel(tema=self.tema_fondos)				
				flag[2] = True
		elif self.nivel == 4:
			if (flag[3]) == False:
				#print "NIVEL ", self.nivel
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(2, self.crear_asteroide, "cuatro", 150)
				self.crearFondosNivel(tema=self.tema_fondos)
				flag[3] = True
		elif self.nivel == 5:
			if (flag[4]) == False:
				#print "NIVEL ", self.nivel
				PantallaJuego.tareaAsteroides.terminar()
				PantallaJuego.tareaAsteroides = self.pilas.tareas.siempre(1.1, self.crear_asteroide, "cinco", 150)
				self.crearFondosNivel(tema=self.tema_fondos)
				flag[4] = True
				luna_final = LunaFinal(self.pilas, tema=self.tema_sprites)
		self.intro_nivel()
		
	def actualizar(self):
		''' Bucle del juego, chequeamos estado de la nave  '''
		#global flag

		if self.minave.choques == 12:
			self.tareaMostrarTextos.terminar()
			self.texto_personalizado.transparencia = 100
			self.sombra_texto_personalizado.transparencia = 100
			self.musica.detener()
			self.minave.choques +=1 # Hack para evitar que vuelva a terminar la lista de tareas
