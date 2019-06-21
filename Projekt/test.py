#!/usr/bin/python

import crypt

def to_ascii_list(text):
  l = list()
  for c in str(text):
    l.append(ord(c))
  return l

def from_ascii_list(lis):
  s = ""
  for c in lis:
    s = s + chr(c)
  return s

val_1 = 687468
val_2 = 367
val_3 = 9876452
val_4 = 1346



private_key, public_key = crypt.generate_keypairs(1024)

c_1 = crypt.encrypt(public_key, val_1)
c_3 = crypt.encrypt(public_key, val_3)

c_sum = crypt.sum(public_key, c_1, c_3)
c_add = crypt.add_const(public_key, c_1, val_2)
c_mul = crypt.mul_const(public_key, c_1, val_4)

print("sum %s = %s" % (val_1 + val_3, crypt.decrypt(private_key, public_key, c_sum)))
print("add const %s = %s" % (val_1 + val_2, crypt.decrypt(private_key, public_key, c_add)))
print("mul const %s = %s" % (val_1 * val_4, crypt.decrypt(private_key, public_key, c_mul)))
