#!/usr/bin/python

import random
import sys

# Miller-Rabin-Test siehe https://de.wikipedia.org/wiki/Miller-Rabin-Test#
# pseudo-code von dort.

def miller_rabin_test(n, a): #n ungerade, 1 < a < n-1
  m = n-1
  d = m >> 1
  e = 1
  while not d & 1:
    d >>= 1
    e = e+1
  p = a
  q = a
  while d >> 1:
    d = d >> 1
    q = q*q % n
    if d & 1:
      p = p*q % n
  if p == 1 or q == m:
    return True
  while e - 1 > 0:
    e = e - 1
    p = p*p % n
    if p == m:
      return True
    if p <= 1:
      break
  return False

kleinePrimzahlen = (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103)

#helpers
def print_isPrim(zahl):
  if miller_rabin_test(zahl,random.randrange(2,zahl-1)):
    print ("%d prim"%zahl)
  else:
    print ("%d nicht prim"%zahl)

def anzahl_versuche(zahl):
  return int(max(40, zahl.bit_length()))

def vermutlich_prim(zahl):
  if zahl == 1:
    return True
  for i in kleinePrimzahlen:
    if zahl == i:
      return True
    if zahl % i == 0:
      return False
  for i in range(anzahl_versuche(zahl)):
    if not miller_rabin_test(zahl, random.randrange(2, zahl-1) | 1):
      return False
  return True


def generate_prim(bitlength):
  assert bitlength >= 8  #muss mind 8 bits lang sein sonst assertionerror
  
  while True:
    zahl = random.randrange(int(2 ** (bitlength-1) + 1), int(2 ** bitlength)) | 1
    if vermutlich_prim(zahl):
      return zahl

