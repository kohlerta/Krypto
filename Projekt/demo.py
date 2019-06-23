#!/usr/bin/python

from config import * 
import random
import crypt
import math

def e_voting_simulation():
  
  plain_votes = [0] * CNT_VOTEE
  
  bitlength_cnt_voter = CNT_VOTER.bit_length()

  priv, pub = crypt.generate_keypairs(KEY_SIZE)

  init = 0
  c = crypt.encrypt(pub, init)
  d = crypt.decrypt(priv, pub, c)

  for i in range(CNT_VOTER): # pro voter an random votee plus eine stimme
    r = random.randint(0, CNT_VOTEE - 1)
    plain_votes[r] += 1

    vote = 1 << (r * bitlength_cnt_voter)
    
    e_vote = crypt.encrypt(pub, vote)
    c = crypt.sum(pub, c, e_vote)

  d = crypt.decrypt(priv, pub, c)
  
  print("Ergebnis:")
  
  votes = [0] * CNT_VOTEE
  mask = pow(2, bitlength_cnt_voter) - 1 
  
  for i in range(CNT_VOTEE):
    v = (d >> (i * bitlength_cnt_voter)) & mask
    votes[i] = v

  if not plain_votes == votes:
    print("error: arithmetischer fehler")

  max = 0
  for i in range(CNT_VOTEE):
    print("%s hat %.2f Prozent (Stimmen: %d)"%(VOTEE[i], round(votes[i]/CNT_VOTER*100,2), votes[i]))
    if votes[max] < votes[i]:
      max = i

  print("")
  print("Die meisten Stimmen hat %s"%VOTEE[max])
  


e_voting_simulation()

