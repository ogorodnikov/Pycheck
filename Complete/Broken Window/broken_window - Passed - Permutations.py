from itertools import permutations
from typing import List, Tuple


def get_heights(pieces, side):
    side_heights = []
    for piece in pieces:
        heights = []
        for i in range(1, len(piece)):
            heights.extend(piece[i - 1:i + 1])
        if side == 'down':
            side_heights.extend(heights)
        elif side == 'up':
            side_heights.extend(list(reversed(heights)))
    return side_heights


def get_pairs(piece, side):
    for i in range(1, len(piece)):
        if side == 'down':
            yield piece[i - 1], piece[i]
        elif side == 'up':
            yield piece[i], piece[i - 1]


def broken_window(pieces: List[List[int]]) -> Tuple[List[int], List[int]]:
    print('Pieces:', *pieces)
    window_length = sum(len(piece) - 1 for piece in pieces) // 2
    print('Window length:', window_length)

    # if pieces == [[0, 1], [0, 5, 1, 0], [1, 6, 3], [4, 3], [1, 1, 4, 0], [0, 3, 2], [3, 6, 2, 5, 5, 6, 5, 1, 6, 0],
    #                     [0, 5], [3, 0], [6, 0]]:
    #     result = [7, 8, 5, 4, 0, 1, 9], [2, 3, 6]
    #     print('=== Workaround:', result)
    #     return result

    index_permutations = permutations(range(len(pieces)))
    fitted_permutations = []

    for index_permutation in index_permutations:
        print('Index permutation:', index_permutation)
        pieces_permutation = [pieces[i] for i in index_permutation]
        print('Pieces permutation:', pieces_permutation)

        for down_pieces_count in range(1, len(pieces_permutation)):
            down_pieces = pieces_permutation[:down_pieces_count]
            down_indexes = index_permutation[:down_pieces_count]
            down_pieces_length = sum(len(piece) - 1 for piece in down_pieces)

            print('    Down pieces:       ', down_pieces)
            print('    Down indexes:      ', down_indexes)
            print('    Down pieces length:', down_pieces_length)

            if down_pieces_length > window_length:
                break
            elif down_pieces_length == window_length:
                up_pieces = pieces_permutation[down_pieces_count:]
                up_indexes = index_permutation[down_pieces_count:]

                up_heights = get_heights(up_pieces, 'up')
                down_heights = get_heights(down_pieces, 'down')

                heights_sum_vector = [up_height + down_height for up_height, down_height in
                                      zip(up_heights, down_heights)]

                print('    Down heights:', down_heights)
                print('    Up pieces:       ', up_pieces)
                print('    Up indexes:      ', up_indexes)
                print('    Up heights:      ', up_heights)
                print('    Sum vector:      ', heights_sum_vector)

                if all(heights_sum == heights_sum_vector[0] for heights_sum in heights_sum_vector):
                    print('    === Adding fitting pieces: ', [up_pieces, down_pieces])
                    print('    === Adding fitting indexes:', [up_indexes, down_indexes])
                    fitted_indexes = list(up_indexes), list(down_indexes)

                    print('Result:', fitted_indexes)
                    print()
                    return fitted_indexes

    print('Unfortunately, no fitting pieces found')
    return ()


if __name__ == '__main__':

    def checker(func, pieces):
        answer = func(pieces)

        if not (isinstance(answer, (tuple, list))
                and len(answer) == 2
                and isinstance(answer[0], list) and isinstance(answer[1], list)):
            print('wrong type:', answer)
            return False

        if set(answer[0] + answer[1]) != set(range(len(pieces))):
            print('wrong value:', answer)
            return False

        tops = [list(reversed(pieces[t])) for t in answer[0]]
        bottoms = [pieces[b] for b in answer[1]]
        height = set()

        top = tops.pop(0)
        bottom = bottoms.pop(0)
        while True:
            height |= set(map(sum, zip(top, bottom)))
            if len(top) < len(bottom) and tops:
                bottom = bottom[len(top) - 1:]
                top = tops.pop(0)
            elif len(top) > len(bottom) and bottoms:
                top = top[len(bottom) - 1:]
                bottom = bottoms.pop(0)
            elif len(top) == len(bottom):
                if tops and bottoms:
                    top = tops.pop(0)
                    bottom = bottoms.pop(0)
                elif not tops and not bottoms:
                    break
                else:
                    return False
            else:
                return False

        return len(height) == 1

    assert checker(broken_window,
                   [[0, 1], [0, 5, 1, 0], [1, 6, 3], [4, 3], [1, 1, 4, 0], [0, 3, 2], [3, 6, 2, 5, 5, 6, 5, 1, 6, 0],
                    [0, 5], [3, 0], [6, 0]])

    assert checker(broken_window, [[0, 1], [0, 1]])  # [0], [1]

    assert checker(broken_window, [[4, 0], [0, 1, 4, 0], [3, 0], [0, 3, 4, 1]])  # ([1, 2], [0, 3])

    assert checker(broken_window, [[0, 3, 4, 1], [4, 0], [3, 0], [0, 1, 4, 0]])

    assert checker(broken_window, [[1, 1], [1, 1], [1, 1], [1, 1]])

    assert checker(broken_window,
                   [[0, 5, 5], [2, 4, 0], [0, 1, 1, 3, 3, 0], [4, 7, 3, 5, 3, 2, 2, 2, 7, 4, 4, 6, 6, 7], [0, 3],
                    [5, 5, 4, 2]])  # ([4,1,5,0,2], [3])

    assert checker(broken_window,
                   [[7, 4, 2, 2, 2, 1, 3, 6, 4, 1, 0], [0, 5, 6], [1, 2, 7, 6, 3, 1, 4, 6, 5, 5, 5, 3, 0]])

    assert checker(broken_window,
                   [[0, 4], [3, 2, 4, 0], [0, 3, 0], [0, 4, 3, 3, 3], [0, 4], [0, 2, 1, 1, 1, 0], [4, 0], [0, 4, 1, 4]])


