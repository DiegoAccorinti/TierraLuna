#!/usr/bin/env python
# -*- coding: utf-8


import pilasengine
from globales import *
from emisorHUMO import *


# Declaramos Luna. Este actor es utilizado en la presentación.
class Tierra(pilasengine.actores.Actor):
	def iniciar(self, tema):
		self.tema = tema
		url = ruta + self.tema + '/tierra.png'
		self.imagen = url
		self.x = 250
		self.y = 50
		self.escala = 1.3
		self.z = 80
	def actualizar(self):
		self.x += 0.1
		if self.x > 600:
			self.eliminar()		
			
class LunaFinal(pilasengine.actores.Actor):
	def iniciar(self, tema):
		self.tema = tema
		url = ruta + self.tema + '/luna_final.png'
		self.imagen = url
		self.x = -1250
		self.y = 50
		self.escala = 1.3
		self.z = 80
		self.transparencia = 15
	def actualizar(self):
		self.x += 0.1
		if self.x > -250:
			self.x = -250 #deja fija la luna si llegó a la mitad de la pantalla
			
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
	
	def iniciar(self, tema):
		self.tema = tema
		url = ruta + self.tema + '/ARSAT-2.png'
		self.imagen = url
		self.z = 20

	def actualizar(self):
		self.rotacion -= 0.06
		self.x += 0.6
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 600:
			self.eliminar()

class HieloEnNave(pilasengine.actores.Actor):
	
	def iniciar(self, tema, x,y):  # Hielo que aparece en la nave al chocar contra asteroide nivel 2. Desaparece a los pocos segundos.
		self.tema = tema
		url = ruta + self.tema + '/Hielo-en-nave.png'
		self.imagen = url
		self.x = x
		self.y = y
		self.z = -51
		self.transparencia = 0
		self.transparencia = [100],4
		
	def actualizar(self):
		if self.transparencia == 100: # Elimino el objeto cuando se hace totalmente transparente.
			self.eliminar()

class FuegoEnNave(pilasengine.actores.Actor):
	
	def iniciar(self, tema, x,y):  # Fuego que aparece en la nave al chocar contra asteroide nivel 5. Desaparece a los pocos segundos.
		self.tema = tema
		url = ruta + self.tema + '/Fuego-en-nave.png'
		self.imagen = url
		self.x = x
		self.y = y
		self.z = -51
		self.transparencia = 0
		self.transparencia = [100,20,80,20,100],1
		
	def actualizar(self):
		if self.transparencia == 100: # Elimino el objeto cuando se hace totalmente transparente.
			self.eliminar()

			
class HUDArsat(pilasengine.actores.Actor):
	
	def iniciar(self, tema):
		self.tema = tema
		url = ruta + self.tema + '/ARSAT-2-HUD.png'
		self.imagen = url
		self.x = -600
		self.y = self.pilas.azar(-50, 150)
		self.escala = 1
		self.z = 21

	def actualizar(self):
		self.x += 0.6
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 600:
			self.eliminar()
		
