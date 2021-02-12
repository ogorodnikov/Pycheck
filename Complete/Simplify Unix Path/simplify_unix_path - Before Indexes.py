def simplify_path(path):
    print('Path:', path)

    initial_directories = path.split('/')
    print('Initial directories:', initial_directories)

    directories = [d for d in initial_directories if d not in ('', '.')]
    print('Cleared:', directories)

    is_absolute_path = path[0] == '/'
    print('Is absolute path:', is_absolute_path)

    while '..' in directories:
        double_dot_index = directories.index('..')
        print('    \'..\' found at index:', double_dot_index)
        if double_dot_index == 0 and not is_absolute_path:
            print('    --- Found double dot at index 0 for related path - breaking')
            break
        start_index = max(0, double_dot_index - 1)
        end_index = double_dot_index + 1
        print('    Removing:', directories[start_index:end_index])
        del directories[start_index:end_index]
        print('    New directories:', directories)

    joined = '/'.join(directories)
    print('Joined:', joined)

    if is_absolute_path:
        joined = '/' + joined
    if not is_absolute_path:
        if joined == '':
            joined = '.'

    result = joined
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
