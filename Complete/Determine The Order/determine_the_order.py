from functools import cmp_to_key, partial


def letter_comparator(a, b, pairs):
    print(f'Comparing {a} and {b}')
    if a + b in pairs:
        print(f'    {a} < {b}')
        return -1
    elif b + a in pairs:
        print(f'    {a} > {b}')
        return 1
    else:
        print(f'    {a} = {b}')
        return 0


def find_bigger_letters(letter, words):
    bigger_letters = set()
    for word in words:
        print(f'Checking \'{letter}\' in \'{word}\'')
        letter_index = word.find(letter)
        print('    Letter index:', letter_index)
        if letter_index == -1:
            continue
        bigger_letters_in_current_word = set(word[letter_index + 1:])
        print('    Bigger letters in current word:', bigger_letters_in_current_word)

        bigger_letters_in_other_words = set()
        for bigger_letter in bigger_letters_in_current_word:
            print('        Bigger letter:', bigger_letter)
            other_words = set(words) - {word}
            print('        Other words:', other_words)
            bigger_letters_in_other_words |= find_bigger_letters(bigger_letter, other_words)
            print('        Bigger letters in other words:', bigger_letters_in_other_words)

        bigger_letters |= bigger_letters_in_current_word
        bigger_letters |= bigger_letters_in_other_words
        print(f'    Returning bigger letters for \'{letter}\' in \'{word}\':', bigger_letters)
    return bigger_letters


def checkio(data):
    print('Data:', data)

    pairs = set()
    for word in data:
        for letter in word:
            print('Letter:', letter)
            bigger_letters = find_bigger_letters(letter, data)
            print(f'= Bigger letters for {letter}:', bigger_letters)
            print()
            pairs |= {letter + bigger_letter for bigger_letter in bigger_letters}
    print('Pairs:', sorted(pairs))

    letter_comparator_with_pairs = partial(letter_comparator, pairs=pairs)

    initial_string = ''.join(data)
    print('Initial string:', initial_string)
    initial_sorted = sorted(set(initial_string))
    print('Initial sorted:', initial_sorted)
    ordered_string = sorted(initial_sorted, key=cmp_to_key(letter_comparator_with_pairs))
    print('Ordered string:', ordered_string)
    output_string = ''.join(ordered_string)
    print('Output string:', output_string)
    print()

    words = sorted(''.join(sorted(set(w), key=w.index)) for w in data if w)
    print('Words:', words)
    print()

    return output_string


if __name__ == '__main__':
    assert checkio(["acb", "bd", "zwa"]) == "zwacbd", \
        "Just concatenate it"
    assert checkio(["klm", "kadl", "lsm"]) == "kadlsm", \
        "Paste in"
    assert checkio(["a", "b", "c"]) == "abc", \
        "Cant determine the order - use english alphabet"
    assert checkio(["aazzss"]) == "azs", \
        "Each symbol only once"
    assert checkio(["dfg", "frt", "tyg"]) == "dfrtyg", \
        "Concatenate and paste in"