class Nave(pilasengine.actores.Actor):
	
	def iniciar(self, mitema, pilotoAutomatico):
		# La clase Nave recibe todos los datos del tema para poder reiniciar PantallaMenu 
		# al morir, por eso tema_sprites es mitema[1]
		
		self.mitema = mitema 
		
		self.grupo_cubitos = self.pilas.actores.Grupo()
		self.grupo_fuegos = self.pilas.actores.Grupo()
		self.pilotoAutomatico = pilotoAutomatico
		self.estadoPilotoAutomatico = "subiendo"
		
		url = ruta + self.mitema[1] + '/lanave.png'
		self.imagen = url
		self.z = -50
		self.choques = 0
		#Crea un objeto asociado que emite particulas
		self.emisor = EmisorHUMO(self.pilas, 0, 0)
		url = ruta + self.mitema[1] + '/humo.png'
		self.emisor.imagen_particula = self.pilas.imagenes.cargar_grilla(url)
		self.emisor.constante = True
		if self.mitema[1] == "/temas/steampunk/sprites":
			self.emisor.composicion = "negro"
			self.emisor.x_min = 90
			self.emisor.y_min = 80
			self.emisor.frecuencia_creacion = 0.08
			
		else:
			self.emisor.composicion = "blanco"
			self.emisor.x_min = 171
			self.emisor.y_min = 2
			self.emisor.frecuencia_creacion = 0.05
		self.emisor.duracion = 2
		self.emisor.vida = 3
		self.emisor.aceleracion_x_min = 36
		self.emisor.aceleracion_x_max = 50
		self.emisor.transparencia_min = 30
		self.emisor.transparencia_max = 50
		
		#self.nave_energia = self.pilas.actores.Energia(color_relleno = self.pilas.colores.verde)
		self.nave_energia = self.pilas.actores.Energia(progreso = 100, color_relleno = self.pilas.colores.Color(56,255,75),
	ancho=190, alto=20, con_sombra = False, con_brillo = False)
		self.nave_energia.x = 250
		self.nave_energia.y = 240
		self.nave_energia.z = 0

	def pilotoAutomaticoActivo(self):
		if self.estadoPilotoAutomatico == "subiendo":
			self.y += 1
			if self.x < 70 : self.x += 1
			if self.x > 70 : self.x -= 1	
			if self.y > 100:
				self.estadoPilotoAutomatico = "bajando"

		if self.estadoPilotoAutomatico == "bajando":
			self.y -= 1
			if self.x < 70 : self.x += 1
			if self.x > 70 : self.x -= 1			
			if self.y < -100:
				self.estadoPilotoAutomatico = "subiendo"
				
				

	def actualizar(self):
		
		if self.pilotoAutomatico :
			self.pilotoAutomaticoActivo()
		if self.grupo_cubitos:
			self.habilidades.MovimientoDeNave.velocidad_maxima = 1 # Si está congelada,  baja la velocidad.
		else:
			self.habilidades.MovimientoDeNave.velocidad_maxima = 3 # Esto debería hacerse de otra manera para que no se ejecute esta línea constantemente.
				
				
	def choque(self, nave, asteroide):
			
			asteroide.estallar(asteroide.x, asteroide.y, asteroide.tipo, nave)
			
			self.pilas.camara.vibrar(3, 0.5)
			self.choques += 1
			self.valor = self.nave_energia.progreso - (100/11)
			self.nave_energia.progreso = [self.valor]
			if int(self.nave_energia.progreso) in range(20, 40):
				self.nave_energia.color_relleno = self.pilas.colores.Color(230,200,0) #amarillo
			elif self.nave_energia.progreso <= 20:
				self.nave_energia.color_relleno = self.pilas.colores.Color(230,49,0) # rojo 
			if self.choques == 2:
				self.imagen = ruta + self.mitema[1] + '/lanave_01.png'
				self.emisor.frecuencia_creacion = 0.07
			if self.choques == 4:
				self.imagen = ruta + self.mitema[1] + '/lanave_02.png'
				self.emisor.frecuencia_creacion = 0.10
			if self.choques == 7:
				self.imagen = ruta + self.mitema[1] + '/lanave_03.png'
				self.emisor.frecuencia_creacion = 0.13
			if self.choques == 9:
				self.imagen = ruta + self.mitema[1] + '/lanave_04.png'
				self.emisor.eliminar()
				self.rotacion = [360], 2
			if self.choques == 11:	
				self.nave_energia.progreso = [2]
			if self.choques == 12: # MUERE
				self.pilas.camara.x = self.x
				self.pilas.camara.y = self.y
				self.morir() #Llamar a astronauta flotando o coso.
				self.eliminar()
				for cubito in self.grupo_cubitos:  # al morir puede estar congelada más de una vez, por eso elimino todos los "cubitos" que existan.
					cubito.eliminar()
				for fuego in self.grupo_fuegos:  # al morir puede estar incendiada más de una vez, por eso elimino todos los "fuego" que existan.
					fuego.eliminar()
				
			mensajeNeo = [False, False]
			print("Choques = " + str(self.choques))
			if (self.choques == 8) and (mensajeNeo[0] == False):
				os.system('clear')
				print("Despierta, Neo.")
				print("La Matrix te tiene.")
				print("Sigue al conejo blanco.")
				print("Toc toc, Neo.")
				mensajeNeo[0] = True
			if (self.choques == 9) and (mensajeNeo[1] == False):
				os.system('clear')
				print("Choques = " + str(self.choques))
				mensajeNeo[1] = True
				
	def choque_repara(self, nave, estacion_reparacion):
			nave.reparar()
			#estacion_reparacion.eliminar()
			estacion_reparacion.reparar_nave(nave.x, nave.y)
			
	def morir(self):
			self.perdido = Astronauta(self.pilas, tema=self.mitema[1]);
			self.pilas.camara.escala = [1.2, 1.5, 1]
			self.perdido.escala = [1, 0.4]
			self.texto_personalizado3 = self.pilas.actores.Texto(u'por miles de años flotarás exánime en el espacio · presiona ESPACIO', magnitud=18, fuente= url_fuente2, y= -230, x = 0)
			self.texto_personalizado3.color =  self.pilas.colores.blanco
			self.pilas.eventos.pulsa_tecla.conectar(self.al_pulsar_tecla)		

	def reparar(self):
		if self.choques > 3:
			self.choques -=3
			self.valor = self.nave_energia.progreso + 3 * 100/11
			self.nave_energia.progreso = [self.valor]
			
		else:
			self.choques = 0
			self.nave_energia.progreso = [100]
	
	def congelar(self): # Cuando la nave choca contra un asteroide nivel 2,  se congela.
			self.cubito = HieloEnNave(self.pilas, tema=self.mitema[1], x=self.x, y=self.y)
			self.cubito.imitar(self)
			self.grupo_cubitos.agregar(self.cubito)  # agrego el nuevo hielo de la nave a un grupo.

	def incendiar(self): # Cuando la nave choca contra un asteroide nivel 2,  se congela.
			self.fuego = FuegoEnNave(self.pilas, tema=self.mitema[1], x=self.x, y=self.y)
			self.fuego.imitar(self)
			self.grupo_fuegos.agregar(self.fuego)  # agrego el nuevo fuego de la nave a un grupo.
	

	def al_pulsar_tecla(self, tecla):
			global flag
			if tecla.codigo == 32:
				flag = [False, False, False, False, False]
				self.pilas.escenas.PantallaMenu(self.mitema[0], self.mitema[1], self.mitema[2], self.mitema[3] )

