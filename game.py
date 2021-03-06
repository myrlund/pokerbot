# from cards import *
from oocards import *
from player import *
import csv
import random



class Dealer:
    
    def __init__(self):
        self.deck = []
        self.sorted_deck = []
        self.gen_shuffled_deck()
        self.gen_sorted_deck()
        
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
            self.deck.append(temp_deck[index])
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
                print 'Sorted deck is empty. Making new.'
                self.gen_sorted_deck()
        return cards
    
    def remove_from_deck(self, card):
        for c in self.deck:
            if c == card:
                self.deck.remove(c)
                
    
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

    def __init__(self, dealer):
        self.players = []
        self.cards_on_table = []
        self.dealer = dealer #hummhumm? 
        self.pot = 0
        high_bet = 0
        
    def add_player(self, player):
        player.game = self
        self.players.append(player)
    
    #rolls through 100k games and records probability of winning with given hole cards.
    #then writes probabilities to csv file...
    #
    def rollout_play(self):
        
        self.dealer = Dealer()
        self.add_player(Player(1, 0))
        self.add_player(Player(2, 0))
        self.add_player(Player(3, 0))
        self.add_player(Player(4, 0))
        
        stats = []
        for i in range(2, 15):
            row_of_stats = []
            for j in range(2, 15):
                if j<i:
                    continue
                #deals combination of hole cards that are not equivalent, to player 1,
                wins = 0
                draws = 0
                losses = 0
                card1 = Card("s", i)
                card2 = Card("s", j)
                self.players[0].deal(Hand([card1, card2], []))
                #removes the cards it dealt from the deck
                self.dealer.remove_from_deck(card1)
                self.dealer.remove_from_deck(card2)
                
                #proceedes to deal to rest of players (100k times?) and registering wins,losses and draws
                for x in range(0, 10): #100k?
                    for y in range(1, len(self.players)):
                        self.players[y].deal(Hand(self.dealer.deal(2)))

                    self.deal_rollout()
                    
                    winners = self.find_winner()
                    if winners.count(self.players[0]) > 0:
                        if len(winners) == 1:
                            wins+=1
                        else:
                            draws+=1
                        continue
                    losses+=1
                #save statistics of the given hole card combination
                row_of_stats.append(wins/(wins+draws+losses))
            stats.append(row_of_stats)
            print str(row_of_stats)
                
        #save the statistics to a csv file
#        stats_file = open("hole_card_stats.csv", "wb")
#        stats_writer = csv.writer(stats_file, delimiter=",")
#        for i in range(0, stats):
#            for j in range(0, stats):
#                stats_writer.write(stats[i][j])
                
    #standard play  
    def play_round(self):
        self.deal_hole_cards()
        self.print_gamestate()
        
        self.take_bets()
        self.print_gamestate()
        
        self.deal_flop()
        self.print_gamestate()
        
        self.take_bets()
        self.print_gamestate()
        
        self.deal_turn()
        self.print_gamestate()
        
        self.take_bets()
        self.print_gamestate()
        
        self.deal_river()
        self.print_gamestate()
        
        self.take_bets()
        self.print_gamestate()
        
        winner = self.find_winner()
        print "WINNER: "+winner
        winner.get_winnings(self.pot)
        
            
        
    def fold_player(self, folded_player):
        self.players.delete(folded_player)
        
         
    def find_winner(self):
        #find the winners, returns a list with all the winners (drawz!)
        winners = []
        winners_counter = 1
        winners.append(self.players[0])
        for i in range(1, len(self.players)):
            if winners[0].hand < self.players[i].hand:
                winners = [self.players[i]]
            elif winners[0].hand == self.players[i].hand:
                winners.append(self.players[i])
                winners_counter += 1
        return winners
            
    #get actions from all the players, call/raise/fold                        
    def take_bets(self):
        better = None 
        player = self.players[0]
        i = 0
        
        while better != player:
            bet = player.action_selection(self.high_bet)
            if bet>0:
                better = player
                self.high_bet = player.current_bet
                self.pot += bet
            elif bet < 0:
                self.fold_player(player)
                
            if i < self.players-1:
                i += 1
            else:
                i = 0
            player = self.players[i]
    
    def deal_flop(self):
        self.cards_on_table += self.dealer.deal(3)
        
    def deal_turn(self):
        self.cards_on_table += self.dealer.deal(1)
        
    def deal_river(self):
        self.cards_on_table += self.dealer.deal(1)
        
    def deal_rollout(self):
        self.cards_on_table = self.dealer.deal(5)
        
    def deal_hole_cards(self):
        for player in self.players:
            player.deal(Hand(self, self.dealer.deal(2)))

    def print_gamestate(self):
        for player in self.players:
            print(player)
        print "- On table: "+ str(self.cards_on_table) +" $"+ str(self.pot) +" "
        print "In deck: "+ str(self.dealer.deck)



if __name__ == "__main__":
    print "WE BE TESTIN UP IN HERRE!"
    dealer = Dealer()
    
    game = Game(dealer)
    game.add_player(Player(1, 20))
    game.add_player(Player(2, 20))
    game.add_player(Player(3, 20))
    game.add_player(Player(4, 20))
    game.rollout_play()
    
