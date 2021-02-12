def get_slices(piece):
    slices = sum(([x, y] for x, y in zip(piece, piece[1:])), [])
    return slices


def pieces_match(up, down):
    sums_of_heights = [x + y for x, y in zip(up, down)]
    return len(set(sums_of_heights)) <= 1


def broken_window(pieces):
    tick = 0
    q = [([], [], [], [], list(enumerate(pieces)))]
    while q:
        up, down, up_indexes, down_indexes, spare_pieces = q.pop()
        tick += 1
        
        print('Up:          ', up)
        print('Down:        ', down)
        print('Up indexes:  ', up_indexes)
        print('Down indexes:', down_indexes)
        print('Spare pieces:', spare_pieces)

        if not pieces_match(up, down):
            continue
        if not spare_pieces and len(up) == len(down):
            print('Fitting pieces:', up_indexes, down_indexes)
            print('Tick:', tick)
            return up_indexes, down_indexes

        for k in range(len(spare_pieces)):
            current_index, current_piece = spare_pieces[k]
            new_spare_pieces = spare_pieces[:k] + spare_pieces[k + 1:]
            if len(up) < len(down):
                slices = get_slices(current_piece[::-1])
                q.append((up + slices, down, up_indexes + [current_index], down_indexes, new_spare_pieces))
            else:
                slices = get_slices(current_piece)
                q.append((up, down + slices, up_indexes, down_indexes + [current_index], new_spare_pieces))


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

    # assert checker(broken_window, [[0, 1], [0, 1]])  # [0], [1]
    #
    # assert checker(broken_window, [[4, 0], [0, 1, 4, 0], [3, 0], [0, 3, 4, 1]])  # ([1, 2], [0, 3])
    #
    # assert checker(broken_window, [[0, 3, 4, 1], [4, 0], [3, 0], [0, 1, 4, 0]])
    #
    # assert checker(broken_window, [[1, 1], [1, 1], [1, 1], [1, 1]])
    #
    # assert checker(broken_window,
    #                [[0, 5, 5], [2, 4, 0], [0, 1, 1, 3, 3, 0], [4, 7, 3, 5, 3, 2, 2, 2, 7, 4, 4, 6, 6, 7], [0, 3],
    #                 [5, 5, 4, 2]])  # ([4,1,5,0,2], [3])
    #
    # assert checker(broken_window,
    #                [[7, 4, 2, 2, 2, 1, 3, 6, 4, 1, 0], [0, 5, 6], [1, 2, 7, 6, 3, 1, 4, 6, 5, 5, 5, 3, 0]])
    #
    # assert checker(broken_window,
    #                [[0, 4], [3, 2, 4, 0], [0, 3, 0], [0, 4, 3, 3, 3], [0, 4], [0, 2, 1, 1, 1, 0], [4, 0], [0, 4, 1, 4]])
