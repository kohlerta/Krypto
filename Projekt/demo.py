#!/usr/bin/python

from Crypto.Random import random
import crypt

def e_voting_simulation(kandi, cnt_voter):
  
  kand_votes = [0] * len(kandi)
  
  bits_pro_kandi = cnt_voter.bit_length()
  
  key_size = 16 # sollte eigentlich mind 1024 sein
  if len(kandi) * bits_pro_kandi > 16:
    key_size = len(kandi) * bits_pro_kandi

  prk, puk = crypt.generate_keypairs(key_size)

  init = 0
  c = crypt.encrypt(puk, init)
  d = crypt.decrypt(prk, puk, c)

  for i in range(cnt_voter):
    r = random.randint(0, len(kandi) - 1)
    kand_votes[r] += 1

    vote = 1 << (r * bits_pro_kandi)
    
    e_vote = crypt.encrypt(puk, vote)
    c = crypt.sum(puk, c, e_vote)

  d = crypt.decrypt(prk,puk, c)
  
  print("Ergebnis:")
  
  votes = [0] * len(kandi)
  mask = pow(2, bits_pro_kandi) - 1
  
  for i in range(len(kandi)):
    v = (d >> (i * bits_pro_kandi)) & mask
    votes[i] = v

  if not kand_votes == votes:
    print("error: arithmetischer fehler")

  max = 0
  for i in range(len(kandi)):
    print("%s hat %d Stimmen (plain: %d)"%(kandi[i], votes[i], kand_votes[i]))
    if votes[max] < votes[i]:
      max = i

  print("")
  print("Die meisten Stimmen hat %s"%kandi[max])


e_voting_simulation(["ÖVP","SPÖ","FPÖ", "GRÜNE", "NEOS", "EUROPA", "KPÖ"], 100)

