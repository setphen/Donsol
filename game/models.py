# Donsol game
import random
import sys
from time import time
import logging


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

SUIT_TYPES = {HEART: "Potion",
              SPADE: "Monster",
              DIAMOND: "Shield",
              CLUB: "Monster",
              JOKER: "Donsol"}

VALUES = {HEART:   [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 11],
          DIAMOND: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11, 11, 11],
          CLUB:    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17],
          SPADE:   [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 17],
          JOKER:   [21, 21]}

CARD_POSITIONS = {
    'j': 0,
    'k': 1,
    'l': 2,
    ';': 3
}

SUIT_ART = {
    SPADE:
    [
    "   ∭∭  ",
    " ◢ ⁕ ) ",
    "  ╖▓▓╖ ",
    " m▟ m▟ ",
    ]
    ,
    CLUB:
    [
    "   ∭∭  ",
    " ◢ ⁕ ) ",
    "  ╖▓▓╖ ",
    " m▟ m▟ ",
    ]
    ,
    JOKER:
    [
    "   ╱ ╲  ",
    "  [ ۞ ] ",
    "   ╲ ╱  ",
    "   ҈ ҈ ҈ ҈  ",
    ]
    ,
    HEART:
    [
    "  ╮◎╭  ",
    "  ┋⇡┋  ",
    " ╭╛ ╘╮ ",
    " ╰━━━╯ ",
    ]
    ,
    DIAMOND:
    [
    "  ▞▲▚  ",
    " ╱┏ ┓╲ ",
    " ╲┗ ┛╱ ",
    "  ▚▼▞  ",
    ]
    ,
}

class Card:

    def __init__(self, suit, value, name=None):
        self.suit = suit
        self.name = name or suit
        self.value = value

    def is_monster(self):
        return self.suit in [SPADE, CLUB, JOKER]

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
        logging.getLogger('history').info('Fought %s monster, took %s damage' % (monster_value,damage))
        self.can_drink_potion = True

    def equip_shield(self, value):
        self.shield = Shield(value)
        logging.getLogger('history').info('Equipped %s shield' % value)
        self.can_drink_potion = True

    def drink_potion(self, potion_value):
        if self.can_drink_potion:
            previous_health = self.health
            self.health = min(self.max_health, self.health+potion_value)
            #Log it
            msg = 'Drank potion, plus %s health' % (self.health - previous_health)
            logging.getLogger('history').info(msg)
            self.can_drink_potion = False
        else:
            logging.getLogger('history').info('Potion had no effect…')
            pass

    def enter_new_room(self, fled=False):
        self.escaped_last_room = fled


class Shield:

    def __init__(self, value):
        self.value = value
        self.previous_value = None

    def handle_monster(self, monster_value):
        """Return tuple of broken boolean and damage taken"""
        broken = False
        if (self.previous_value is not None and
                monster_value >= self.previous_value):
            logging.getLogger('history').info('Shield Broke!')
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
            #TODO: print flavor text here
            logging.getLogger('history').info('Fleeing the room')
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
        logging.getLogger('history').info("Deck's random seed is: {}".format(seed))
        #print("Deck's random seed is: {}".format(seed))


    def count(self):
        """Return how many cards remain in the deck"""
        return len(self.cards)

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
    cards = []
    for suit in VALUES.keys():
        for value in VALUES[suit]:
            cards.append(Card(suit, value))
    return cards


class Dungeon:
    """Handle deck, room and player creation and interaction"""

    def __init__(self, cards=None, seed=None):
        if not cards:
            cards = make_standard_deck()
        self.deck = Deck(cards=cards, seed=seed)
        self.deck.shuffle()
        self.player = Player()
        self.room_history = []
        #self.event_history = []
        self.generate_room()

    def generate_room(self, fled=False):
        self.player.enter_new_room(fled=fled)
        self.room_history.append(Room(self.deck.draw(4), fled))

    def handle_input(self, input):
        if input == 'q':
            sys.exit()
        elif input in ['j', 'k', 'l', ';'] and self.player.health > 0:
            card = self.room_history[-1].select_card(input)
            if card:
                self.handle_card(card)
            if self.room_history[-1].completed():
                self.generate_room()
        elif input == 'f' and self.room_history[-1].escapable() and self.player.health > 0:
            cards = self.room_history[-1].flee()
            self.handle_flee(cards)
            self.generate_room(fled=True)
        else:
            pass

    def handle_card(self, card):
        if card.suit == HEART:
            self.player.drink_potion(card.value)
        elif card.suit == DIAMOND:
            self.player.equip_shield(card.value)
        else:
            self.player.handle_monster(card.value)

        if self.player.health == 0:
            logging.getLogger('history').info('You died!')

        if self.deck.count() == 0:
            logging.getLogger('history').info('You WON!')


    def handle_flee(self, cards):
        self.deck.add(cards)
        self.deck.shuffle()

