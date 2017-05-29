from game.models import Deck


def test_deck_draw_removes_items():
    d = Deck(list(range(16)))
    assert len(d.cards) == 16
    d.shuffle()
    d.draw()
    assert len(d.cards) == 15


def test_deck_add():
    d = Deck(list(range(5)))
    assert len(d.cards) == 5
    d.add(list(range(5)))
    assert len(d.cards) == 10
