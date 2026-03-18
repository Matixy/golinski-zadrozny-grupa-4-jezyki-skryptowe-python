import pytest
import io
import sys
import os

from src.filterFunctions.getSelectedSentences import getSelectedSentences
from src.filterFunctions.getQuestionsAndExclamationsSenteces import getQuestionsAndExclamationsSenteces
from src.filterFunctions.getMax4WordsSentences import getMax4WordsSentences
from src.filterFunctions.getFirst20Sentences import getFirst20Sentences

@pytest.fixture
def sample_text():
    return (
        "Ala ma kota. "                                 # 3 wyrazy kropka
        "Oto jest piękny pies! "                        # 4 wyrazy wykrzyknik
        "Czy to jest prawda? "                          # 4 wyrazy pytajnik
        "To jest bardzo bardzo bardzo długie zdanie. "  # 6 wyrazow
        "i oraz ale że lub."                            # 5 slow kluczowych
    )

def test_get_selected_sentences(sample_text):
    stream = io.StringIO(sample_text)
    result = getSelectedSentences(stream, 2)
    
    #Wynik "i oraz ale że lub."
    assert "i oraz ale że lub." in result
    assert "Ala ma kota." not in result

def test_get_questions_and_exclamations(sample_text):
    stream = io.StringIO(sample_text)
    result = getQuestionsAndExclamationsSenteces(stream)
    
    #Wynik: "Oto jest piękny pies!" i "Czy to jest prawda?"
    assert "Oto jest piękny pies!" in result
    assert "Czy to jest prawda?" in result
    assert "Ala ma kota." not in result

def test_get_max_4_words(sample_text):
    stream = io.StringIO(sample_text)
    result = getMax4WordsSentences(stream)
    
    #Wynik "Ala ma kota. " 
    assert "Ala ma kota." in result
    assert "To jest bardzo bardzo bardzo długie zdanie." not in result

def test_get_first_20_sentences(sample_text):
    # stworzenie tekstu z 25 zdaniami "Zadanie. "
    text = "Zdanie. \n" * 25
    stream = io.StringIO(text)
    
    result = getFirst20Sentences(stream)
    
    #Wynik = 20
    assert result.count("Zdanie.") == 20