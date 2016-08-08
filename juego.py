#!/usr/bin/env python
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
		self.y = -700
		self.escala = 1.3
		self.z = -1

	def actualizar(self):
		self.rotacion -= 0.05

'''
Esta escena es el juego propiamente. Es lo que comenzará cuando elijamos
"iniciar juego" en el menú principal
'''


class PantallaJuego(pilasengine.escenas.Escena):

	puntaje = pilas.actores.Puntaje(280, 200, color=pilas.colores.blanco, texto="0")
	choques = pilas.actores.Puntaje(600, 600, color=pilas.colores.blanco, texto="0") # uso 600,600 para que no se vea.
	velocidad_asteroides = 2

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
			self.x += PantallaJuego.velocidad_asteroides
			# Elimina el objeto cuando sale de la pantalla.
			if self.x > 500:
				self.eliminar()
				PantallaJuego.puntaje.aumentar()
				#print "PUNTOS"+ str(PantallaJuego.puntaje.obtener())

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
		#musica = pilas.sonidos.cargar('musica/Dreams-Become-Real.ogg')
		#musica.reproducir(repetir=True)

		'''
		En "textos" guardamos la colección de frases que irán apareciendo
		durante la travesía.
		'''
		textos = [u'este juego es distinto a todos los que jugaste antes',
		u'no se trata de medir tu habilidad',
		u'este viaje es en tiempo real',
		u'¿serás capáz de llegar a la luna?',
		u'¿podrás pilotear la nave durante una hora?',
		u'ya lo veremos.',
		u'No te preocupes, te acompañaré durante toda tu travesía.',
		u'Tengo muchas cosas para contarte',
		u'Antes que nada te recomiendo esquivar los asteroides',
		u'hicimos lo mejor que pudimos con la nave,',
		u'pero no resistirá más de 11 o 12 impactos.',
		u'Así que, no te distraigas jejeje',
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
		u'la estrella central de nuestro Sistema Solar.', '',
		#31 textos
		#Nivel2
		u'Excelente! llegamos a un nuevo nivel, ya estamos más cerca.',
		u'¿cómo lo vas llevando?', u'mucho cuidado con los asteorides..',
		u'o quedarás flotando en el espacio como una batata sideral.',
		u'mmm tratemos de que esto no se descontrole',
		u'',
		u'Me hace hambre. Siempre que viajo',
		u'llevo un paquete de sandwiches de miga',
		u'jamón y queso. mayonesa.',
		u'y el mate, no puede faltar el mate',
		u'¿te parece raro tomar mate en el espacio?',
		u'dale, mientras te cuento sobre constelaciones.',
		u'',
		u'Las estrellas de una constelación no suelen tener',
		u'más relación que su proximidad en el cielo',
		u'tal como se ven desde la Tierra.',
		u'Las estrellas que forman una constelación',
		u'pueden no mantener relación entre sí,',
		u'ya que algunas están relativamente cerca de la Tierra',
		u'y otras se encuentran a distancias mucho mayores',
		u'en el espacio. Al verlas desde la tierra forman',
		u'figuras que podemos observar.',
		'',
		u'Las distancias a las estrellas se miden en años luz.',
		u'Un año luz equivale a unos 9,5 billones de kilómetros.',
		u'La gente confunde un año luz con una medida de tiempo',
		u'porque el término contiene la palabra año.',
		u'Sin embargo, un año luz es una medida de distancia:',
		u'la longitud que recorre la luz moviéndose',
		u'a 300.000 kilómetros por segundo',
		u'durante un año.',
		u'',
		#32 textos
		#Nivel3
		u'La estrella más próxima a La Tierra',
		u'luego del Sol es Próxima Centauri,',
		u'está a unos 4 años luz de distancia.',
		u'Los astrónomos no pueden ver Próxima Centauri',
		u'tal como es hoy,',
		u'sino tal y como era hace cuatro años.',
		u'La galaxia Andrómeda es el objeto más distante',
		u'que se puede ver a simple vista, en una',
		u'noche despejada y oscura en otoño.',
		u'La luz que recibe tu ojo',
		u'dejó esa galaxia hace unos 2,6 millones de años.',
		u'Si se produjera un gran cambio en Andrómeda mañana,',
		u'no lo sabremos hasta dentro de',
		u'más de dos millones de años.',
		u'',
		u'A veces escucho sobre',
		u'proyectos de exploración del espacio',
		u'que tienen como objetivo',
		u'encontrar otros planetas habitables.',
		u'Pienso ¿por qué en vez de buscar un planeta',
		u'de repuesto, no cuidamos más y sanamos',
		u'el que ya tenemos?',
		u'se pueden hacer muchas cosas por La Tierra.',
		u'',
		u'Por ejemplo,',
		u'Cambiar el automovil por la bicicleta en viajes cortos.',
		u'Cambiar el ascensor por las escaleras en tres o menos pisos.',
		u'De esta forma ahorrás energía',
		u'y fortalecés tu salud al mismo tiempo.',
		u'Desenchufa todo lo que no uses.',
		u'Muchos equipos por más que estén apagados',
		u'consumen electricidad.',
		u'Usá lamparitas de LED que duran mucho más',
		u'que las tradicionales, incluso las fluorescentes,',
		u'y consumen menos energía.',
		u'Comenzá a usar una bolsa de las compras',
		u'en vez de recibir las bolsas plásticas comunes,',
		u'que no son biodegradables',
		u' y además cuestan dinero extra.',
		u'Si cerras la canilla mientras te cepillás los dientes,',
		u'ahorrás unos 60 litros de agua potable por mes.',
		#40 textos
		u'Antes de tirar cualquier cosa a la basura,',
		u'piensa si se puede reutilizar, reciclar o reparar.']

		texto_personalizado = pilas.actores.Texto('Comienza el viaje', magnitud=30, fuente="Tentacles.ttf", y= -230, ancho = 230)
		sombra_texto_personalizado = pilas.actores.Texto('Comienza el viaje', magnitud=30, fuente="Tentacles.ttf", y= -233, x=1, ancho = 230)

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

		minave = Nave(pilas);
		minave.z = -2


		c2 = pilas.fisica.Circulo(minave.x, minave.y, 70, restitucion=0.1, amortiguacion=0.5)
		def seguir(evento):

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
		emisor.imagen_particula = pilas.imagenes.cargar_grilla("imagenes/humo.png")
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
				factor = texto_personalizado.imagen.obtener_area_de_texto(texto_personalizado.texto)[0] + 10
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
				minave.imagen = "imagenes/lanave_01.png"
				emisor.frecuencia_creacion = 0.07
			if self.choques.obtener() == 6:
				minave.imagen = "imagenes/lanave_02.png"
				emisor.frecuencia_creacion = 0.10
			if self.choques.obtener() == 8:
				minave.imagen = "imagenes/lanave_03.png"
				emisor.frecuencia_creacion = 0.13
			if self.choques.obtener() == 10:
				minave.imagen = "imagenes/lanave_04.png"
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
		if contador_texto == 2:
			''' Recien al segundo texto comienzan a venir los asteroides '''
			# Creo una tarea para que aparezca un asteroide cada 2 segundos.
			if (self.flag[0]) == False:
				PantallaJuego.tarea1 = pilas.tareas.siempre(2, self.crear_asteroide)
				self.flag[0] = True
		if contador_texto == 31:
			''' ###  NIVEL 2 ###
			    Llegamos al segundo nivel.  Aumentamos la velocidad de los enemigos y cambiamos el fondo. '''
			# Creo una tarea para que aparezca un asteroide cada 2 segundos.
			if (self.flag[1]) == False:
				PantallaJuego.tarea1.terminar()
				tarea2 = pilas.tareas.siempre(1, self.crear_asteroide)
				PantallaJuego.velocidad_asteroides = 6
				fondo = pilas.fondos.Galaxia(dx=-3, dy=0)
				fondo.imagen = "imagenes/galaxia_02.png"
				self.flag[1] = True
		if contador_texto == 63:
			''' ###  NIVEL 3 ### '''
			if (self.flag[2]) == False:
				PantallaJuego.velocidad_asteroides = 4
				fondo = pilas.fondos.Galaxia(dx=-2, dy=0)
				fondo.imagen = "imagenes/galaxia_03.png"
				self.flag[2] = True
		if contador_texto == 102:
			''' ###  NIVEL 4 ### '''			
			if (self.flag[3]) == False:
				PantallaJuego.velocidad_asteroides = 2
				fondo = pilas.fondos.Galaxia(dx=-1, dy=0)
				fondo.imagen = "imagenes/galaxia_04.png"
				self.flag[3] = True
		if contador_texto == 240:
			''' ###  NIVEL 5 ### '''			
			if (self.flag[4]) == False:
				PantallaJuego.velocidad_asteroides = 6
				fondo = pilas.fondos.Galaxia(dx=-3, dy=0)
				fondo.imagen = "imagenes/galaxia_05.png"
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
		fondo.imagen = pilas.imagenes.cargar('imagenes/intro.png')
		fondo.z = -2

		luna = Luna(pilas);

		menu = pilas.actores.Menu([
					('iniciar juego', cargar_escena_juego),
					('salir', salir_del_juego),
				], fuente='Tentacles.ttf', y=0)
		menu.escala = 3
		menu.escala = [1]

pilas.escenas.vincular(PantallaJuego)
pilas.escenas.vincular(PantallaMenu)
pilas.escenas.PantallaMenu()

pilas.ejecutar()
