import re


def unix_match(filename: str, pattern: str) -> bool:
    print('Filename:', filename)
    print('Pattern:', pattern)

    # regex_pattern = pattern.replace('.', '\.').replace('*', '.*').replace('?', '.') \
    #                        .replace('[][]', '[\]\[]') \
    #                        .replace('[]', '[^.]').replace('[!', '[^').replace('[^]', '\[!\]') \
    #                        .replace('[[^.][.][.*][^.]]', '\[\?\*\]')

    regex_pattern = pattern.replace('.', '\.')   \
                           .replace('*', '.*')   \
                           .replace('?', '.')    \
                           .replace('[!', '[^')  \
                           .replace('[[]', '\[') \
                           .replace('[]]', '\]') \
                           .replace('[.]', '\?') \
                           .replace('[.*]', '\*')\

    print('Regex pattern:', regex_pattern)

    try:
        full_match = re.fullmatch(regex_pattern, filename)
        if full_match:
            print(full_match.group(0))
        else:
            print('Not matched')
    except re.error:
        print('Regexp error')
        full_match = filename == pattern

    print()
    return bool(full_match)


if __name__ == '__main__':
    assert unix_match("name.txt", "name[]txt") == False
    assert unix_match("nametxt", "name[]txt") == False
    assert unix_match("1name.txt", "[!abc]name.txt") == True
    assert unix_match("[!]check.txt", "[!]check.txt") == True
    assert unix_match("[check].txt", "[][]check[][].txt") == True
    assert unix_match("[?*]", "[[][?][*][]]") == True

    assert unix_match('somefile.txt', '*') == True
    assert unix_match('other.exe', '*') == True
    assert unix_match('my.exe', '*.txt') == False
    assert unix_match('log1.txt', 'log?.txt') == True
    assert unix_match('log1.txt', 'log[1234567890].txt') == True
    assert unix_match('log12.txt', 'log?.txt') == False
    assert unix_match('log12.txt', 'log??.txt') == True
