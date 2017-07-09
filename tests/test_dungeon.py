from game.models import (Dungeon,
                         Deck,
                         Player,
                         make_standard_deck)
import pytest


@pytest.fixture
def dungeon():
    return Dungeon(make_standard_deck(), seed=123456789)


def test_dungeon_handle_input_valid(dungeon):
    dungeon.handle_input('f')

