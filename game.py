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
        self.deck = []
        for i in range(0, 52):
            index = random.randint(0, 51-i)
            self.deck[i] = sorted_deck[index]
            sorted_deck[index:index+1] = []
        
            
    #deals nr_of_cards card(s) of it's deck
    def deal(self, nr_of_cards):
        cards = []
        for i in range(0, nr_of_cards):
            if self.deck:
                cards.append(self.deck.pop(0))
            else:
                print "Deck is empty. Shuffling new..."
                self.gen_shuffled_deck()
        return cards
        
        
        
class Game:
    
    #  w00t holder vel game-staten hummhumm

    def __init__(self, players, cards_on_table, dealer, pot):
        self.players = players
        self.cards_on_table = cards_on_table
        self.dealer = dealer #hummhumm? 
        self.pot = pot
        
        
    def play(self):
        #plain da game in turns, turns should hold for input? or maybe just gogogoo
        self.print_gamestate()
        
    def print_gamestate(self):
        for player in self.players:
            print str(player)
        print "- On table: "+ str(self.cards_on_table) +" $"+ str(self.pot) +" "
        print "In deck: "+ str(self.dealer.deck)
        
    

        