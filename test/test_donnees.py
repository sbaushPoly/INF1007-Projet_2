import sys
sys.path.insert(0, 'src')
import donnees
import pytest

def test_implementation_test_initial():
    assert donnees.implementation_test_initial() == True