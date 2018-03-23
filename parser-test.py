#!/usr/bin/env python
# -*- coding: utf-8

import codecs

#textos = []
archivo = codecs.open("aventura-test.txt", "r", "utf8")

#textos = archivo.readlines()
lineas = [line.rstrip('\n') for line in archivo]

for l in lineas:
	if l <> "<PAUSA>" and l <> "<EVENTO>" and l <> "<NIVEL>":
		print l
