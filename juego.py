# -*- coding: utf-8
import pilasengine
from emisorHUMO import * 

pilas = pilasengine.iniciar(ancho=900, alto=550, titulo='De la tierra a la luna')

class PantallaJuego(pilasengine.escenas.Escena):

    def iniciar(self):

		puntaje = pilas.actores.Puntaje(280, 200, color=pilas.colores.blanco, texto="0")
		choques = pilas.actores.Puntaje(600, 600, color=pilas.colores.blanco, texto="0") # uso 600,600 para que no se vea.
		fondo = pilas.fondos.Galaxia(dx=-2, dy=0)


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

		c2 = pilas.fisica.Circulo(minave.x, minave.y, 100, restitucion=0.1, amortiguacion=0.5)
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

		#defino un grupo de enemigos
		enemigos = pilas.actores.Grupo()

		def crear_asteroide():
			#creo el actor enemigo
			asteroide = Asteroide(pilas);
			#creo un objeto para la física
			c1 = pilas.fisica.Circulo(asteroide.x, asteroide.y, 100, restitucion=1, amortiguacion=2)
			asteroide.imitar(c1)
			#lo agrego al grupo
			enemigos.agregar(asteroide)


		# Creo una tarea para que aparezca un asteroide cada 2 segundos.
		pilas.tareas.siempre(2, crear_asteroide)  

		def nave_choco():#Cuando un asteroide choca nave
			#minave.y = [minave.y +5, minave.y -5],0.2
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
				minave.rotacion = [360], 4
			if choques.obtener() == 11:
				pilas.camara.x = minave.x
				pilas.camara.y = minave.y
				perdido = Astronauta(pilas);
				minave.eliminar()
				pilas.camara.escala = [1.2, 1.5, 1]
				perdido.escala = [1, 0.7]
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
		fondo = pilas.fondos.Fondo()
		fondo.imagen = pilas.imagenes.cargar('imagenes/intro.png')
		
		menu = pilas.actores.Menu(
				[
					('iniciar juego', cargar_escena_juego),
					('salir',  salir_del_juego),
				])
		menu.escala = 2
		menu.escala = [1]

pilas.escenas.vincular(PantallaJuego)
pilas.escenas.vincular(PantallaMenu)
pilas.escenas.PantallaMenu()

pilas.ejecutar()
