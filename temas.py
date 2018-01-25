#!/usr/bin/env python
# -*- coding: utf-8
'''
Cada Tema debe informar qué elementos incluye para personalizar. 
Aquellos elementos no incluidos serán reemplazados por los del tema "Default"
Los temas se guardan en un diccionario de listas con los paramtros de cada tema.
Las listas se forma con "Titulo del tema", "nombre de la carpeta", incluye sprites [bool], incluye fondos [bool], incluye textos [bool]
'''


temas = {}

temas['original']=['Original', True, True, True]
temas['steampunk']=['Steampunk', True, True, False]
#temas['interior']=['Viaje Interior', True, True, True]
#temas['conurbania']=['Conurbania', False, False, False]

