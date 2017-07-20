from game.models import (Dungeon,
                         Deck,
                         Player,
                         make_standard_deck)
import pytest


@pytest.fixture
def dungeon():
    return Dungeon(seed=123456789)


def test_deck_order(dungeon):
    """this check ensures that we can plan for the first three rooms having
    known cards and thus we can check the availability of certain actions or
    sequences of actions"""
    # room 1
    assert str(dungeon.room_history[-1].slots['j']) == "4 of Spades"
    assert str(dungeon.room_history[-1].slots['k']) == "4 of Clubs"
    assert str(dungeon.room_history[-1].slots['l']) == "10 of Clubs"
    assert str(dungeon.room_history[-1].slots[';']) == "8 of Spades"
    dungeon.generate_room()
    # room 2
    assert str(dungeon.room_history[-1].slots['j']) == "17 of Clubs"
    assert str(dungeon.room_history[-1].slots['k']) == "11 of Diamonds"
    assert str(dungeon.room_history[-1].slots['l']) == "8 of Diamonds"
    assert str(dungeon.room_history[-1].slots[';']) == "7 of Spades"
    # room 3
    dungeon.generate_room()
    assert str(dungeon.room_history[-1].slots['j']) == "5 of Clubs"
    assert str(dungeon.room_history[-1].slots['k']) == "11 of Spades"
    assert str(dungeon.room_history[-1].slots['l']) == "17 of Spades"
    assert str(dungeon.room_history[-1].slots[';']) == "11 of Diamonds"
    # room 4
    dungeon.generate_room()
    assert str(dungeon.room_history[-1].slots['j']) == "9 of Spades"
    assert str(dungeon.room_history[-1].slots['k']) == "Joker"
    assert str(dungeon.room_history[-1].slots['l']) == "6 of Spades"
    assert str(dungeon.room_history[-1].slots[';']) == "2 of Diamonds"


def test_dungeon_valid_flee_unconditioned(dungeon):
    dungeon.handle_input('f')
    assert len(dungeon.room_history) == 2


def test_cannot_flee_twice(dungeon):
    assert dungeon.room_history[-1].escapable() == True
    dungeon.handle_input('f')
    assert dungeon.player.escaped_last_room == True
    assert dungeon.room_history[-1].escapable() == False
    dungeon.handle_input('f')
    assert len(dungeon.room_history) == 2


def test_can_flee_after_clearing_monsters(dungeon):
    # skip the first room
    dungeon.generate_room()
    # second room
    print(dungeon.room_history[-1].slots)
    dungeon.handle_input('k') # equip the 11 shield
    assert dungeon.player.shield.value == 11
    dungeon.handle_input('f') # this causes the deck to be reshuffled
    # third room
    assert len(dungeon.room_history) == 3
    dungeon.handle_input('f') # try to flee again
    assert len(dungeon.room_history) == 3 # couldn't escape
    dungeon.handle_input('l') # handle club 5
    dungeon.handle_input('j') # handle spade 2
    dungeon.handle_input('f') # try to flee
    assert len(dungeon.room_history) == 3 # couldn't escape
    dungeon.handle_input(';') # handle last monster
    dungeon.handle_input('f') # try to flee
    assert len(dungeon.room_history) == 4 # escaped!
