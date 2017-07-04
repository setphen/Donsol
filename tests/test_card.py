from game.models import (Card,
                         HEART,
                         SPADE,
                         CLUB,
                         DIAMOND)

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
    c = Card(SPADE, 5)
    assert c.is_monster() == True


def test_card_club_is_monster():
    c = Card(CLUB, 5)
    assert c.is_monster() == True


def test_card_heart_is_not_monster():
    c = Card(HEART, 5)
    assert c.is_monster() == False


def test_card_diamond_is_not_monster():
    c = Card(DIAMOND, 5)
    assert c.is_monster() == False
