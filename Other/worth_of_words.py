VALUES = {'e': 1,  'a': 1, 'i': 1, 'o': 1, 'n': 1, 'r': 1,
          't': 1,  'l': 1, 's': 1, 'u': 1, 'd': 2, 'g': 2,
          'b': 3,  'c': 3, 'm': 3, 'p': 3, 'f': 4, 'h': 4,
          'v': 4,  'w': 4, 'y': 4, 'k': 5, 'j': 8, 'x': 8,
          'q': 10, 'z': 10}


def get_word_value(word):
    return sum(VALUES[letter] for letter in word)


def worth_of_words(words):
    print('Words:', words)
    most_worthy_word = max(words, key=get_word_value)
    print('Most worthy word:', most_worthy_word)
    print()
    return most_worthy_word


if __name__ == '__main__':
    assert worth_of_words(['hi', 'quiz', 'bomb', 'president']) == 'quiz'
    assert worth_of_words(['zero', 'one', 'two', 'three', 'four', 'five']) == 'zero'

