from collections import namedtuple, defaultdict
from functools import reduce
from itertools import groupby, product
from operator import and_

Row = namedtuple('Row', ['os', 'xs', 'qs'])


def str_to_row(row_string):
    row_dict = defaultdict(set)
    for i, l in enumerate(row_string):
        row_dict[l] |= {i}
    row = Row(row_dict['O'], row_dict['X'], row_dict['?'])
    return row


def row_to_str(row):
    if not row:
        return None
    os, xs, qs = row
    row_string = ''
    for l in range(sum(map(len, row))):
        if l in os:
            row_string += 'O'
        elif l in xs:
            row_string += 'X'
        elif l in qs:
            row_string += '?'
        else:
            row_string += '_'
    return row_string


def row_clue_match(row, clues):
    row_string = row_to_str(row)
    row_groups = groupby(row_string)
    row_o_group_lens = [len(list(g)) for k, g in row_groups if k == 'O']
    return row_o_group_lens == clues


def get_clue_placements(row_string, clues):
    row = str_to_row(row_string)
    row_set = row.os | row.xs | row.qs

    positions = list(product(row.qs | row.os, repeat=len(clues)))

    for position in positions:
        current_row = row

        for clue, q in zip(clues, position):

            clue_os = set(range(q, q + clue))
            clue_xs = {q - 1, q + clue}

            new_os = (current_row.os | clue_os) & row_set
            new_xs = (current_row.xs | clue_xs) & row_set
            new_qs = current_row.qs - new_os - new_xs

            if new_os & current_row.xs:
                break
            if new_xs & current_row.os:
                break

            new_row = Row(new_os, new_xs, new_qs)
            current_row = new_row

        if row_clue_match(current_row, clues):
            yield current_row


def intersect_rows(rows):
    if not rows:
        return None
    row_set = rows[0].os | rows[0].xs | rows[0].qs
    final_os = reduce(and_, (row.os for row in rows))
    final_xs = reduce(and_, (row.xs | row.qs for row in rows))
    final_qs = row_set - final_os - final_xs
    return Row(final_os, final_xs, final_qs)
        

def nonogram_row(row_string, clue_numbers):
    print('Clue numbers:', clue_numbers)
    print('Row string:', row_string)
    valid_clues = list(filter(None, clue_numbers))

    placements = list(get_clue_placements(row_string, valid_clues))
    for placement in placements:
        print('Placement: ', row_to_str(placement))

    intersect_string = row_to_str(intersect_rows(placements))
    print('Intersect: ', intersect_string)
    print()
    return intersect_string


if __name__ == '__main__':
    assert nonogram_row('??????????', [8]) == '??OOOOOO??', 'Simple boxes_1'
    assert nonogram_row('???????????X?????X????', [6]) == '?????O?????XXXXXXXXXXX'
    assert nonogram_row('??????????', [4, 3]) == '??OO???O??', 'Simple boxes_2'
    assert nonogram_row('???O????O?', [3, 1]) == 'X??O??XXOX', 'Simple spaces'
    assert nonogram_row('????X?X???', [3, 2]) == '?OO?XXX?O?', 'Forcing'
    assert nonogram_row('O?X?O?????', [1, 3]) == 'OXX?OO?XXX', 'Glue'
    assert nonogram_row('??OO?OO???O?O??', [5, 2, 2]) == 'XXOOOOOXXOOXOOX', 'Joining and splitting'
    assert nonogram_row('????OO????', [4]) == 'XX??OO??XX', 'Mercury'
    assert nonogram_row('?????', []) == 'XXXXX', 'Empty_2'
    assert nonogram_row('???X?', [0]) == 'XXXXX', 'Empty_1'
    assert nonogram_row('??X??', [3]) is None, 'Wrong string'
