import pytest
from game.models import (Room,
                         Card,
                         HEART,
                         DIAMOND,
                         CLUB,
                         SPADE)


@pytest.fixture
def cards():
    return [
        Card(HEART, 5, 'Elixir'),
        Card(SPADE, 2),
        Card(CLUB, 9, ''),
        Card(DIAMOND, 6, 'Stalwart'),
    ]


def test_room_escapable(cards):
    r = Room(cards, player_escaped_previous_room=False)
    assert r.escapable() == True


def test_room_previous_escaped(cards):
    r = Room(cards, player_escaped_previous_room=True)
    assert r.escapable() == False


def test_room_select_card(cards):
    r = Room(cards, player_escaped_previous_room=True)
    card = r.select_card('k')
    assert card.suit == SPADE
    assert card.value == 2


def test_room_flee_failure(cards):
    r = Room(cards, player_escaped_previous_room=True)
    assert r.flee() == None


def test_room_flee_success(cards):
    r = Room(cards)
    assert set(r.flee()) == set(cards)
