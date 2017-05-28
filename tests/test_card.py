from game.models import Card

def test_card_creation_without_name():
    c = Card('heart', 5)
    assert c.name == 'heart'
    assert c.suit == 'heart'
    assert c.value == 5


def test_card_creation_with_name():
    c = Card('spade', 5, name='jabberwock')
    assert c.name == 'jabberwock'
    assert c.suit == 'spade'
    assert c.value == 5


def test_card_spade_is_monster():
    c = Card('spade', 5)
    assert c.is_monster() == True


def test_card_club_is_monster():
    c = Card('club', 5)
    assert c.is_monster() == True

