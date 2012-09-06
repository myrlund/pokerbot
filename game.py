from cards import *
import csv
import random



class Dealer:
    
    def __init__(self):
        self.deck = []
        self.sorted_deck = []
        
    def gen_sorted_deck(self):
        self.sorted_deck = []
        for s in SUITS:
            for i in range(2, 15):
                self.sorted_deck.append(Card(s,i))
       
    def shuffle_deck(self):
        temp_deck = self.sorted_deck
        self.deck = []
        for i in range(0, 52):
            index = random.randint(0, 51-i)
            self.deck[i] = temp_deck[index]
            temp_deck[index:index+1] = []
        
        
       
    def gen_shuffled_deck(self):
        self.gen_sorted_deck()
        self.shuffle_deck()
         
    #for rollout simulation?
    def deal_sorted(self, nr_of_cards): 
        cards = []
        for i in range(0, nr_of_cards):
            if self.sorted_deck:
                cards.append(self.sorted_deck.pop(0))
            else:
                print "Sorted deck is empty. Making new..."
                self.gen_sorted_deck()
        return cards
    
    
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
        
    #rolls through 100k games and records probability of winning with given hole cards.
    #then writes probabilities to csv file...
    def rollout_play(self):
        stats = [][]
        
        for i in range(0, 100):
            self.deal_hole_cards()
            self.take_bets()
            
            self.deal_rollout()
            self.take_bets()    
            
            
        stats_file = open("hole_card_stats.csv", "wb")
        stats_writer = csv.writer(stats_file, delimiter=",")
        for i in range(0, stats):
            for i in range(0, stats[]):
                stats_writer.write(stats[i][j])
                
                
        
    def fold_player(self, folded_player):
        self.players.delete(folded_player)
        
         
    def find_winner(self):
        #find the winner
        winner = self.players[0]
        for i in range(1, self.players):
            if winner.hand.__cmp__(self.players[i]) < 0:
                winner = self.players[i]
        return winner
            
                            
    def take_bets(self):
        return 
    
    def deal_flop(self):
        self.cards_on_table += self.dealer.deal_n_cards(3)
        
    def deal_turn(self):
        self.cards_on_table += self.dealer.deal_n_cards(1)
        
    def deal_river(self):
        self.cards_on_table += self.dealer.deal_n_cards(1)
        
    def deal_rollout(self):
        self.cards_on_table = self.dealer.deal_n_cards(5)
        
    def deal_hole_cards(self):
        for player in self.players:
            player.deal(Hand(self, self.dealer.deal_n_cards(2)))
        
        
    def print_gamestate(self):
        for player in self.players:
            print str(player)
        print "- On table: "+ str(self.cards_on_table) +" $"+ str(self.pot) +" "
        print "In deck: "+ str(self.dealer.deck)
        

if __name__ == '__main__':
    dealer = Dealer()
    dealer.gen_shuffled_deck()
    print sorted(dealer.deck)

