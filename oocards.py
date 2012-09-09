from strengths import *

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
  
  def __init__(self, hole_cards, cards_on_table=[]):
    self.hole_cards = hole_cards
    self.cards = Hand.calculate_max_hand(hole_cards + cards_on_table)
  
  def __cmp__(self, other):
      for i in range(0, self.strength()):
          if self.strength()[i] == other.strength()[i]:
              continue
          return self.strength()[i] - other.strength()[i]
      
  
  @classmethod
  def calculate_max_hand(cards):
    if len(cards) > 5:
      # TODO: Choose best permutation
      cards = cards[0:5]
    
    return sorted(cards)

  def strength(self):
    """Returns strength of hand, on a scale from [1] to [9]."""
    return [5]
    
  @classmethod
  def strength_type(self, cards):
    for strength_type in range(9, 1, -1):
      if STRENGTH_TYPE_INDICATORS[strength_type](cards):
        return strength_type
    return 1
    
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
