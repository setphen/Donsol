from game.models import Deck


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
