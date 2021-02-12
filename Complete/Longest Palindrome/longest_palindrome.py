def longest_palindromic(a):
    return next(a[start:start + delta + 1]
                for delta in range(len(a), -1, -1)
                for start in range(len(a) - delta)
                if a[start:start + delta + 1] == a[start:start + delta + 1][::-1])

if __name__ == '__main__':
    assert longest_palindromic('abc') == 'a'
    assert longest_palindromic('abacada') == 'aba'
    assert longest_palindromic('artrartrt') == 'rtrartr'
    assert longest_palindromic('aaaaa') == 'aaaaa'
