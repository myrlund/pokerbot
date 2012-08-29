from oocards import *
import random



class Dealer:
    def __init__(self):
        self.deck = []
        
    def gen_shuffled_deck(self):
        sorted_deck = []
        for s in SUITS:
            for i in range(2, 15):
                sorted_deck.append(Card(s,i))
        #shuffleduffle
        deck = []
        for i in range(0, 52):
            index = random.randint(0, 51-i)
            deck[i] = sorted_deck[index]
            sorted_deck[index:index+1] = []
        
            
    #deals x card(s) of it's deck
    def deal(self, nr_of_cards):
        
        
        
class Game:
    
    #  w00t holder vel game-staten hummhumm

    def __init__(self, players, cards_on_table, dealer, pot):
        self.players = players
        self.cards_on_table = cards_on_table
        self.dealer = dealer #hummhumm? 
        self.pot = pot
        
        
    def play(self):
        #sumethin n stuff
    

        