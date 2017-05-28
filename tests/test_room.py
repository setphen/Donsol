import pytest
from game.models import Room, Card


@pytest.fixture
def cards():
    return [
        Card('heart', 5, 'Elixir'),
        Card('spade', 2),
        Card('club', 9, ''),
        Card('diamond', 6, 'Stalwart'),
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
    assert card.suit == 'spade'
    assert card.value == 2


def test_room_flee_failure(cards):
    r = Room(cards, player_escaped_previous_room=True)
    assert r.flee() == None


def test_room_flee_success(cards):
    r = Room(cards)
    assert set(r.flee()) == set(cards)
