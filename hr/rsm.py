#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
'''
Created on 18 ago 2019

@author: ernestoalvarado
'''


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
from pickletools import string1

class RMQ:

    def __init__(self, n):
        self.sz = 1
        self.inf = chr(ord("z") + 1)
        while self.sz <= n:
            self.sz <<= 1
        self.dat = [self.inf] * (2 * self.sz - 1)

    def update(self, idx, x):
            idx += self.sz - 1
            self.dat[idx] = x
            while idx > 0:
                idx = (idx - 1) >> 1
                self.dat[idx] = min(self.dat[idx * 2 + 1], self.dat[idx * 2 + 2])

    def query(self, a, b):
        return self.query_help(a, b, 0, 0, self.sz - 1)

    def query_help(self, a, b, k, l, r):
        if r < a or b < l:
            return self.inf
        elif a <= l and r <= b:
            return self.dat[k]
        else:
            return min(self.query_help(a, b, 2 * k + 1, l, (l + r) >> 1), self.query_help(a, b, 2 * k + 2, ((l + r) >> 1) + 1, r))


# XXX: https://stackoverflow.com/questions/24017363/how-to-test-if-one-string-is-a-subsequence-of-another
def is_subseq(x, y):
    it = iter(y)
    return all(any(c == ch for c in it) for ch in x)

# XXX: https://www.geeksforgeeks.org/given-two-strings-find-first-string-subsequence-second/
# Returns true if str1[] is a subsequence of str2[]. m is 
# length of str1 and n is length of str2 
def isSubSequence(string1, string2, m, n): 
    # Base Cases 
    if m == 0:    return True
    if n == 0:    return False
  
    # If last characters of two strings are matching 
    if string1[m - 1] == string2[n - 1]: 
        return isSubSequence(string1, string2, m - 1, n - 1) 
  
    # If last characters are not matching 
    return isSubSequence(string1, string2, m, n - 1) 

# Intervalo = collections.namedtuple('Intervalo', 'posiciones indice_posicion_inicial indice_posicion_final')
class Intervalo:

    def __init__(self, letra, posiciones, indice_posicion_inicial, indice_posicion_final):
        self.letra = letra
        self.posiciones = posiciones
        self.indice_posicion_inicial = indice_posicion_inicial
        self.indice_posicion_final = indice_posicion_final


# Complete the reverseShuffleMerge function below.
def reverseShuffleMerge(s):
    s = list(reversed(s))
#    indices_alfabeto = [ord(c) - ord("a") for c in ascii_lowercase]
    indices_alfabeto = reduce(lambda a, c:(a.update({c:ord(c) - ord("a")}) or a), ascii_lowercase, defaultdict(lambda:None))
    intervalos = [Intervalo(c, [], maxsize, maxsize) if c in s else None for c in ascii_lowercase]
    sequencia = array("B", [0] * len(s))
    for i, c in enumerate(s):
        intervalo = intervalos[indices_alfabeto[c]]
        if intervalo:
            intervalo.posiciones.append(i)
    for c in s:
        intervalo = intervalos[indices_alfabeto[c]]
        intervalo.indice_posicion_inicial = 0
        intervalo.indice_posicion_final = (len(intervalo.posiciones) >> 1) - 1
    logger.debug("intervalos {}".format(intervalos))
    for c in ascii_lowercase:
        intervalo = intervalos[indices_alfabeto[c]]
        if intervalo:
            intervalos_menores = intervalos[:indices_alfabeto[c]]
            try:
                intervalo_menor_mas_cercano = max(intervalos_menores, key=lambda i:i.posiciones[i.indice_posicion_final] if i else -maxsize)
            except ValueError as _:
                intervalo_menor_mas_cercano = None
            posicion_menor_mas_cercano = None
            if intervalo_menor_mas_cercano:
                posicion_menor_mas_cercano = intervalo_menor_mas_cercano.posiciones[intervalo_menor_mas_cercano.indice_posicion_final]
            else:
                posicion_menor_mas_cercano = intervalo.posiciones[0] - 1
            indice_posicion_inicial_nuevo = max(0, bisect_left(intervalo.posiciones, posicion_menor_mas_cercano))
            corrimiento = min(intervalo.indice_posicion_final + 1, indice_posicion_inicial_nuevo - intervalo.indice_posicion_inicial)
            intervalo.indice_posicion_inicial += corrimiento
            intervalo.indice_posicion_final += corrimiento
    for c in ascii_lowercase:
        intervalo = intervalos[indices_alfabeto[c]]
        if not intervalo:
            continue
        for i in range(intervalo.indice_posicion_inicial, intervalo.indice_posicion_final + 1):
            logger.debug("c {} i {}".format(c,i))
            sequencia[intervalo.posiciones[i]] = ord(c)
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
#    assert isSubSequence(list(reversed(result)), s, len(result), len(s))
    assert is_subseq(reversed(result), s)

    fptr.write(result + '\n')

    fptr.close()

