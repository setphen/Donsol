from game.models import Shield

def test_new_shield_handle_monster_under_value():
    s = Shield(8)
    damage = s.handle_monster(6)
    assert damage == 0
    assert s.previous_value == 6

def test_new_shield_handle_monster_over_value():
    s = Shield(5)
    damage = s.handle_monster(10)
    assert damage == 5
    assert s.previous_value == 10

def test_shield_breaking():
    s = Shield(10)
    damage = s.handle_monster(8)
    assert damage == 0
    damage = s.handle_monster(13)
    assert s.value == 0
    assert damage == 13



