from strengths import *
from copy import copy
import random

class Deck:
    
    def __init__(self):
        self.cards = []
        for suit in SUITS.keys():
            for value in VALUES.keys():
                self.cards.append(Card(suit, value))
        self.shuffle()
        
    def shuffle(self):
        ordered_cards = self.cards
        self.cards = []
        
        for i in range(52):
            index = random.randint(0, 51-i)
            self.cards.append(ordered_cards[index])
            ordered_cards[index:index+1] = []
    
    def deal(self, n):
        """Deals n cards."""
        cards = []
        for i in range(n):
            cards.append(self.cards.pop())
        return cards

class Card:
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __cmp__(self, other):
        return self.value - other.value
    
    def __str__(self):
        return "%s%s" % (str(VALUES[self.value]), self.suit)
    
    def __repr__(self):
        return self.__str__()

class Hand:
  
    def __init__(self, hole_cards=[0], cards_on_table=[]):
        self.hole_cards = hole_cards
        self.cards = Hand.calculate_max_hand(hole_cards + cards_on_table)

    def __cmp__(self, other):
        for i in range(0, len(self.strength())):
            if self.strength()[i] == other.strength()[i]:
                continue
            return self.strength()[i] - other.strength()[i]
        return 0

    def strength(self):
        return Hand.strength_of_cards(self.cards)

    @classmethod
    def calculate_max_hand(self, cards):
        # a b c d e f g
        if len(cards) > 5:
            # for i in range(len(cards) - 1):
            
            # TODO: Choose best permutation
            cards = cards[0:5]
        
        return sorted(cards)

    @classmethod
    def strength_of_cards(self, cards):
        """Returns strength of hand, on a scale from [1] to [9]."""
        for strength_type in range(9, 1, -1):
            strength_found = STRENGTH_TYPE_INDICATORS[strength_type](cards)
            if strength_found:
                return strength_found
        return [1] + sorted(cards).reverse()
        
    @classmethod
    def strength_type(self, cards):
        for strength_type in range(9, 1, -1):
            if STRENGTH_TYPE_INDICATORS[strength_type](cards):
                return strength_type
        return 1
    
    def __str__(self):
        return str(Hand.calculate_max_hand(self.cards))
        
STRENGTH_TYPES = {
    1: 'high card',
    2: 'pair',
    3: 'two pairs',
    4: 'three of a kind',
    5: 'straight',
    6: 'flush',
    7: 'full house',
    8: 'four of a kind',
    9: 'straight flush'
}
STRENGTH_TYPE_INDICATORS = {
    2: is_pair,
    3: is_two_pairs,
    4: is_three_of_a_kind,
    5: is_straight,
    6: is_flush,
    7: is_full_house,
    8: is_four_of_a_kind,
    9: lambda cards: is_straight(cards) and is_flush(cards),
}

SUITS = {
    's': 'spades',
    'h': 'hearts',
    'c': 'clubs',
    'd': 'diamonds'
}
VALUES = dict([[n, n] for n in range(2, 11)] + zip([11, 12, 13, 14], ['J', 'Q', 'K', 'A']))

if __name__ == '__main__':
    cards = [Card('s', 2), Card('d', 2), Card('s', 9), Card('s', 10), Card('s', 11)]
    
    print "%s: %s" % (cards, STRENGTH_TYPES[Hand.strength_type(cards)])
