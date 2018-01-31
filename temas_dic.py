#!/usr/bin/env python
# -*- coding: utf-8
'''
Cada Tema debe informar qué elementos incluye para personalizar. 
Aquellos elementos no incluidos serán reemplazados por los del tema "Default"
Los temas se guardan en un diccionario de listas con los paramtros de cada tema.
Las listas se forma con "Titulo del tema", "nombre de la carpeta", incluye sprites [bool], incluye fondos [bool], incluye textos [bool]
'''


temas = {}

temas['original']=['Original', True, True, True, u"Tierra-Luna, tema original creado por Diego Accorinti"]
temas['steampunk']=['Steampunk', True, True, False, u"Una variante Steampunk, orientada a la difusión de la literatura ciencia ficción del siglo XIX. Creada por Claudio Andaur."]
#temas['interior']=['Viaje Interior', True, True, True]
#temas['conurbania']=['Conurbania', False, False, False]

