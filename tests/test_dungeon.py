from game.models import (Dungeon,
                         Deck,
                         Player,
                         make_standard_deck)
import pytest


@pytest.fixture
def dungeon():
    return Dungeon(make_standard_deck(), seed=123456789)


def test_deck_order(dungeon):
    """this check ensures that we can plan for the first three rooms having
    known cards and thus we can check the availability of certain actions or
    sequences of actions"""
    cards = dungeon.deck.draw(12)
    assert str(cards[0]) == "17 of Clubs"
    assert str(cards[1]) == "11 of Diamonds"
    assert str(cards[2]) == "8 of Diamonds"
    assert str(cards[3]) == "7 of Spades"
    assert str(cards[4]) == "5 of Clubs"
    assert str(cards[5]) == "11 of Spades"
    assert str(cards[6]) == "17 of Spades"
    assert str(cards[7]) == "11 of Diamonds"
    assert str(cards[8]) == "9 of Spades"
    assert str(cards[9]) == "Joker"
    assert str(cards[10]) == "6 of Spades"
    assert str(cards[11]) == "2 of Diamonds"


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
