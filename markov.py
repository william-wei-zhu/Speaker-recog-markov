'''
MPCS 51042 S'20: Markov models and hash tables

William Zhu (wzhu4@uchicago.edu)
'''
import math
from hash_table import Hashtable

HASH_CELLS = 57

# Recommended load factor and growth factor for the assignment
# TOO_FULL = 0.5
# GROWTH_RATIO = 2

class Markov:

    def __init__(self, k, text, state):
        self.k = k
        self.ltext = len(text)
        self.S = len(set(text))
        self.state = state

        if state == 0:
            self.table = Hashtable(HASH_CELLS, 0, 0.5, 2)
        elif state == 1:
            self.table = {}

        for i in range(self.ltext):
            if i + k + 1 < self.ltext:
                self.add_to_table(text[i:i+k])
                self.add_to_table(text[i:i+k+1])

            elif i + k + 1 == self.ltext:
                self.add_to_table(text[i:i+k])
                self.add_to_table(text[i:])
                
            elif i + k == self.ltext:
                self.add_to_table(text[i:])
                temp = text[i:] + text[0]
                self.add_to_table(temp)

            else:
                temp1 = text[i:] + text[:i+k-self.ltext]
                self.add_to_table(temp1)
                temp2 = text[i:] + text[:i+k-self.ltext+1]
                self.add_to_table(temp2)

    def add_to_table(self, key):
        if key not in self.table:
            self.table[key] = 1
        else:
            self.table[key] = self.table[key] + 1

    def find_MN(self, key1, key2):
        if key1 not in self.table:
            self.N = 0
        else:
            self.N = self.table[key1]
        
        if key2 not in self.table:
            self.M = 0
        else:
            self.M = self.table[key2]

    def log_probability(self, text):
        self.ltext2 = len(text)
        self.total_log = 0
        for i in range(self.ltext2):
            if i + self.k + 1 < self.ltext2:
                self.find_MN(text[i:i+self.k], text[i:i+self.k+1])

            elif i + self.k + 1 == self.ltext2:
                self.find_MN(text[i:i+self.k], text[i:])

            elif i + self.k == self.ltext2:
                self.find_MN(text[i:], text[i:] + text[0])

            else:
                temp1 = text[i:] + text[:i+self.k-self.ltext2]
                temp2 = text[i:] + text[:i+self.k-self.ltext2+1]
                self.find_MN(temp1, temp2)
            
            self.total_log += math.log((self.M+1)/(self.N+self.S))

        return self.total_log


def identify_speaker(speaker_a, speaker_b, unknown_speech, k, state):
    l3 = len(unknown_speech)
    speech1 = Markov(k, speaker_a, state)
    p1 = speech1.log_probability(unknown_speech)/l3

    speech2 = Markov(k, speaker_b, state)
    p2 = speech2.log_probability(unknown_speech)/l3
    winner = "A"
    if p2 > p1:
        winner = "B"
    return (p1, p2, winner)

