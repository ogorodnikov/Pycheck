from typing import Set, Iterable
from collections import deque

CLOCKWISE_EVEN = (0, -1), (1, -1), (1, 0), (0, 1), (-1, 0), (-1, -1)
CLOCKWISE_ODD = (0, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)


def get_border(a, border_cells, return_contours=False):
    contours = set()
    border = {a}
    q = deque([a])
    while q:
        a = q.pop()
        ax = ord(a[0]) - 65
        ay = int(a[1:])
        # shift of deltas for even column
        if ax % 2:
            deltas = CLOCKWISE_ODD
        else:
            deltas = CLOCKWISE_EVEN
        for dx, dy in deltas:
            bx = ax + dx
            by = ay + dy
            b = chr(bx + 65) + str(by)
            if b not in border_cells:
                contours.add(b)
                continue
            if 'A' > b[0] or b[0] > 'L':
                continue
            if by < 1 or by > 9:
                continue
            if b in border:
                continue
            q.append(b)
            border.add(b)
    border, contours = map(sorted, map(list, (border, contours)))
    if return_contours:
        return border, contours
    else:
        return border


def parse_borders(border_cells, return_contours=False):
    parsed_borders = []
    parsed_contours = []
    for a in (border_cells):
        if any(a in parsed_border for parsed_border in parsed_borders):
            continue
        if return_contours:
            new_border, contours = get_border(a, border_cells, return_contours=True)
            parsed_borders.append(new_border)
            parsed_contours.append(parse_borders(contours))
        else:
            new_border = get_border(a, border_cells)
            parsed_borders.append(new_border)
    if return_contours:
        return parsed_borders, parsed_contours
    else:
        return parsed_borders


def get_area(border_cells):
    print('    Calculating area for:', border_cells)
    borders, contours = parse_borders(border_cells, return_contours=True)
    print('    Got borders, contours:', borders, contours)
    if len(*contours) == 1:
        print('        Only 1 contour, returning:', len(border_cells))
        return len(border_cells)
    else:
        print('        2 or more contours')
        smaller_contour = min(*contours, key=len)
        print('        Smaller contour:', smaller_contour)
        sub_area = get_area(smaller_contour)
        print('        Sub-area:', sub_area)
        print('        Plus contour area:', len(border_cells))
        print('        Returning:', sub_area + len(border_cells))
        return sub_area + len(border_cells)


###   main method   ###

def hexagonal_islands(coasts: Set[str]) -> Iterable[int]:
    # initial parse
    borders, contours = parse_borders(coasts, return_contours=True)

    areas = []
    for border, contour in zip(borders, contours):
        print('Border:', border)
        print('Parsed contour:', contour)
        area = get_area(border)
        areas.append(area)
        print()

    areas.sort()
    print('Areas:', areas)
    print()
    return areas


if __name__ == '__main__':
    assert (sorted(hexagonal_islands(['A1', 'A2', 'A3', 'A4', 'B1', 'B4', 'C2', 'C5', 'D2', 'D3', 'D4', 'D5',
                                      'H6', 'H7', 'H8', 'I6', 'I9', 'J5', 'J9', 'K6', 'K9', 'L6', 'L7', 'L8']))) == [16,
                                                                                                                     19]

    assert (sorted(hexagonal_islands(['C5', 'E5', 'F4', 'F5', 'H4', 'H5', 'I4', 'I6', 'J4', 'J5', 'G9']))) == [1, 1, 3,
                                                                                                               7]

    print('The local tests are done. Click on "Check" for more real tests.')
