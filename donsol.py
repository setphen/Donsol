#Donsol game
import random
import math
from blessed import Terminal

TERM = Terminal()

class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

class Player:

    def __init__(self):
        self.max_health = 21
        self.health = self.max_health
        self.shield = None
        self.can_drink_potion = True
        self.escaped_last_room = False
        self.last_monster_value = None

#Build Deck
# x2, clubs and spades
blackValues = [2,3,4,5,6,7,8,9,10,11,13,15,17]
# x2, hearts and diamonds
redValues = [2,3,4,5,6,7,8,9,10,11,11,11,11]

DECK = []

hearts = [Card('potion', value) for value in redValues]
diamonds = [Card('shield', value) for value in redValues]
clubs = [Card('monster', value) for value in blackValues]
spades = [Card('monster', value) for value in blackValues]
jokers = [Card('monster', 21), Card('monster', 21)]

DECK = [card for suit in [hearts, diamonds, clubs, spades, jokers] for card in suit]

PLAYER = Player()

history = []

#other things
SUIT_COLORS = {
    'monster': TERM.black_on_red,
    'potion': TERM.black_on_green,
    'shield': TERM.black_on_blue,
}

#card positions:
margin = 4
w = 16

CARD_SLOTS = [ 
    {'key':'j', 'position':(margin,margin)},
    {'key':'k', 'position':(margin+w,margin)},
    {'key':'l', 'position':(margin+w*2,margin)},
    {'key':';', 'position':(margin+w*3,margin)},
]

def consume(card):
    global PLAYER, history

    #Take damage from monster
    if card.suit == 'monster':
        if PLAYER.shield:
            if PLAYER.last_monster_value == None or PLAYER.last_monster_value >= card.value: 
                damage = max(0,card.value - PLAYER.shield.value)
                PLAYER.last_monster_value = card.value
            else:
                #Shield broke!
                damage = card.value
                PLAYER.shield = None
                history.append("Shield broke!")
        else:
            damage = card.value

        history.append(TERM.red("Battled " + str(card.value) + " monster, took " + str(damage) + " damage"))
        PLAYER.health = max(0,PLAYER.health - damage)

    #Get health from potion
    if card.suit == 'potion':
        if PLAYER.can_drink_potion:
            PLAYER.health = min(PLAYER.max_health, PLAYER.health + card.value)
            PLAYER.can_drink_potion = False
            history.append(TERM.green("Drank " + str(card.value) + " potion"))
        else:
            history.append(TERM.red("Potion made you sick - No effect!"))
    else:
        PLAYER.can_drink_potion = True

    if card.suit == 'shield':
        PLAYER.shield = card
        PLAYER.last_monster_value = None
        history.append("Equipped " + str(card.value) + " shield")

def main():
    global PLAYER, history
        
    print(TERM.enter_fullscreen)

    print(TERM.clear)

    random.shuffle(DECK)

    draw = []
    room = []
    history = []

    with TERM.cbreak():
        keyval = ''
        
        while keyval.lower() != 'q':

            #HANDLE INPUT

            #Consume a card
            if keyval in [slot['key'] for slot in CARD_SLOTS]:
                #Consume card in KEYVAL associated slot
                try:
                    n = next(index for (index,d) in enumerate(room) if d['slot']['key'] == keyval)
                    consume(room[n]['card'])
                    del room[n]
                except:
                    pass

                if len(room) == 0:
                    PLAYER.escaped_last_room = False

            #Escape room
            no_monsters = len([x['card'] for x in room if x['card'].suit == 'monster']) == 0
            can_escape = not PLAYER.escaped_last_room or no_monsters

            if keyval == 'f':
                if can_escape:
                    DECK.extend([x['card'] for x in room])
                    random.shuffle(DECK)
                    room = []
                    PLAYER.escaped_last_room = True
                    history.append("Escaped the room")
                else:
                    #this gets overwritten by render layer
                    #try creating a messaging system instead
                    history.append(TERM.red("Cannot escape!"))
            
            #Draw new cards, if room is empty
            if len(room) == 0 and PLAYER.health > 0 and len(DECK) > 0:
                ncards = min(len(DECK),4)
               
                draw = DECK[:ncards]

                del DECK[:ncards]

                history.append(TERM.blue(str(len(DECK)) + " CARDS REMAIN"))

                room = list( {'card': x[0], 'slot': x[1]} for x in zip(draw,CARD_SLOTS))


            if PLAYER.health == 0:
                history.append(TERM.black_on_red("YOU DIED"))
            elif len(room) == 0 and len(DECK) == 0:
                history.append(TERM.blue_on_white("YOU SURVIVED"))

            #Escape room
            no_monsters = len([x['card'] for x in room if x['card'].suit == 'monster']) == 0
            can_escape = not PLAYER.escaped_last_room or no_monsters

            #RENDER
            print(TERM.clear)

            #Print cards
            for cardTurn in room:
                if cardTurn:
                    pos = cardTurn['slot']['position']
                    card = cardTurn['card']
                    info = card.suit + " " + str(card.value)
                    print(
                        TERM.move(pos[1], pos[0]) + 
                        SUIT_COLORS[card.suit] (cardTurn['slot']['key'] + "> " + info))

            with TERM.location(margin,margin+2):
                if can_escape:
                    print(TERM.black_on_yellow('f> flee'))
                else:
                    print(TERM.black('f> flee')) 

            #Print my stats!
            with TERM.location(y=margin*2):
                print(TERM.move_x(margin) + "HEALTH: " + str(PLAYER.health))
                if PLAYER.shield:
                    if PLAYER.last_monster_value:
                        print(TERM.move_x(margin) +
                            "SHIELD: " 
                            + str(PLAYER.shield.value) + " " 
                            + TERM.red(str(PLAYER.last_monster_value))
                            )
                    else:
                        print(TERM.move_x(margin) + "SHIELD: " + str(PLAYER.shield.value))

            #Print my messages!
            with TERM.location(y=margin*3):
                for message in history[-6:]:
                    print(TERM.move_x(margin) + TERM.yellow(message))

            #GET INPUT        
            keyval = TERM.inkey()
            if PLAYER.health == 0:
                if keyval != 'q':
                    keyval = '1'


    print(TERM.exit_fullscreen)

if __name__ == "__main__":
    main()
