def acronym(word_list: list[str]) -> str:
    char_list = [word[0] for word in word_list]
    return "".join(char_list).upper()



def median(num_list: list[int]) -> float:
    num_list.sort()
    size = len(num_list)
    mediana = num_list[size//2] if size%2==1 else (num_list[size//2] + num_list[size//2 -1]) /2
    return mediana



def pierwiastek(x: float, epsilon: float) -> float:
    x = abs(x)
    return _newton_sqrt(x, epsilon)

def _newton_sqrt(x: float, epsilon: float, y=None) -> float:
    y = x if y is None else y
    return ( y if abs(y*y - x) < epsilon and y>=0 else _newton_sqrt(x, epsilon, (y + (x/y))/2) ) 



def make_alpha_dict(sentence: str) -> dict[str, list[str]]:
    keys = dict.fromkeys([letter for letter in sentence if letter.isalpha()]) #tworzy slownik zachowujac kolejnosc kluczy i akceptuje tylko znaki alfanumeryczne, wartosci domylsnie None
    word_list = sentence.split()

    return {key: _get_first_letter_word_list(word_list, key) for key in keys} #zwracamy slownik za pomoca listy skladanej i funkcji pomocniczej
    
def _get_first_letter_word_list(word_list: list[str], letter: str) -> list[str]:
    """Helper method for zad1 d
    Returns sorted list of words which contain inserted letter"""
    return sorted([word for word in word_list if letter in word])


def flatten(formula) -> list:
    return [formula] if not isinstance(formula, (list, tuple)) else ( [] if not formula else flatten(formula[0]) + flatten(formula[1:]))
    #Jesli pojedynczy element (nie jest instancja typu list lub tuple) to zwracamy ten element np. 5 zwraca [5]
    #W przeciwnym wypadku sprawdzamy czy jest pusty jesli tak to zwracamy pusta liste []
    #Jesli cos ma w srodku to rekurencyjnie wywolujemy flatten na glowie i ogonie ktore laczymy


def group_anagrams(word_list) -> dict[str, list[str]]:
    keys = dict.fromkeys([ _sort_word_by_letters(word) for word in word_list])
    
    return {key: _get_sorted_words_by_letter_list(word_list, key) for key in keys}

def _sort_word_by_letters(word: str) -> str:
    return "".join(sorted(word))

def _get_sorted_words_by_letter_list(word_list: list[str], key_word: str) -> list[str]:
    return [word for word in word_list if key_word == _sort_word_by_letters(word)]



def main():
    words = ["zaklad", "ubezpieczen", "spolecznych"]
    print("A) "+ acronym(words))

    nums = [1,7,2,7,2,4,3,9]
    print(f"B) Lista: {sorted(nums)} Mediana: {median(nums)}")

    print(f"C) {pierwiastek(-3, 0.01)}")

    sentence = "on i ona"
    print(f"D) {make_alpha_dict(sentence)}")

    print(f"E) {flatten([1, [2, 3], (8, []), [(4, 5), 6]])}")

    print(f"F) {group_anagrams(["kot", "tok", "pies", "kep", "pek"])}")


if __name__ == "__main__":
    main()