from re import findall


def repeat_inside(line):
    print('Line:', line)

    repeats = findall(r'(?=((.+?)\2+))', line)
    print('Repeats:', repeats)
    longest_repeat = max((repeat for repeat, part in repeats), key=len, default='')
    print('Longest repeat:', longest_repeat)
    print()
    return longest_repeat


if __name__ == '__main__':
    assert repeat_inside('rghtyjdfrtdfdf56r') == 'dfdf'
    assert repeat_inside('aaaaa') == 'aaaaa', "First"
    assert repeat_inside('aabbff') == 'aa', "Second"
    assert repeat_inside('aababcc') == 'abab', "Third"
    assert repeat_inside('abc') == '', "Forth"
    assert repeat_inside('abcabcabab') == 'abcabc', "Fifth"