class GameLogHandler(logging.Handler):
    """Keep track of what is going on in the Dungeon"""

    def __init__(self, *args, **kwargs):
        super(GameLogHandler, self).__init__(*args, **kwargs)
        self.history = []

    def get_history(self):
        return self.history

    def emit(self, record):
        self.history.append(record.getMessage())




class Renderer:
    """Render the dungeon and controls"""

    def __init__(self, dungeon, terminal, margin = 6, card_spacing = 18):
        self.dungeon = dungeon
        self.term = terminal

        # card positions:
        self.margin = margin
        self.spacing = card_spacing

        self.palette = {HEART: self.term.white,
                        SPADE: self.term.bright_red,
                        DIAMOND: self.term.white,
                        CLUB: self.term.bright_red,
                        JOKER: self.term.bright_blue}

        self.history_handler = GameLogHandler()
        logging.getLogger('history').setLevel(logging.INFO)
        logging.getLogger('history').addHandler(self.history_handler)

    def render(self):
        print(self.term.clear)

        slots = self.dungeon.room_history[-1].slots

        """
        Print artwork
        """

        for slot in slots:
            card = slots[slot]
            pos = CARD_POSITIONS[slot] * self.spacing
            color = self.palette[card.suit]

            for (y, line) in enumerate(SUIT_ART[card.suit]):
                print(self.term.move(1+y,self.margin + pos) + color(line))

        """
        Print card information
        """


        for slot in slots:
            card = slots[slot]
            pos = CARD_POSITIONS[slot] * self.spacing
            color = self.palette[card.suit]
            #info = str(card.name).capitalize() + " " + str(card)
            #
            # for (y, line) in enumerate(SUIT_ART[card.suit]):
            #     print(self.term.move(1+y,pos[0]) + line)

            print(
                self.term.move(self.margin, self.margin + pos) +
                    self.term.black_on_white (slot + '>') +
                    color(' ' + str(SUIT_TYPES[card.suit]) + ' ' +
                    str(card.value)) +
                self.term.move(self.margin + 1, self.margin + pos) +
                    self.term.blue (str(slots[slot]))
                )

        #flee command
        if self.dungeon.room_history[-1].escapable():
            print(
                self.term.move(self.margin + 5, self.margin) +
                self.term.black_on_white('f> flee') )
        else:
            print(
                self.term.move(self.margin + 5, self.margin) +
                self.term.red('Can\'t flee') )



        """
        Print stats like shield, health, etc
        """

        # shield
        if self.dungeon.player.shield:
            if self.dungeon.player.shield.previous_value:
                print(self.term.move(self.margin + 7, self.margin) +
                    "Shield: "
                    + str(self.dungeon.player.shield.value) + " "
                    + self.term.move_x(self.margin + 12) + '#' * self.dungeon.player.shield.value
                    + self.term.red(" ≠" + str(self.dungeon.player.shield.previous_value)))
            else:
                print(
                    self.term.move(self.margin + 7, self.margin) + "Shield: " +
                    str(self.dungeon.player.shield.value) +
                    self.term.move_x(self.margin + 12) +  '#' * self.dungeon.player.shield.value)

        # health
        if self.dungeon.player:
            print(self.term.move(self.margin + 8, self.margin) +
                "Health: "
                + str(self.dungeon.player.health) + " "
                + self.term.move_x(self.margin + 12) + '#' * self.dungeon.player.health)

        if self.dungeon.deck:
            print(self.term.move(self.margin + 9, self.margin) +
                "Cards Remaining: "
                + str(self.dungeon.deck.count()))



        #Print event history
        print(self.term.move(self.margin + 12, self.margin) + "History:")
        for index,x in enumerate(self.history_handler.get_history()[-4:]):
            print(self.term.move(self.margin + 12 + index, self.margin) +
            x)
