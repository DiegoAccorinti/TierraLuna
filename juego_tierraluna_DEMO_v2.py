#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine

from globales import *
from objetos import *
from fondos import *
# Pantallas adicionales
from pantallas_juego import *
from juego_tierraluna import *
# LOS TEXTOS
# Le pido la biblioteca de textos contenido en textos.py
from textos import textos
from movimiento_de_nave import MovimientoDeNave

# Esta escena es una demo. Hereda los métodos de PantallaJuego y modifica el comportamiento de la nave
# Es lo que comenzará cuando elijamos "Demo" en el menú principal


class PantallaDemo(PantallaJuego):
	
	def iniciar(self, tema_actual, tema_sprites, tema_fondos, tema_textos):

		global contador_texto
		global contador_choques
		global flag
		global flagEspeciales
		global pausa
		self.tema_sprites = tema_sprites
		self.tema_fondos = tema_fondos
		self.tema_textos = tema_textos
		self.tema_actual = tema_actual
		self.mitema = [self.tema_actual, self.tema_sprites, self.tema_fondos, self.tema_textos]
		pausa = False
		flag = [False, False, False, False, False]
		flagEspeciales = [False]
		self.crear_grupo_enemigos()
		
		self.pilas.eventos.pulsa_tecla.conectar(self.pausar_juego)
		self.crearFondosNivel(lvl="NIVEL1", tema=self.tema_fondos )
		tierra = Tierra(self.pilas, tema=self.tema_sprites)
		contador_texto = 0

		self.iniciar_musica()

		self.texto_personalizado = self.pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -230, ancho = 230)
		self.sombra_texto_personalizado = self.pilas.actores.Texto('', magnitud=31, fuente= url_fuente, y= -233, x=1, ancho = 230)
		self.sombra_texto_personalizado.color = self.pilas.colores.negro
		self.sombra_texto_personalizado.z = 4

		self.minave = Nave(self.pilas, mitema= self.mitema, pilotoAutomatico = True);
				
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

		self.minave.aprender(MovimientoDeNave)
		self.minave.aprender(self.pilas.habilidades.LimitadoABordesDePantalla)
		
		# Creo una tarea para que aparezcan los textos, cada 5 segundos.
		self.tareaMostrarTextos = self.pilas.tareas.siempre(5, self.imprimir_texto)		

		# Creo un control de coliciones para saber cuando perdes  # SIN COLISIONES PORQUE ES DEMO
		#self.pilas.colisiones.agregar(self.minave, self.enemigos, self.minave.choque)

		#Elimino los límites laterales y la gravedad
		self.pilas.fisica.gravedad_x = 0
		self.pilas.fisica.gravedad_y = 0
		self.pilas.fisica.eliminar_paredes()
		self.pilas.fisica.eliminar_techo()
		self.pilas.fisica.eliminar_suelo()

	# Cuando pierdo, si presiono una tecla termina el juego y se cierra
			

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
				PantallaDemo.tareaAsteroides = self.pilas.tareas.siempre(2, self.crear_asteroide, "uno", 150)
				flag[0] = True
				cambio_nivel(1, "DEMO")
				#r1 = Reparacion(self.pilas) #Crea puesto de reparacion

		if contador_texto == 4: 
			''' ###  NIVEL 2 ###
			Llegamos al segundo nivel.  Aumentamos la velocidad de los enemigos y cambiamos el fondo. '''
			# Creo una tarea para que aparezca un asteroide cada 1.5 segundos.
			if (flag[1]) == False:
				print "NIVEL 2"
				PantallaDemo.tareaAsteroides.terminar()
				PantallaDemo.tareaAsteroides = self.pilas.tareas.siempre(1.5, self.crear_asteroide, "dos", 110) # A "crear_asteroide" le paso el tipo que tiene que crear y el radio de colisión.
				self.crearFondosNivel(lvl="NIVEL2", tema=self.tema_fondos)
				cambio_nivel(2, "DEMO")
				flag[1] = True

		if contador_texto == 8: 
			''' ###  NIVEL 3 ### '''
			if (flag[2]) == False:
				print "NIVEL 3"
				PantallaDemo.tareaAsteroides.terminar()

				PantallaDemo.tareaAsteroides = self.pilas.tareas.siempre(1.5, self.crear_asteroide, "tres", 150)
				self.crearFondosNivel(lvl="NIVEL3", tema=self.tema_fondos)				
				cambio_nivel(3, "DEMO")
				flag[2] = True
		if contador_texto == 12: 
			''' ###  NIVEL 4 ### '''
			if (flag[3]) == False:
				print "NIVEL 4"
				PantallaDemo.tareaAsteroides.terminar()
				PantallaDemo.tareaAsteroides = self.pilas.tareas.siempre(2, self.crear_asteroide, "cuatro", 150)
				self.crearFondosNivel(lvl="NIVEL4", tema=self.tema_fondos)
				cambio_nivel(4, "DEMO")
				flag[3] = True
		if contador_texto == 16: 
			''' ###  NIVEL 5 ### '''
			if (flag[4]) == False:
				print "NIVEL 5"
				PantallaDemo.tareaAsteroides.terminar()
				PantallaDemo.tareaAsteroides = self.pilas.tareas.siempre(1.5, self.crear_asteroide, "cinco", 150)
				self.crearFondosNivel(lvl="NIVEL5", tema=self.tema_fondos)
				cambio_nivel(5, "DEMO")
				flag[4] = True

		if contador_texto == 20:
			flag = [False, False, False, False, False]
			contador_texto = 1
			PantallaDemo.tareaAsteroides.terminar()
			
				
				
		''' Eventos únicos especiales durante el juego '''	

		# paso de ARSAT-2
		if contador_texto == 6:
			if flagEspeciales[0] == False:
				hudarsat = HUDArsat(self.pilas, tema=self.mitema[1])
				arsat = Arsat(self.pilas, tema=self.mitema[1])
				arsat.x = hudarsat.x
				arsat.y = hudarsat.y
				flagEspeciales[0] = True


