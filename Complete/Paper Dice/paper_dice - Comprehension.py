PERIMETERS = ('1265126_1364136_2354235')


def paper_dice(paper):
    print('Paper:', paper)
    rows = [row.strip() for row in paper]
    print('Rows:', rows)
    columns = [''.join(c).strip() for c in zip(*paper)]
    print('Columns:', columns)
    print('PERIMETERS:', PERIMETERS)

    if any(line not in PERIMETERS and line[::-1] not in PERIMETERS for line in rows + columns):
        print('Not found')
        print()
        return False
    else:
        print('Found')

    print('All matched')
    print()
    return True


if __name__ == '__main__':
    assert paper_dice([
                '  1  ',
                ' 235 ',
                '  6  ',
                '  4  ']) is True, 'cross'
    assert paper_dice([
                '    ',
                '12  ',
                ' 36 ',
                '  54',
                '    ']) is True, 'zigzag'
    assert paper_dice(['123456']) is False, '1 line'
    assert paper_dice([
                '123  ',
                '  456']) is False, '2 lines_wrong'
    assert paper_dice([
                '126  ',
                '  354']) is True, '2 lines_right'

    assert paper_dice(["     ",
                       "  63 ",
                       " 45  ",
                       "  1  ",
                       "  2  ",
                       "     "]) is True

    assert paper_dice(["    ", " 3  ", " 51 ", " 4  ", " 26 ", "    "]) is False