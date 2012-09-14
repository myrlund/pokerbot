from copy import copy
from oocards import *

# Some information constants
HIGH_BET   = 0
BETS       = 1
TOTAL_BETS = 2
HAND       = 3
TABLE      = 4

# Action constants
FOLD  = 0
CALL  = 1
RAISE = 2

class Game:
    
    def __init__(self, players=[]):
        self.players = players
        self.dealer_position = 0
        self.blinds = (1, 2)
        self.max_raises = 3
    
    def play(self, n=100):
        """Plays n rounds."""
        for i in range(n):
            self.play_round()
        
        print "Scores:"
        total = 0
        for player in self.players:
            print "%s: %d" % (player, player.balance)
            total += player.balance
        
        print "TOTAL: %d" % total
    
    def play_round(self):
        self.deck = Deck()
        Round(self, self.dealer_position).play()
        
        # Move dealer button around the table
        self.dealer_position += 1
        self.dealer_position %= len(self.players)
    
    def deal(self, n):
        """Deals n cards."""
        return self.deck.deal(n)

class Round:
    
    def __init__(self, game, dealer_position):
        self.game = game

        # Round participants - players deleted as they fold
        self.dealer_position = dealer_position
        self.players = copy(game.players) # Shallow copy
        self.order_players()
        
        self.hands = {}
        self.table = []
        
        self.pot = 0
        self.total_bets = {}
        
        # Reset each betting round
        self.bets = {}
    
    def play(self):
        """Plays a single round."""
        
        self.deal_hole_cards()
        self.take_bets(place_blinds=True)
        
        self.deal_flop()
        self.take_bets()
        
        self.deal_turn()
        self.take_bets()
        
        self.deal_river()
        seen_player_index = self.take_bets()
        
        return self.showdown(seen_player_index)
    
    def take_bets(self, place_blinds=False):
        """Runs a betting round."""
        players = self.players
        raises = {}
        self.bets = {}
        
        if place_blinds:
            for i in range(2):
                self.place_bet(players[i], self.game.blinds[i])
            
            high_betting_player_index = 1
            betting_player_index = 2 % len(players)
            high_bet = self.bets[players[high_betting_player_index]]
            first_bet = False
        
        else:
            high_betting_player_index = 0
            high_bet = 0
            betting_player_index = high_betting_player_index
            first_bet = True
        
        # Run until back at highest betting player without raise, or first round
        while first_bet or betting_player_index != high_betting_player_index:
            first_bet = False
            
            # Player acts
            betting_player = players[betting_player_index]
            
            info = {
                HIGH_BET: high_bet,
                BETS: self.bets,
                TOTAL_BETS: self.total_bets,
                HAND: self.hands[betting_player],
                TABLE: self.table
            }
            
            # Any player's act method should return an action and an amount
            action, amount = betting_player.act(self, info)
            
            # Each player can raise a maximum number of times
            if betting_player in raises and raises[betting_player] >= self.game.max_raises:
                action = CALL
            
            if action == FOLD:
                self.update("%s folds." % betting_player)
                
                self.players.delete(betting_player)
                
            elif action == CALL: # /CHECK
                # If high bet greater than current round of bets from player, place the difference
                if self.bets[betting_player] < high_bet:
                    self.place_bet(betting_player, high_bet - self.bets[betting_player])
                    
                self.update("%s calls with %d." % (betting_player, high_bet - self.bets[betting_player]))
                
            elif action == RAISE:
                # Place given amount as a new bet
                high_betting_player_index = betting_player_index
                self.place_bet(betting_player, amount)
                
                # Add to number of raises for player
                if betting_player in raises:
                    raises[betting_player] += 1
                else:
                    raises[betting_player] = 1
                
                # High bet is the accumulated bet of highest betting player
                high_bet = self.bets[betting_player]
                
                self.update("%s raises the pot with %d." % (betting_player, amount))
                
            else:
                raise Exception("Not a valid action.")
            
            # Next player to act
            betting_player_index = (betting_player_index + 1) % len(players)
        
        # Return seen player's index
        return high_betting_player_index
    
    def showdown(self, seen_player_index):
        """Determines winners and gives out money in pot."""
        strongest_hand = None
        strongest_players = []
        for i in range(seen_player_index, seen_player_index + len(self.players)):
            player_index = i % len(self.players)
            player = self.players[player_index]
            player_hand = Hand(self.hands[player], self.table)
            
            if not strongest_hand:
                strongest_hand = player_hand
            
            self.debug("* %s shows %s." % (player, player_hand.hole_cards))
            
            # Assume first player is the strongest
            if not strongest_players:
                strongest_players = [player]
            
            # Compare current strongest hand to this player's hand
            if strongest_hand and player_hand > strongest_hand:
                if strongest_hand == player_hand:
                    strongest_players.append(player)
                else:
                    strongest_players = [player]
                
                strongest_hand = player_hand
        
        # Share pot money between winners
        pot_per_player = self.pot / len(strongest_players)
        for player in strongest_players:
            self.debug("** %s wins %d with a %s." % (player, pot_per_player, STRENGTH_TYPES[strongest_hand.strength()[0]]))
            player.win(pot_per_player)
        
        return strongest_players
    
    def deal_hole_cards(self):
        """Deals 2 cards to each player."""
        for player in self.players:
            self.hands[player] = self.game.deal(2)
    
    def deal_flop(self):
        """Deals 3 cards to the table."""
        self.table = self.game.deal(3)
        self.update("Dealing flop. Table: %s." % self.table)
    
    def deal_turn(self):
        """Deals 1 card to the table."""
        self.table += self.game.deal(1)
        self.update("Dealing turn. Table: %s." % self.table)
    
    def deal_river(self):
        """Deals 1 card to the table."""
        self.table += self.game.deal(1)
        self.update("Dealing river. Table: %s." % self.table)
    
    def order_players(self):
        """Players ordered from dealer button."""
        players = []
        for i in range(0, len(self.players)):
            player_index = (i + self.dealer_position) % len(self.players)
            players.append(self.players[player_index])
        self.players = players

    def place_bet(self, player, amount):
        player.bet(amount)
        
        self.pot += amount
        
        if player in self.bets:
            self.bets[player] += amount
        else:
            self.bets[player] = amount
        
        if player in self.total_bets:
            self.total_bets[player] += amount
        else:
            self.total_bets[player] = amount
    
    def debug(self, msg):
        print msg
    
    def update(self, msg):
        self.debug("%s Pot total: %d." % (msg, self.pot))


