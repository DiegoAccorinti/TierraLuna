#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine
from emisorHUMO import *
import os
import juego_tierraluna
import pantalla_menu
import configuracion



# Inicializamos PILAS-ENGINE
# pasando como parámetros la resolución gráfica de la ventana y el título de la misma:

pilas = pilasengine.iniciar(ancho=900, alto=550, titulo='TierraLuna')


#pilas.cambiar_escena(pantalla_menu.PantallaMenu())

# Habilitando el Audio en PILAS: 

try:
  pilas.forzar_habilitacion_de_audio()
except AttributeError:
  print u"Omitiendo Habilitación forzada de audio, version anterior a 1.4.8".encode('utf-8')


pilas.escenas.vincular(juego_tierraluna.PantallaJuego)
pilas.escenas.vincular(pantalla_menu.PantallaMenu)
pilas.escenas.vincular(configuracion.PantallaConfig)
pilas.escenas.vincular(juego_tierraluna.PantallaFinal)

pilas.escenas.PantallaMenu()

pilas.ejecutar()
