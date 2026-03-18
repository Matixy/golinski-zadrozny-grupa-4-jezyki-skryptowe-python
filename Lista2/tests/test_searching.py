import pytest
import io
import sys
from src.utils.textTools import findLongestSentence
from src.searchingFunctions.findLongestSentenceWithoutSameStartingAdjacentLetters import (isValidSentenceWithoutSameStartingAdjacentLetters, main)
from src.searchingFunctions.findFirstSentenceWithMultipleCommas import findFirstComplexSentence

# Testy dla findFirstSentenceWithMultipleCommas.py
@pytest.fixture
def multi_comma_text():
    return (
        "To jest proste zdanie bez przecinków.\n"
        "To zdanie, jak widać, ma dokładnie dwa przecinki.\n" # To powinno zostać zwrócone
        "To zdanie, choć ma, bardzo, wiele, przecinków, jest drugie w kolejności."
    )

def test_find_first_complex_sentence_success(multi_comma_text):
    stream = io.StringIO(multi_comma_text)
    result = findFirstComplexSentence(stream)
    assert result == "To zdanie, jak widać, ma dokładnie dwa przecinki."    #Sprawdzamy czy to na pewno to konkretne zdanie
    assert result.count(',') == 2  #Upewniamy się, że ma więcej niż 1 przecinek


def test_find_first_complex_sentence_not_found():
    text = "Zdanie bez przecinka. Zdanie, z jednym przecinkiem."    #zdania z 0 i 1 przecinkiem (warunek > 1 nie zostanie spełniony)
    stream = io.StringIO(text)
    with pytest.raises(ValueError) as e:
        findFirstComplexSentence(stream)
    assert "W tekście nie znaleziono zdania z więcej niż jednym przecinkiem" in str(e.value) # Sprawdzamy czy komunikat błędu jest taki, jak w kodzie


# Testy dla findFirstSentenceWithMultipleCommas.py
def test_check_each_sentence_logic():
    """Sprawdzamy każde zdanie z osobna, żeby potwierdzić logikę filtra."""

    s1 = "Biały bocian brodzi po błocie."
    assert isValidSentenceWithoutSameStartingAdjacentLetters(s1) is False

    s2 = "Ala ma kota."
    assert isValidSentenceWithoutSameStartingAdjacentLetters(s2) is True

    s3 = "Cicha noc, ciemna, noc."
    assert isValidSentenceWithoutSameStartingAdjacentLetters(s3) is True



# Testy dla findLongestSentence.py
@pytest.fixture
def mixed_sentences_stream():
    text = (
        "To jest krótkie.\n" 
        "To jest najdłuższe zdanie w zestawie.\n"  
        "A to jest średniej zdanie."
    )
    return io.StringIO(text)

def test_find_longest_no_filter(mixed_sentences_stream):
    result = findLongestSentence(mixed_sentences_stream)
    assert result == "To jest najdłuższe zdanie w zestawie."
