import re
def unix_match(filename: str, pattern: str) -> bool:
    t = { '.':'\.', '*':'.*', '?':'.', '[!':'[^', '[^]':'[^.]' }
    for i, j in t.items():
        pattern = pattern.replace(i, j)
    print(pattern)
    try:
        return bool(re.search(pattern, filename))
    except re.error:
        return False

if __name__ == '__main__':
    assert unix_match('somefile.txt', 'somefile.txt') == True
    assert unix_match('1name.txt', '[!abc]name.txt') == True
    assert unix_match('log1.txt', 'log[!0].txt') == True
    assert unix_match('log1.txt', 'log[1234567890].txt') == True
    assert unix_match('log1.txt', 'log[!1].txt') == False
    assert unix_match("name.txt","name[]txt") == False
    assert unix_match("[!]check.txt","[!]check.txt") == True
    assert unix_match("checkio","[c[]heckio") == True