class Astronauta(pilasengine.actores.Actor):

	def iniciar(self, tema):
		self.tema = tema
		url = ruta + self.tema + '/astronauta.png'
		self.imagen = url

	def actualizar(self):
		self.rotacion += 1

class Asteroide(pilasengine.actores.Actor):

	def iniciar(self, tema, tipo):
		self.tema = tema
		self.tipo = tipo

		if self.tipo == "uno":
			self.imagen = ruta + self.tema + '/asteroide.png'
			self.giro = 1
			self.velocidad = 3
		if self.tipo == "dos":
			self.imagen = ruta + self.tema + '/asteroide2.png'
			self.giro = 3
			self.velocidad = 6

		if self.tipo == "tres":
			self.imagen = ruta + self.tema + '/asteroide3.png'
			self.giro = 2
			self.velocidad = 4
		if self.tipo == "cuatro":
			self.imagen = ruta + self.tema + '/asteroide4.png'
			self.giro = -2
			self.velocidad = 2
		if self.tipo == "cinco":
			self.imagen = ruta + self.tema + '/asteroide5.png'
			self.giro = 3
			self.velocidad = 6
		self.escala = 0.3
		self.x = -500
		self.y = self.pilas.azar(-300, 300)
		self.z = self.pilas.azar(-100, 10)

	def actualizar(self):
		self.rotacion += self.giro
		self.x += self.velocidad
		# Elimina el objeto cuando sale de la pantalla.
		if self.x > 500:
			self.eliminar()
			
			
	def estallar(self, x, y, tipo, nave):
		if tipo == "uno":  # El asteroide estalla en pedazos.
			self.fragmentos = [Fragmento(self.pilas, x, y, tema=self.tema), Fragmento(self.pilas, x, y, tema=self.tema), Fragmento(self.pilas, x, y, tema=self.tema), Fragmento(self.pilas, x, y, tema=self.tema)] # Es necesario explicitar la lista por un bug en pilas que crashea si se clona con un parametro.
			self.eliminar()
		if tipo == "dos": # El asteroide  congela la nave.
			nave.congelar()
			#self.eliminar()
		if tipo == "cinco": # El asteroide prende fuego la nave
			nave.incendiar()
			#self.eliminar()

class Fragmento(pilasengine.actores.Actor):
		def iniciar(self, x, y, tema):
			self.x = x
			self.y = y
			self.tema = tema
			self.imagen = ruta + self.tema + '/fragmento.png'
			self.giro = 1
			velocidades = [-4,-3,-2,-1,1,2,3,4]
			self.velocidadX = velocidades[self.pilas.azar(0, 7)]
			self.velocidadY = velocidades[self.pilas.azar(0, 7)]
			self.transparencia = 0.0
			self.escala = 0.1 * self.pilas.azar(1, 3)
		def actualizar(self):
			self.rotacion += self.giro
			self.x += self.velocidadX
			self.y += self.velocidadY
			self.transparencia += 0.5
			if self.transparencia > 100.0:
				self.eliminar()
			# Elimina el objeto cuando sale de la pantalla.
			if self.x > 500 or self.x < -500:
				self.eliminar()
			elif self.y > 400 or self.y < -400:
				self.eliminar()
			
class Reparacion(pilasengine.actores.Actor):

	def iniciar(self, tema):
		self.tema = tema
		url = ruta + self.tema + '/reparacion_bot.png'
		self.imagen = url
		self.x = -500
		self.z = -51
		self.velocidad = 0.3
		self.delta_escala = 0.001
		self.escala = 0.5
		
	def reparar_nave(self, x, y):
		self.transparencia = [100],1.5
		url = ruta + self.tema + '/reparacion_bot_ojo_rojo.png'
		self.imagen = url
		
	def actualizar(self):
		self.x += self.velocidad
		self.escala += self.delta_escala
		if self.escala > 0.55 or self.escala < 0.5:
			self.delta_escala = -self.delta_escala
			#deberia agrandar o achicar entre 0.6 y 1
		if self.transparencia == 100:  # si la transparencia es total,  elimino el actor.
			self.eliminar()
