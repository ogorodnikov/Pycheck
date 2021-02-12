def longest_palindromic(a):
    print('A:', a)

    longest_palindrome = ''
    for center, letter in enumerate(a):
        print('Center, letter:', (center, letter))
        left = right = center
        while left >= 0 and right < len(a) and a[left] == a[right]:
            print('    Left, right:', (left, right))
            if right - left + 1 > len(longest_palindrome):
                longest_palindrome = a[left:right + 1]
                print('    = New longest palindrome:', longest_palindrome)
            left -= 1
            right += 1
    print('Longest palindrome:', longest_palindrome)

    return longest_palindrome


if __name__ == '__main__':
    assert longest_palindromic('abc') == 'a'
    assert longest_palindromic('abacada') == 'aba'
    assert longest_palindromic('artrartrt') == 'rtrartr'
    assert longest_palindromic('aaaaa') == 'aaaaa'
