from itertools import zip_longest
from math import ceil


def text_formatting(text: str, width: int, style: str) -> str:
    print('Text:', text)

    words = text.split(' ')
    print('Words:', words)

    lines = []
    rest_words = words

    while rest_words:
        print('Starting with rest:', rest_words)
        new_line_words = []
        while rest_words:
            word = rest_words[0]
            if len(' '.join(new_line_words + [word])) > width:
                break
            rest_words = rest_words[1:]
            new_line_words.append(word)

        print('    New line words:', new_line_words)
        new_line = ' '.join(new_line_words)
        print('    New line:', new_line, len(new_line))
        print('    Rest words:', rest_words)
        print()
        lines.append(new_line_words)

    print('Lines:', lines)
    print()

    if style == 'l':
        formatted_text = '\n'.join(' '.join(line) for line in lines)
    elif style == 'r':
        formatted_text = '\n'.join(' ' * (width - len(' '.join(line))) + ' '.join(line) for line in lines)
    elif style == 'c':
        formatted_text = '\n'.join(' ' * ((width - len(' '.join(line))) // 2) + ' '.join(line) for line in lines)
    elif style == 'j':
        spaces_counts = []
        for line in lines:
            print('Line:', line)
            gaps_count = len(line) - 1
            print('Gaps count:', gaps_count)
            words_len = sum(map(len, line))
            print('    Words len:', words_len)
            spaces_len = width - words_len
            print('    Spaces len:', spaces_len)

            spaces_count = []
            spaces_left = spaces_len
            gaps_count_left = gaps_count
            while spaces_left and gaps_count_left:
                spaces_per_gap = spaces_left / gaps_count_left
                print('        Spaces per gap:', spaces_per_gap)
                rounded_spaces_per_gap = ceil(spaces_per_gap)
                print('        Rounded spaces per gap:', rounded_spaces_per_gap)
                spaces_left -= rounded_spaces_per_gap
                print('        Spaces left:', spaces_left)
                spaces_count.append(rounded_spaces_per_gap)
                gaps_count_left -= 1
                print('        Gaps count left:', gaps_count_left)
                print()
            print('Spaces count:', spaces_count)
            spaces_counts.append(spaces_count)
        spaces_counts[-1] = [1 for space in spaces_counts[-1]]
        print('Spaces counts:', spaces_counts)
        print()

        formatted_lines = []
        for words, spaces_count in zip(lines, spaces_counts):
            print('Words:', words)
            print('Spaces count:', spaces_count)
            spaces = [' ' * sc for sc in spaces_count]
            print('Spaces:', spaces)
            formatted_line = ''.join(''.join(pair) for pair in zip_longest(words, spaces, fillvalue=''))
            print('Formatted line:', formatted_line)
            formatted_lines.append(formatted_line)

        formatted_text = '\n'.join(formatted_lines)

    print(formatted_text)
    print()
    return formatted_text


if __name__ == '__main__':
    LINE = ('Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iure '
            'harum suscipit aperiam aliquam ad, perferendis ex molestias '
            'reiciendis accusantium quos, tempore sunt quod veniam, eveniet '
            'et necessitatibus mollitia. Quasi, culpa.')


    assert text_formatting("Hi, my name is Alex and I am 18 years old.",20,"j")

    assert text_formatting(LINE, 38, 'l') == \
        '''Lorem ipsum dolor sit amet,
consectetur adipisicing elit. Iure
harum suscipit aperiam aliquam ad,
perferendis ex molestias reiciendis
accusantium quos, tempore sunt quod
veniam, eveniet et necessitatibus
mollitia. Quasi, culpa.''', 'Left 38'

    assert text_formatting(LINE, 30, 'c') == \
''' Lorem ipsum dolor sit amet,
consectetur adipisicing elit.
 Iure harum suscipit aperiam
  aliquam ad, perferendis ex
     molestias reiciendis
accusantium quos, tempore sunt
   quod veniam, eveniet et
   necessitatibus mollitia.
        Quasi, culpa.''', 'Center 30'

    assert text_formatting(LINE, 50, 'r') == \
        '''           Lorem ipsum dolor sit amet, consectetur
     adipisicing elit. Iure harum suscipit aperiam
   aliquam ad, perferendis ex molestias reiciendis
       accusantium quos, tempore sunt quod veniam,
 eveniet et necessitatibus mollitia. Quasi, culpa.''', 'Right 50'

    assert text_formatting(LINE, 45, 'j') == \
        '''Lorem   ipsum  dolor  sit  amet,  consectetur
adipisicing elit. Iure harum suscipit aperiam
aliquam    ad,   perferendis   ex   molestias
reiciendis  accusantium  quos,  tempore  sunt
quod   veniam,   eveniet   et  necessitatibus
mollitia. Quasi, culpa.''', 'Justify 45'