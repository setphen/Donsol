#Donsol game
import random
import math
from time import sleep
import argparse
from blessed import Terminal

from game.models import *

parser = argparse.ArgumentParser()

TERM = Terminal()

SUIT_ART = {
    'monster':
    [
    "   ∭∭  ",
    " ◢ ⁕ ) ",
    "  ╖▓▓╖ ",
    " m▟ m▟ ",
    ]
    ,
    'potion':
    [
    "  ╮◎╭  ",
    "  ┋⇡┋  ",
    " ╭╛ ╘╮ ",
    " ╰━━━╯ ",
    ]
    ,
    'shield':
    [
    "  ▞▲▚  ",
    " ╱┏ ┓╲ ",
    " ╲┗ ┛╱ ",
    "  ▚▼▞  ",
    ]
    ,
}

def main():

    print(TERM.enter_fullscreen)

    print(TERM.clear)

    dungeon = Dungeon()
    renderer = Renderer(dungeon, TERM)

    history = []

    with TERM.cbreak():
        keyval = ''

        while keyval.lower() != 'q':

            #HANDLE INPUT
            dungeon.handle_input(keyval)

            #RENDER
            renderer.render()

 #            with TERM.location(margin,margin+2):
 #                if can_escape and PLAYER.health > 0:
 #                    print( PALETTE['shield'] (TERM.black_on_white('f>') + ' flee'))
 #                else:
 #                    print(TERM.black('f> flee'))
 #
 #            #Print my stats!
 #            with TERM.location(y=margin*2):
 #                healthbar = '#' * PLAYER.health
 #                print(
 #                    TERM.move_x(margin) + "HEALTH: " + str(PLAYER.health)
 #                    + TERM.move_x(margin+12) + PALETTE['potion'] (healthbar)
 #                )
 #                if PLAYER.shield:
 #                    if PLAYER.last_monster_value:
 #                        print(TERM.move_x(margin) +
 #                            "SHIELD: "
 #                            + str(PLAYER.shield.value) + " "
 #                            + TERM.move_x(margin+12) + PALETTE['shield'] ('#' * PLAYER.shield.value)
 # + TERM.red(" ≠" + str(PLAYER.last_monster_value)))
 #
 #                    else:
 #                        print(
 #                            TERM.move_x(margin) + "SHIELD: " +
 #                            str(PLAYER.shield.value) +
 #                            TERM.move_x(margin+12) + PALETTE['shield'] ('#' * PLAYER.shield.value))
 #
 #            #Print my messages!
 #            with TERM.location(y=margin*3):
 #                for message in history[-6:]:
 #                    print(TERM.move_x(margin) + TERM.yellow(message))

            #SLEEP before getting INPUT
            # time.sleep(0.11)

            #GET INPUT
            keyval = TERM.inkey()


    print(TERM.exit_fullscreen)

if __name__ == "__main__":
    main()
