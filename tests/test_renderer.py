import pytest
import logging
import sys
from game.models import GameLogHandler

@pytest.fixture
def handler():
    return GameLogHandler()

def test_log(handler):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    log.addHandler(handler)
    log.info('hello!')
    print(handler.history)
    print(log.getEffectiveLevel())
    assert len(handler.history) > 0
