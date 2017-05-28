import pytest
from game.models import Player

def test_player_handle_monster():
    p = Player()
    p.handle_monster(5)
    assert p.health == 16
    p.handle_monster(10)
    assert p.health == 6