class RolloutGame(Game):
    def play(self, hand, n=100):
        n_wins = 0
        n_draws = 0
        for i in range(n):
            winners = self.play_round(hand)
            if self.players[0] in winners: 
                if len(winners) == 1:
                    n_wins += 1
                else:
                    n_draws += 1
        return (n_wins + n_draws / 2.0) / n
    
    def play_round(self, cards):
        self.deck = Deck()
        return RolloutRound(self, self.dealer_position).play(cards)

class RolloutRound(Round):
    def play(self, hand):
        self.hand = hand
        return Round.play(self)
    
    def deal_hole_cards(self):
        self.hands[self.players[0]] = self.hand
        self.game.deck.remove(self.hand)
        for player in self.players[1:]:
            self.hands[player] = self.game.deal(2)
        
    def take_bets(self, place_blinds=False):
        """A simple overridden take_bets, without money and shit."""
        return 0

    def debug(self, msg):
        pass


class APlayer:
    """Abstract player class."""
    
    def __init__(self, name, money):
        self.name = name
        self.balance = money

    def bet(self, amount):
        """Decreases balance by amount."""
        self.balance -= amount
    
    def win(self, amount):
        """Increases balance by amount."""
        self.balance += amount
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.__str__()

class Player(APlayer):
    """Actual player bot."""
    def act(self, round, info):
        return RAISE, round.game.blinds[1]

if __name__ == '__main__':
    player1 = Player("Player 1", 1000)
    player2 = Player("Player 2", 1000)
    player3 = Player("Player 3", 1000)
    player4 = Player("Player 4", 1000)
    game = RolloutGame([player1, player2, player3, player4])
    
    for v1 in VALUES.keys():
        for v2 in [v for v in VALUES.keys() if v < v1]:
            if v1 != v2:
                hand = [Card(SUITS.keys()[0], v1), Card(SUITS.keys()[0], v2)]
                print "%s: %f" % (hand, game.play(hand))
            hand = [Card(SUITS.keys()[0], v1), Card(SUITS.keys()[1], v2)]
            print "%s: %f" % (hand, game.play(hand))
            
        
            





