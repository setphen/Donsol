from game.models import Player, Shield

def test_player_handle_monster():
    p = Player()
    p.handle_monster(5)
    assert p.health == 16
    p.handle_monster(10)
    assert p.health == 6


def test_player_handle_monster_with_shield():
    p = Player()
    p.shield = Shield(8)
    p.handle_monster(10)
    assert p.health == 19
    assert p.shield.previous_value == 10


def test_player_shield_breaks():
    p = Player()
    p.shield = Shield(3)
    p.handle_monster(3)
    p.handle_monster(3)
    assert p.shield is None
