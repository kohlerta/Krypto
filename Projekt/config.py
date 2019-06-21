#!/usr/bin/phython

VOTEE = ["ÖVP","SPÖ","FPÖ", "GRÜNE", "NEOS", "EUROPA", "KPÖ"]

CNT_VOTEE = len(VOTEE)
CNT_VOTER = 8000000

KEY_SIZE = 128 # sollte 1024 sein, dauert aber zu lang zu test zwecken

#if CNT_VOTEE * CNT_VOTER > KEY_SIZE:
#  KEY_SIZE = CNT_VOTEE * CNT_VOTER

