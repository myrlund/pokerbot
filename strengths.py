
def is_pair(cards):
  counts = {}
  for card in cards:
    counts[card.value] = counts.get(card.value, 0) + 1
    if counts[card.value] == 2:
      return True
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

