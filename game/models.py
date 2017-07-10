# Donsol game
import random
import sys
from time import time


HEART = 1
DIAMOND = 2
SPADE = 3
CLUB = 4
JOKER = 5

SUIT_NAMES = {HEART: "Hearts",
              SPADE: "Spades",
              DIAMOND: "Diamonds",
              CLUB: "Clubs",
              JOKER: "Joker"}

VALUES = {HEART:   [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 11],
          DIAMOND: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 11],
          CLUB:    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17],
          SPADE:   [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17],
          JOKER:   [21, 21]}


class Card:

    def __init__(self, suit, value, name=None):
        self.suit = suit
        self.name = name or suit
        self.value = value

    def is_monster(self):
        return self.suit in [SPADE, CLUB]

    def __str__(self):
        if self.suit == JOKER:
            return "Joker"
        return "{} of {}".format(self.value, SUIT_NAMES[self.suit])

    def __repr__(self):
        return str(self)


class Player:

    def __init__(self):
        self.max_health = 21
        self.health = self.max_health
        self.shield = None
        self.can_drink_potion = True
        self.escaped_last_room = False

    def handle_monster(self, monster_value):
        damage = monster_value
        if self.shield:
            broken, damage = self.shield.handle_monster(monster_value)
            if broken:
                self.shield = None
        self.health = max(0, self.health - damage)
        self.can_drink_potion = True

    def equip_shield(self, shield):
        self.shield = shield
        self.can_drink_potion = True

    def drink_potion(self, potion_value):
        if self.can_drink_potion:
            self.health = min(self.max_health, self.health+potion_value)
            self.can_drink_potion = False
        else:
            pass


class Shield:

    def __init__(self, value):
        self.value = value
        self.previous_value = None

    def handle_monster(self, monster_value):
        """Return tuple of broken boolean and damage taken"""
        broken = False
        if (self.previous_value is not None and
                monster_value >= self.previous_value):
            # logging.getLogger('history', 'Shield Broke!')
            broken = True
            self.value = 0
        self.previous_value = monster_value
        return (broken, max(0, monster_value - self.value))


class Room:

    def __init__(self, cards, player_escaped_previous_room=False):
        self.slots = dict(zip('jkl;', cards))
        self.player_escaped_previous_room = player_escaped_previous_room

    def flee(self):
        """
        Fleeing returns None if unable to flee, else returns the set of
        cards to return to the deck
        """
        if self.escapable():
            return self.slots.values()
        return None

    def select_card(self, key):
        """
        Return the card at 'key' from the room, and remove it from the rooms'
        storage. If given an invalid key, return None
        """
        try:
            return self.slots.pop(key)
        except KeyError:
            return None

    def completed(self):
        if self.slots:
            return False
        return True

    def escapable(self):
        """Check whether or not the room is escapable"""
        if self.player_escaped_previous_room:
            monsters_remain = any(c.is_monster() for c in self.slots.values())
            if monsters_remain:
                return False
        return True


class Deck:
    """A deck holds an ordered set of cards and can pop or shuffle them"""

    def __init__(self, cards, seed=None):
        """Optionally accept a seed to make the deck deterministic"""
        self.cards = cards
        self.random = random.Random()
        if seed is None:
            seed = time()

        self.random.seed(seed)
        print("Deck's random seed is: {}".format(seed))

    def draw(self, count):
        """
        Draw <count> cards from the deck, or as many as are available.
        return a list of cards drawn.
        """
        drawn = []
        while len(drawn) < count:
            try:
                drawn.append(self.cards.pop())
            except IndexError:
                break
        return drawn

    def shuffle(self):
        self.random.shuffle(self.cards)

    def add(self, cards):
        """Add the passed list of cards to the deck"""
        self.cards.extend(cards)


def make_standard_deck():
    print("running MSD")
    cards = []
    for suit in VALUES.keys():
        for value in VALUES[suit]:
            cards.append(Card(suit, value))
    return cards


class Dungeon:
    """Handle deck, room and player creation and interaction"""

    def __init__(self, cards=make_standard_deck(), seed=None):
        self.deck = Deck(cards=cards, seed=seed)
        self.deck.shuffle()
        self.player = Player()
        self.room_history = []
        self.generate_room()

    def generate_room(self):
        self.room_history.append(
            Room(self.deck.draw(4),
                 self.player.escaped_last_room))

    def handle_input(self, input):
        if input == 'q':
            sys.exit()
        elif input in ['j', 'k', 'l', ';']:
            card = self.room_history[-1].select_card(input)
            self.handle_card(card)
            if self.room_history[-1].completed():
                self.generate_room()

        elif input == 'f' and self.room_history[-1].escapable():
            cards = self.room_history[-1].flee()
            self.handle_flee(cards)
            self.generate_room()
        else:
            pass

    def handle_card(self, card):
        if card.suit == HEART:
            self.player.drink_potion(card.value)
        elif card.suit == DIAMOND:
            self.player.equip_shield(card.value)
        else:
            self.Player.handle_monster(card.value)

    def handle_flee(self, cards):
        self.deck.add(cards)
        self.deck.shuffle()
