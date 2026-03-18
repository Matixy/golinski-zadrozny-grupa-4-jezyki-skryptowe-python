import pytest
import io
from src.utils.textTools import cleanLine, countWords, getWord, generateSentences, findLongestSentence

# --- TESTY DLA textTools.py ---
def test_clean_line_basic():
    """Testuje usuwanie spacji i białych znaków."""
    assert cleanLine("   To jest   test   ") == "To jest test"
    assert cleanLine("\tTabulacja i  spacje\n") == "Tabulacja i spacje"


def test_count_words():
    """Testuje liczenie słów (tylko znaki alfabetu)."""
    assert countWords("Ala ma 2 koty!") == 3
    assert countWords("... --- ...") == 0
    assert countWords("") == 0


def test_get_word():
    """Testuje wyciąganie pierwszego słowa."""
    assert getWord("  Witaj, świecie!") == "Witaj"
    assert getWord("123 Liczby") == "Liczby"
    assert getWord("!!!") == ""


def test_generate_sentences_basic():
    """Testuje dzielenie na zdania po znakach interpunkcyjnych."""
    text = "Pierwsze zdanie. Drugie zdanie? Trzecie!"
    stream = io.StringIO(text) #tworzenie chwilowego wejscia
    sentences = list(generateSentences(stream))
    assert len(sentences) == 3
    assert sentences[0] == "Pierwsze zdanie."


def test_generate_sentences_paragraphs():
    """Testuje dzielenie na zdania przez akapity (2x nowa linia)."""
    text = "Zdanie pierwsze\n\nZdanie drugie bez kropki"
    stream = io.StringIO(text)
    sentences = list(generateSentences(stream))
    assert len(sentences) == 2
    assert "Zdanie drugie" in sentences[1]


def test_find_longest_sentence_with_predicate():
    """Testuje szukanie najdłuższego zdania z filtrem."""
    text = "Krótkie zdanie. To jest bardzo długie zdanie. Małe."
    stream = io.StringIO(text)

    # Szukamy najdłuższego, które ma więcej niż 3 słowa
    def more_than_3_words(s):
        return countWords(s) > 3

    result = findLongestSentence(stream, predicateFunction=more_than_3_words)
    assert "bardzo " in result



