import pytest
import io
import sys

# import funkcji do testu
from src.reducingFunctions.countChars import countChars
from src.reducingFunctions.countParagraphs import countParagraphs
from src.reducingFunctions.countPercentProperNames import countPercentProperNames

# przygotowanie danych tekstowych
@pytest.fixture
def processed_text():
    return (
        "\nTo jest pierwszy akapit. Zawiera on Nazwę własną nawet Dwie.\n"
        "To jest drugi akapit. Nie zawiera nic specjalnego.\n\n"
        "Trzeci akapit i koniec.\n"
    )

# test dla funkcji zliczającej znaki (bez bialych)
def test_count_chars(monkeypatch, processed_text):
    monkeypatch.setattr('sys.stdin', io.StringIO(processed_text))
    
    # znaki = 114
    assert countChars(sys.stdin) == 114

# test dla funkcji zliczającej akapity
def test_count_paragraphs(monkeypatch, processed_text):
    monkeypatch.setattr('sys.stdin', io.StringIO(processed_text))
    
    # akapity = 3
    assert countParagraphs(sys.stdin) == 3

# test dla funkcji liczącej procent zadan z nazwami własnymi
def test_count_percent_proper_names(monkeypatch, processed_text):
    monkeypatch.setattr('sys.stdin', io.StringIO(processed_text))
    
    # procent zdan z nazwami wlasnymi 20%
    assert countPercentProperNames(sys.stdin) == pytest.approx(20)