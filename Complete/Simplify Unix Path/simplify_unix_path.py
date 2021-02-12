def simplify_path(path):
    print('Path:', path)

    directories = [d for d in path.split('/') if d not in ('', '.')]
    print('Cleared:', directories)

    is_absolute_path = path[0] == '/'
    print('Is absolute path:', is_absolute_path)

    new_directories = []
    for i, directory in enumerate(directories):
        print('    Index:', i)
        print('    Directory:', directory)
        if directory == '..':
            is_first = all(directory == '..' for directory in new_directories)
            print('        Is first:', is_first)
            if is_first and not is_absolute_path:
                print('        First .. in relative path - writing')
                new_directories.append('..')
            else:
                del new_directories[-1:]
        else:
            new_directories.append(directory)
    print('Complete new directories:', new_directories)

    result = '/'.join(new_directories)

    if is_absolute_path:
        result = '/' + result
    if not is_absolute_path and result == '':
        result = '.'

    print('Result:', result)
    print()
    return result


if __name__ == '__main__':
    # last slash is not important
    assert simplify_path('/a/') == '/a'

    # double slash can be united in one
    assert simplify_path('/a//b/c') == '/a/b/c'

    # double dot - go to previous folder
    assert simplify_path('dir/fol/../no') == 'dir/no'
    assert simplify_path('dir/fol/../../no') == 'no'

    # one dot means current dir
    assert simplify_path('/a/b/./ci') == '/a/b/ci'
    assert simplify_path('vi/..') == '.'
    assert simplify_path('./.') == '.'

    # you can't go deeper than root folder
    assert simplify_path('/for/../..') == '/'
    assert simplify_path('/for/../../no/..') == '/'

    # not all double-dots can be simplified in related path
    assert simplify_path('for/../..') == '..'
    assert simplify_path('../foo') == '../foo'
    assert simplify_path(".././..") == '../..'
    assert simplify_path("../foo/../foo") == '../foo'
