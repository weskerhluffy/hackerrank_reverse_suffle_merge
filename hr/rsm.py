#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3
'''
Created on 18 ago 2019

@author: ernestoalvarado
'''

# XXX: https://www.hackerrank.com/challenges/reverse-shuffle-merge/problem

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
from collections import defaultdict, Counter
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


#  XXX: https://stackoverflow.com/questions/24017363/how-to-test-if-one-string-is-a-subsequence-of-another
def is_subseq(x, y):
    it = iter(y)
    return all(any(c == ch for c in it) for ch in x)


#  XXX: https://www.geeksforgeeks.org/given-two-strings-find-first-string-subsequence-second/
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
        self.restantes = {}


# Complete the reverseShuffleMerge function below.
def reverseShuffleMerge(s):
    s = list(reversed(s))
    s_len = len(s)
    indices_alfabeto = reduce(lambda a, c:(a.update({c:ord(c) - ord("a")}) or a), ascii_lowercase, defaultdict(lambda:None))
    intervalos = [Intervalo(c, [], maxsize, maxsize) if c in s else None for c in ascii_lowercase]
#    indices_alfabeto = [ord(c) - ord("a") for c in ascii_lowercase]
    r = []
    histograma = Counter(s)
    for c in histograma:
        histograma[c] >>= 1
        
    rmq = RMQ(s_len)
    i = s_len - 1
    while i >= 0:
        c = s[i]
        intervalo = intervalos[indices_alfabeto[c]]
        if intervalo:
            intervalo.posiciones.append(i)
            intervalo.restantes[i] = len(intervalo.posiciones)
        rmq.update(i, c)
        i -= 1
    
    histograma1 = {}
    i = s_len - 1
    while i >= 0 and (not histograma1 or not all(map(lambda c:c in histograma1 and histograma1[c] == histograma[c], histograma))):
        c = s[i]
        conteo = histograma1.setdefault(c, 0) 
        if (conteo + 1) <= histograma[c]:
            histograma1[c] = conteo + 1
#        histograma1[c] = min(conteo+ 1, histograma[c])
        i -= 1
    j = i
    i = 0
    while any(histograma.values()):
        c = rmq.query(i, j)
        while i < s_len and s[i] != c:
            i += 1
        i = min(s_len - 1, i + 1)
#        j = min(s_len - 1, j + 1)
        histograma[c] = max(0, histograma[c] - 1)
        print("i {} j {} c {}". format(i, j, c))
        if not histograma[c]:
            for k in intervalos[indices_alfabeto[c]].posiciones:
                s[k] = rmq.inf
                rmq.update(k, rmq.inf)
        while j < s_len and (s[j] == rmq.inf or intervalos[indices_alfabeto[s[j]]].restantes[j] > histograma[s[j]]):
            j += 1
        r.append(c)
        
    return "".join(r)
        

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

