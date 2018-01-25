#!/usr/bin/env python
# -*- coding: utf-8

import os

# Definimos la ruta hasta los archivos de las dos tipografías que utilizaremos en el juego. 

ruta = os.path.dirname(os.path.realpath(__file__))
url_fuente = ruta + '/Tentacles.ttf'
url_fuente2 = ruta + '/Oswald-Regular.ttf'


#Valores iniciales para tema, estas variables deberian ser sobreescritas por la configuracion 
tema_sprites_init = '/temas/original/sprites'
tema_fondos_init = '/temas/original/fondos'
tema_textos_init = '/temas/original'

tema_actual_init = 'original' # El primer tema disponible es el inicial
