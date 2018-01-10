# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
import math

from pilasengine import habilidades


class MovimientoDeNave(habilidades.Habilidad):
    """Hace que un actor cambie de posición con pulsar el teclado."""

    def iniciar(self, receptor, control=None, velocidad_maxima=4,
                aceleracion=0.7, deceleracion=0.1):
        """Inicializa la habilidad.

        :param receptor: Referencia al actor que aprenderá la habilidad.
        :param control: Control al que va a responder para mover el Actor.
        :param velocidad_maxima: Velocidad maxima en pixeles a la que se moverá
                                 el Actor.
        :param aceleracion: Indica lo rapido que acelera el actor hasta su
                            velocidad máxima.
        :param deceleracion: Indica lo rapido que decelera el actor hasta parar.
        """

        super(MovimientoDeNave, self).iniciar(receptor)

        if control is None:
            self.control = self.pilas.escena_actual().control
        else:
            self.control = control

        self.velocidad_y = 0
        self.velocidad_x = 0
        self.velocidad_maxima = velocidad_maxima
        self.deceleracion = deceleracion
        self.aceleracion = aceleracion

    def actualizar(self):
        if self.control.arriba:
            self.velocidad_y += self.aceleracion
        elif self.control.abajo:
            self.velocidad_y -= self.aceleracion
        elif abs(self.velocidad_y - self.deceleracion) < 0.5:
            self.velocidad_y = 0
        else:
            self.velocidad_y -= math.copysign(self.deceleracion,
                                              self.velocidad_y - self.deceleracion)

        if abs(self.velocidad_y) > self.velocidad_maxima:
            self.velocidad_y = math.copysign(self.velocidad_maxima,
                                             self.velocidad_y)

        if self.control.izquierda:
            self.velocidad_x -= self.aceleracion
        elif self.control.derecha:
            self.velocidad_x += self.aceleracion
        elif abs(self.velocidad_x - self.deceleracion) < 0.5:
            self.velocidad_x = 0
        else:
            self.velocidad_x -= math.copysign(self.deceleracion,
                                              self.velocidad_x - self.deceleracion)

        if abs(self.velocidad_x) > self.velocidad_maxima:
            self.velocidad_x = math.copysign(self.velocidad_maxima,
                                             self.velocidad_x)

        self.receptor.x += self.velocidad_x
        self.receptor.y += self.velocidad_y
