#!/usr/bin/env python
# -*- coding: utf-8
import pilasengine
from globales import *
from emisorHUMO import *
from pantalla_config import *
from pantalla_menu import *
from juego_tierraluna import *

# Inicializamos PILAS-ENGINE
# pasando como parámetros la resolución gráfica de la ventana y el título de la misma:

pilas = pilasengine.iniciar(ancho=900, alto=550, titulo='TierraLuna')


# Habilitando el Audio en PILAS: 

try:
  pilas.forzar_habilitacion_de_audio()
except AttributeError:
  print u"Omitiendo Habilitación forzada de audio, version anterior a 1.4.8".encode('utf-8')


pilas.escenas.vincular(PantallaJuego)
pilas.escenas.vincular(PantallaMenu)
pilas.escenas.vincular(PantallaConfig)
pilas.escenas.vincular(PantallaFinal)
pilas.escenas.PantallaMenu()

pilas.ejecutar()
