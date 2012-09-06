STRENGTH_HIGH_CARD = 1
STRENGTH_PAIR = 2
STRENGTH_TWO_PAIRS = 3
STRENGTH_THREE_KIND = 4
STRENGTH_STRAIGHT = 5
STRENGTH_FLUSH = 6
STRENGTH_FULL_HOUSE = 7
STRENGTH_FOUR_KIND = 8
STRENGTH_STRAIGHT_FLUSH = 9


def is_pair(cards):
  counts = {}
  for card in cards:
    counts[card.value] = counts.get(card.value, 0) + 1
    if counts[card.value] == 2:
      return True
  return False

def pair_strength(cards):
  counts = {}
  for card in cards:
    counts[card.value] = counts.get(card.value, 0) + 1
    if counts[card.value] == 2:
      nonpaired_cards = sorted([c for c in cards if c.value != card.value])
      return [2, card.value] + nonpaired_cards
      
  return False

def is_two_pairs(cards):
  
  return False

def is_three_of_a_kind(cards):
  return False

def is_straight(cards):
  return False

def is_flush(cards):
  return False

def is_full_house(cards):
  return False

def is_four_of_a_kind(cards):
  return False

