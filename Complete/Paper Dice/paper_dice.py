
paper_dice = lambda p: not any(l not in '1265126_1364136_2354235_5324532_6314631_6215621' for l in [r.strip() for r in p] + [''.join(c).strip() for c in zip(*p)])

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

    assert paper_dice(["    ",
                       " 3  ",
                       " 51 ",
                       " 4  ",
                       " 26 ", "    "]) is False
