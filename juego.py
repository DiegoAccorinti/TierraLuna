# -*- coding: utf-8
import pilasengine
from emisorHUMO import * 

pilas = pilasengine.iniciar(ancho=900, alto=550, titulo='TierraLuna')
contador_texto = 0

								
class Luna(pilasengine.actores.Actor):
	''' Este actor es para la presentación y para el final del juego '''

	def iniciar(self):
		self.imagen = "imagenes/luna.jpg"
		self.x = 0
		self.y = -600
		self.escala = 1.3
		self.z = -1

	def actualizar(self):
		self.rotacion -= 0.05

class PantallaJuego(pilasengine.escenas.Escena):

    def iniciar(self):

		fondo = pilas.fondos.Galaxia(dx=-2, dy=0)
		puntaje = pilas.actores.Puntaje(280, 200, color=pilas.colores.blanco, texto="0")
		choques = pilas.actores.Puntaje(600, 600, color=pilas.colores.blanco, texto="0") # uso 600,600 para que no se vea.
		
		# En "textos" guardamos la colección de frases que irán apareciendo durante la travesía.
		textos = [u'wwwwwwwwww',u'iiiiiiiii',u'este juego es distinto a todos los que jugaste antes',
		u'no se trata de medir tu habilidad',
		u'este viaje es en tiempo real',
		u'¿serás capáz de llegar a la luna?',
		u'¿podrás pilotear la nave durante una hora?',
		u'ya lo veremos.',
		u'No te preocupes, te acompañaré durante toda tu travesía.',
		u'Tengo muchas cosas para contarte',
		u'Antes que nada te recomiendo esquivar los asteroides',
		u'hicimos lo mejor que pudimos con la nave, pero no resistirá',
		u'más de 11 o 12 impactos.',
		u'Así que, no te distraigas  Jejeje',
		u'Vienes de un planeta llamado Tierra, pero',
		u'el 70% de su superficie está cubierta por agua',
		u'y solamente el 3% de esa agua es potable.',
		u'El término "planeta" viene de la palabra griega planetes,',
		u'que significa "errante".',
		u'En la antigua Grecia se dieron cuenta',
		u'de que había cinco puntos de luz',
		u'que se movían a través del resto de las estrellas',
		u'fijas en el cielo.',
		u'Algunas se movían constantemente hacia adelante,',
		u'otras daban marcha atrás.',
		u'Nadie sabía por qué, pero aquellos puntos de luz',
		u'no parpadeaban como las estrellas',
		u'Cada cultura tenía un nombre para',
		u'aquellos cinco puntos de luz:',
		u'Mercurio, Venus, Marte, Júpiter y Saturno.',
		u'Estos cuerpos celestes no viajan a través de las estrellas,',
		u'sino que orbitan alrededor del Sol,',
		u'la estrella central de nuestro Sistema Solar.'
		]
		texto_personalizado = pilas.actores.Texto('Comienza el viaje', magnitud=30, fuente="Tentacles.ttf", y= -230, ancho = 230)
		sombra_texto_personalizado = pilas.actores.Texto('Comienza el viaje', magnitud=30, fuente="Tentacles.ttf", y= -232, ancho = 230)

		sombra_texto_personalizado.color = pilas.colores.negro
		sombra_texto_personalizado.z = 4

		class Nave(pilasengine.actores.Actor):

			def iniciar(self):
				self.imagen = "imagenes/lanave.png"

		class Astronauta(pilasengine.actores.Actor):

			def iniciar(self):
				self.imagen = "imagenes/astronauta.png"
			def actualizar(self):
				self.rotacion += 1

		class Asteroide(pilasengine.actores.Actor):

			def iniciar(self):
				self.imagen = "imagenes/asteroide.png"
				self.escala = 0.3
				self.x = -500
				self.y = pilas.azar(-300, 300)
				self.giro = 2
				self.z = self.y
				
			def actualizar(self):
				self.rotacion += self.giro
				self.x += 2
				# Elimina el objeto cuando sale de la pantalla.
				if self.x > 500:
					self.eliminar()
					puntaje.aumentar()
							
		minave = Nave(pilas);
		minave.z = -2


		c2 = pilas.fisica.Circulo(minave.x, minave.y, 70, restitucion=0.1, amortiguacion=0.5)
		minave.imitar(c2)

		emisor = EmisorHUMO(pilas, 0, 0)
		emisor.imagen_particula = pilas.imagenes.cargar_grilla("imagenes/humo.png")
		emisor.constante = True
		emisor.composicion = "blanco"
		emisor.duracion = 2
		emisor.frecuencia_creacion = 0.03
		emisor.vida = 8
		emisor.aceleracion_x_min = 36
		emisor.aceleracion_x_max = 50
		emisor.x_min = 171
		emisor.y_min = 2
		emisor.transparencia_min = 30
		emisor.transparencia_max = 50


		emisor.aprender(pilas.habilidades.Imitar, minave)

		minave.aprender(pilas.habilidades.MoverseConElTeclado)
		minave.aprender(pilas.habilidades.LimitadoABordesDePantalla)


		#defino un grupo de enemigos
		enemigos = pilas.actores.Grupo()

		def crear_asteroide():
			#creo el actor enemigo
			asteroide = Asteroide(pilas);
			#creo un objeto para la física
			c1 = pilas.fisica.Circulo(asteroide.x, asteroide.y, 150, restitucion=1, amortiguacion=2)
			asteroide.imitar(c1)
			#lo agrego al grupo
			enemigos.agregar(asteroide)

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
				
				#determino un factor para centrar el texto
				'''if (len(textos[contador_texto]) > 20):
					texto_personalizado.ancho = len(textos[contador_texto] * 15)
				elif (len(textos[contador_texto]) > 10):
					texto_personalizado.ancho = len(textos[contador_texto] * 12)'''
					
					# tego un problema con esto.. el ancho varia mucho depende de qué letras 
					# tenga la cadena.  BUSCAR OTRA SOLUCION
				texto_personalizado.ancho = texto_personalizado.imagen.obtener_area_de_texto(texto_personalizado.texto)[0] + 200
				print texto_personalizado.ancho 
				
				sombra_texto_personalizado.ancho = texto_personalizado.ancho
				
				contador_texto += 1 # incremento el contador para que la próxima vez muestre el siguiente texto.
			else:
				# si no quedan textos que mostar, no muestro nada.
				texto_personalizado.texto = ''
				sombra_texto_personalizado.texto = ''


		# Creo una tarea para que aparezca un asteroide cada 2 segundos.
		pilas.tareas.siempre(2, crear_asteroide)  
		
			
		# Creo una tarea para que aparezcan los textos, cada 10 segundos.
		pilas.tareas.siempre(5, imprimir_texto)


		def nave_choco():#Cuando un asteroide choca nave
			
			pilas.camara.vibrar(3, 0.5)
			choques.aumentar()
			if choques.obtener() == 3:
				minave.imagen = "imagenes/lanave_01.png"
				emisor.frecuencia_creacion = 0.04
			if choques.obtener() == 6:
				minave.imagen = "imagenes/lanave_02.png"
				emisor.frecuencia_creacion = 0.07
			if choques.obtener() == 8:
				minave.imagen = "imagenes/lanave_03.png"
				emisor.frecuencia_creacion = 0.10
			if choques.obtener() == 10:
				minave.imagen = "imagenes/lanave_04.png"
				emisor.eliminar()
				minave.rotacion = [360], 2
			if choques.obtener() == 11:
				pilas.camara.x = minave.x
				pilas.camara.y = minave.y
				perdido = Astronauta(pilas);
				minave.eliminar()
				pilas.camara.escala = [1.2, 1.5, 1]
				perdido.escala = [1, 0.4]
				puntaje.eliminar()


		# Creo un control de coliciones para saber cuando perdes
		pilas.colisiones.agregar(minave, enemigos, nave_choco)

		#Elimino los límites laterales y la gravedad
		pilas.fisica.gravedad_x = 0
		pilas.fisica.gravedad_y = 0
		pilas.fisica.eliminar_paredes()
		pilas.fisica.eliminar_techo()
		pilas.fisica.eliminar_suelo()


# Escena Menu
def cargar_escena_juego():
	pilas.escenas.PantallaJuego()
	
def salir_del_juego():
	pilas.terminar()

class PantallaMenu(pilasengine.escenas.Escena):

    def iniciar(self):
		fondo = pilas.fondos.Color(pilas.colores.negro)
		fondo = pilas.fondos.Fondo()
		fondo.imagen = pilas.imagenes.cargar('imagenes/intro.png')
		fondo.z = -2
		
		luna = Luna(pilas);
		
		menu = pilas.actores.Menu([
					('iniciar juego', cargar_escena_juego),
					('salir',  salir_del_juego),
					
				], fuente='Tentacles.ttf', y=-30 )
		menu.escala = 3
		menu.escala = [1.5]

pilas.escenas.vincular(PantallaJuego)
pilas.escenas.vincular(PantallaMenu)
pilas.escenas.PantallaMenu()

pilas.ejecutar()
