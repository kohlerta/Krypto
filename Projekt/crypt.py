#!/usr/bin/python

import prime
import math
import random

#basiert auf https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm

def egcd(a, b):
  if a == 0:
    return (b,0,1)
  else:
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def mod_invers(a, m): #a * x == 1 mod m
  g, x, y = egcd(a,m)
  if g != 1:
    raise Exception('nicht teilerfremd')
  else:
    return x % m
      

class PrivateKey(object):
  def __init__(self, p, q, n):
    self.l = (p-1) * (q-1)
    self.m = mod_invers(self.l, n)

  def __repr__(self):
    return '<PrivateKey: %s %s>' %(self.l, self.m)

  def save(self):
    priv = open(".PRIV_KEY", "w+")
    priv.write("%s %s"%(self.l, self.m))

  def load(self):
    priv = open(".PRIV_KEY", "r")
    values = priv.read().split()    
    self.l = values[0]
    self.m = values[1]

class PublicKey(object):
  def from_n(cls, n):
    return cls.n

  def __init__(self, n):
    self.n = n
    self.sq_n = n*n
    self.g = n + 1

  def save(self):
    pub = open(".PUB_KEY", "w+")
    pub.write(str(self.n))

  def load(self):
    pub = open(".PUB_KEY", "r")
    self.n = pub.read()
    self.sq_n = n*n
    self.g = n + 1

  def __repr__(self):
   return "<PublicKey: %s &s %s>"%(self.n, self.sq_n, self.g)


def generate_keypairs(bitlength):
  assert bitlength >= 16 # aufgrund von primes.generate_prime
  while True:
    p = prime.generate_prim(bitlength / 2)
    q = prime.generate_prim(bitlength / 2)
    if math.gcd(p*q, (p-1)*(q-1)) == 1:
      break;
  n = p*q
  return PrivateKey(p,q,n), PublicKey(n)

def get_value_in_Zn(pub_key): # zufaelliges r in Z/nZ*, muss ein modulares inverses haben
  while True:
    r = prime.generate_prim(int(round(math.log(pub_key.n, 2)))) # gleiche bit laenge
    if r > 0 and r < pub_key.n and math.gcd(pub_key.n, r) == 1:
      return r

def encrypt_with(pub_key, r, plain): # returns (g ** m % (n*n) ) * (r ** n % (n*n) ) % n*n
  x = pow(r, pub_key.n, pub_key.sq_n)
  return (pow(pub_key.g, plain, pub_key.sq_n) * x) % pub_key.sq_n

def encrypt(pub_key, plain):
  r = get_value_in_Zn(pub_key)
  return encrypt_with(pub_key,r,plain)

def sum(pub_key, a, b): # sum with encrypted
  return a * b % pub_key.sq_n

def add_const(pub_key, e, c): # add c als konstante
  return e * pow (pub_key.g, c, pub_key.sq_n) % pub_key.sq_n

def mul_const(pub_key, e, c): # mult e mit konstantem c
  return pow(e, c, pub_key.sq_n)

def decrypt(priv_key, pub_key, cipher): # returns ((((c ** l % (n*n))-1) // n) * m ) % n
  x = pow(cipher, priv_key.l, pub_key.sq_n) - 1
  return ((x // pub_key.n) * priv_key.m) % pub_key.n
  

