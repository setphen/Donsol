from game.models import Player, Shield


def test_player_handle_monster():
    p = Player()
    p.handle_monster(5)
    assert p.health == 16
    p.handle_monster(10)
    assert p.health == 6


def test_player_handle_monster_with_shield():
    p = Player()
    p.equip_shield(8)
    p.handle_monster(10)
    assert p.health == 19
    assert p.shield.previous_value == 10


def test_player_shield_breaks():
    p = Player()
    p.equip_shield(3)
    p.handle_monster(3)
    p.handle_monster(3)
    assert p.shield is None


def test_player_equip_shield():
    p = Player()
    p.equip_shield(4)
    p.handle_monster(4)
    assert p.health == 21

def test_player_drink_potion_heals():
    p = Player()
    p.health = 15
    p.drink_potion(5)
    assert p.health == 20
