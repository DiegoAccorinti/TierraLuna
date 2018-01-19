#!/usr/bin/env python
# -*- coding: utf-8

import os

# Definimos la ruta hasta los archivos de las dos tipografías que utilizaremos en el juego. 

ruta = os.path.dirname(os.path.realpath(__file__))
url_fuente = ruta + '/Tentacles.ttf'
url_fuente2 = ruta + '/Oswald-Regular.ttf'


#Valores iniciales para tema, estas variables deberian ser sobreescritas por la configuracion 
tema_sprites = '/temas/original'
tema_fondos = '/temas/original'
tema_textos = '/temas/original'

tema_actual = 'original' # El primer tema disponible es el inicial
