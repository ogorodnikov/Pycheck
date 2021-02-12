get_cookie = lambda cookie, name: [value for pair in cookie.split('; ') for key, value in [pair.split('=', maxsplit=1)] if key == name][0]


def get_cookie(cookie, name):
    print('Cookie:', cookie)
    print('Name:', name)

    pairs = cookie.split('; ')
    print('Pairs:', pairs)
    print()

    for pair in pairs:
        key, value = pair.split('=', maxsplit=1)
        print('Key:', key)
        print('Value:', value)
        if key == name:
            print('Found')
            return value


if __name__ == "__main__":
    assert get_cookie('theme=light; sessionToken=abc123', 'theme') == 'light', 'theme=light'
    assert get_cookie('_ga=GA1.2.447610749.1465220820; _gat=1; ffo=true', 'ffo') == 'true', 'ffo=true'

    assert get_cookie("USER=name=Unknown; domain=bbc.com", "USER") == 'name=Unknown'
