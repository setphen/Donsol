from game.models import Deck

def test_deck_with_seed_is_repeatable():
    d = Deck(list(range(52)), seed=847576)
    d.shuffle()
    assert d.draw(10) == [11, 24, 46, 37, 25, 47, 18, 14, 8, 39]
    d2 = Deck(list(range(52)), seed=234987)
    d2.shuffle()
    assert d2.draw(10) == [14, 17, 23, 9, 10, 24, 36, 20, 49, 7]


def test_deck_draw_removes_items():
    d = Deck(list(range(16)))
    assert len(d.cards) == 16
    d.shuffle()
    d.draw(4)
    assert len(d.cards) == 12


def test_drawing_past_end_of_deck():
    d = Deck(list(range(3)))
    drawn = d.draw(4)
    assert len(d.cards) == 0
    assert len(drawn) == 3


def test_deck_add():
    d = Deck(list(range(5)))
    assert len(d.cards) == 5
    d.add(list(range(5)))
    assert len(d.cards) == 10
