import re
from functools import partial, reduce

ESCAPE_SEQUENCE = r'(%..)'

UNRESERVED_RANGES = {'ALPHA 1': (0x41, 0x5A),
                     'ALPHA 2': (0x61, 0x7A),
                     'DIGIT': (0x30, 0x39),
                     'hyphen': 0x2D,
                     'period': 0x2E,
                     'underscore': 0x5F,
                     'tilde': 0x7E}

DEFAULT_PORTS = {'http': 80}


def parse_hex_ranges(hex_ranges_dict):
    decimal_digits = []
    for hex_range in hex_ranges_dict.values():
        if isinstance(hex_range, int):
            decimal_digits.append(hex_range)
        elif isinstance(hex_range, tuple):
            decimal_digits.extend(range(hex_range[0], hex_range[1] + 1))
    hex_characters = [f'{digit:X}' for digit in decimal_digits]
    return hex_characters


def escape_sequences_upper(url):
    return re.sub(ESCAPE_SEQUENCE, lambda m: m.group(0).upper(), url)


def unreserved_characters_decode(url, unreserved_characters):
    def decode_character(match_object):
        character = match_object.group(0)[1:]
        if character in unreserved_characters:
            return chr(int(character, 16)).lower()
        return match_object.group(0)

    return re.sub(ESCAPE_SEQUENCE, decode_character, url)


def remove_default_ports(initial_url):
    for protocol, port in DEFAULT_PORTS.items():
        url = re.sub(rf'({protocol}://.+\..+):{port}(\D|\Z)', r'\1\2', initial_url)
    return url


def remove_dot_segments(initial_url):
    url = initial_url
    while True:
        url, delete_count = re.subn(r'/\.(?=/)', '', url)
        url, delete_count = re.subn(r'/[^/.]+/\.\.', '', url)
        if delete_count == 0:
            return url


def checkio(url):
    print('Url:           ', url)

    characters_decode = partial(unreserved_characters_decode,
                                unreserved_characters=parse_hex_ranges(UNRESERVED_RANGES))

    rules = [str.lower,
             escape_sequences_upper,
             characters_decode,
             remove_default_ports,
             remove_dot_segments]

    normalized_url = reduce(lambda u, rule: rule(u), rules, url)

    print('Normalized url:', normalized_url)
    print()
    return normalized_url


if __name__ == '__main__':
    assert checkio("Http://Www.Checkio.org") == \
           "http://www.checkio.org", "1st rule"
    assert checkio("http://www.checkio.org/%cc%b1bac") == \
           "http://www.checkio.org/%CC%B1bac", "2nd rule"
    assert checkio("http://www.checkio.org/task%5F%31") == \
           "http://www.checkio.org/task_1", "3rd rule"
    assert checkio("http://www.checkio.org:80/home/") == \
           "http://www.checkio.org/home/", "4th rule"
    assert checkio("http://www.checkio.org:8080/home/") == \
           "http://www.checkio.org:8080/home/", "4th rule again"
    assert checkio("http://www.checkio.org:80") == \
           "http://www.checkio.org"
    assert checkio("http://www.checkio.org/task/./1/../2/././name") == \
           "http://www.checkio.org/task/2/name", "5th rule"

    assert checkio("HTTP://EXAMPLE.COM:80") == "http://example.com"
    assert checkio("http://example.com:80/HOME/../././Guest/1/../2/..") == "http://example.com/guest"
    assert checkio("http://example.com:80/HOME/GARDEN/../././Guest/1/../2/..") == "http://example.com/home/guest"

    assert checkio("http://example.com/a/b/c/d/../../") == "http://example.com/a/b/"
    assert checkio("http://example.com:80/a/b/c/d/../../../..") == "http://example.com"
