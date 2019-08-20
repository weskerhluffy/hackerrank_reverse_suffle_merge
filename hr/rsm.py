'''
Created on 18 ago 2019

@author: ernestoalvarado
'''

#!/bin/python3

import math
import os
import random
import re
import sys
import logging

import collections
from string import ascii_lowercase
from sys import maxsize
from functools import reduce
from collections import defaultdict
from _bisect import bisect_left
from array import array


# Intervalo = collections.namedtuple('Intervalo', 'posiciones indice_posicion_inicial indice_posicion_final')
class Intervalo:

    def __init__(self, posiciones, indice_posicion_inicial, indice_posicion_final):
        self.posiciones = posiciones
        self.indice_posicion_inicial = indice_posicion_inicial
        self.indice_posicion_final = indice_posicion_final


# Complete the reverseShuffleMerge function below.
def reverseShuffleMerge(s):
    s = list(reversed(s))
    alfabeto = list(reversed(ascii_lowercase))
#    indices_alfabeto = [ord(c) - ord("a") for c in ascii_lowercase]
    indices_alfabeto = reduce(lambda a, c:(a.update({c:ord(c) - ord("a")}) or a), ascii_lowercase, defaultdict(lambda:None))
    intervalos = [Intervalo([], maxsize, maxsize) if c in s else None for c in ascii_lowercase]
    sequencia = array("B", [0] * len(alfabeto))
    for i, c in enumerate(s):
        intervalo = intervalos[indices_alfabeto[c]]
        if intervalo:
            intervalo.posiciones.append(i)
    for c in s:
        intervalo = intervalos[indices_alfabeto[c]]
        intervalo.indice_posicion_inicial = 0
        intervalo.indice_posicion_final = (len(intervalo.posiciones) >> 1) - 1
    logger.debug("intervalos {}".format(intervalos))
    for c in alfabeto:
        intervalo = intervalos[indices_alfabeto[c]]
        if intervalo:
            intervalos_mayores = intervalos[indices_alfabeto[c] + 1:]
            if not any(map(lambda intervalo_tmp:intervalo_tmp  and intervalo_tmp.indice_posicion_inicial <= intervalo.indice_posicion_inicial <= intervalo_tmp.indice_posicion_final, intervalos_mayores)):
                try:
                    intervalo_mayor_mas_cercano = min(intervalos_mayores, key=lambda i:i.indice_posicion_inicial if i else maxsize)
                except ValueError as _:
                    intervalo_mayor_mas_cercano = None
                posicion_mayor_mas_cercano = None
                if intervalo_mayor_mas_cercano:
                    posicion_mayor_mas_cercano = intervalo_mayor_mas_cercano.posiciones[intervalo_mayor_mas_cercano.indice_posicion_inicial]
                else:
                    posicion_mayor_mas_cercano = intervalo.posiciones[-1] + 1
                indice_posicion_final_nuevo = max(0, bisect_left(intervalo.posiciones, posicion_mayor_mas_cercano) - 1)
                corrimiento = max(0, indice_posicion_final_nuevo - intervalo.indice_posicion_final)
                intervalo.indice_posicion_inicial += corrimiento
                intervalo.indice_posicion_final += corrimiento
    for c in ascii_lowercase:
        intervalo = intervalos[indices_alfabeto[c]]
        if not intervalo:
            continue
        for i in range(intervalo.indice_posicion_inicial, intervalo.indice_posicion_final + 1):
            sequencia[i] = ord(c)
    return "".join(map(chr, filter(lambda c:c, sequencia)))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s  %(levelname)-10s %(processName)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %(name)s %(message)s')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.ERROR)
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    if "STDIN" in os.environ:
        f = open(os.environ["STDIN"], "r")
        input_fn = f.readline
    else:
        input_fn = input
    s = input_fn().strip()

    result = reverseShuffleMerge(s)

    fptr.write(result + '\n')

    fptr.close()
