from collections import deque, namedtuple
from itertools import combinations


def print_history(history):
    for i, line in enumerate(history):
        print(f'{i + 1:2} {line[3]:20} {line[0]:5} _ {line[1]:5} _ {line[2]:5}')


def river_crossing(wolves, goats, cabbages, payload):
    #    Left, Boat, Right = (namedtuple(name, 'w, g, c', defaults = [0, 0, 0])
    #                                     for name in ['Left', 'Boat', 'Right'])
    #    left, boat, right = Left(w=wolves, g=goats, c=cabbages), Boat(), Right()

    left = 'W' * wolves + 'G' * goats + 'C' * cabbages
    boat = ''
    right = ''
    state = 'Unloaded to left'
    history = [[left, boat, right, state]]
    min_path = []
    min_path_len = 9999
    level = 0
    q = deque([[left, boat, right, state, history, level]])

    while q:
        left, boat, right, state, history, level = q.popleft()

        if level > 30: break

        if state == 'Unloaded to left':

            # loading left to boat
            for new_left_to_boat_count in range(0, payload + 1 - len(boat)):
                for new_left_to_boat in list(set(combinations(left, new_left_to_boat_count))):
                    new_left = left
                    new_boat = boat + ''.join(new_left_to_boat)
                    new_right = right
                    for passenger in new_left_to_boat:
                        new_left = new_left.replace(passenger, '', 1)
                    state = 'Loaded from left'
                    #                    print(f'    {state} {level}: {new_left} > {new_boat} _ {new_right}')

                    if 'G' in new_left and ('W' in new_left or 'C' in new_left):
                        #                        print('        Warning on Left')
                        continue
                    if len(history) > min_path_len:
                        #                        print('        Shorter path exists:', len(history), min_path_len)
                        continue
                    if [new_left, new_boat, new_right, state] in history:
                        #                        print('        Already in history')
                        continue
                    q.append([new_left, new_boat, new_right, state,
                              history + [[new_left, new_boat, new_right, state]], level + 1])

        elif state == 'Loaded from left':

            # unloading boat to right
            for new_boat_to_right_count in range(0, len(boat) + 1):
                for new_boat_to_right in list(set(combinations(boat, new_boat_to_right_count))):
                    new_left = left
                    new_boat = boat
                    new_right = right + ''.join(new_boat_to_right)
                    for passenger in new_boat_to_right:
                        new_boat = new_boat.replace(passenger, '', 1)

                    # victory condition
                    if new_left == '' and new_boat == '':
                        #                        print('!!! Victory')
                        path_len = len(history)
                        if path_len < min_path_len:
                            min_path = history
                            min_path_len = path_len

                    state = 'Unloaded to right'
                    #                    print(f'    {state} {level}: {new_left} _ {new_boat} > {new_right}')
                    if len(history) > min_path_len:
                        #                        print('        Shorter path exists:', len(history), min_path_len)
                        continue
                    if [new_left, new_boat, new_right, state] in history:
                        #                        print('        Already in history')
                        continue
                    q.append([new_left, new_boat, new_right, state,
                              history + [[new_left, new_boat, new_right, state]], level + 1])

        elif state == 'Unloaded to right':

            # loading right to boat
            for new_right_to_boat_count in range(0, payload + 1 - len(boat)):
                for new_right_to_boat in list(set(combinations(right, new_right_to_boat_count))):
                    new_left = left
                    new_boat = boat + ''.join(new_right_to_boat)
                    new_right = right
                    for passenger in new_right_to_boat:
                        new_right = new_right.replace(passenger, '', 1)
                    state = 'Loaded from right'
                    #                    print(f'    {state} {level}: {new_left} _ {new_boat} < {new_right}')

                    if 'G' in new_right and ('W' in new_right or 'C' in new_right):
                        #                        print('        Warning on Right')
                        continue
                    if len(history) > min_path_len:
                        #                        print('        Shorter path exists:', len(history), min_path_len)
                        continue
                    if [new_left, new_boat, new_right, state] in history:
                        #                        print('        Already in history')
                        continue
                    q.append([new_left, new_boat, new_right, state,
                              history + [[new_left, new_boat, new_right, state]], level + 1])

        elif state == 'Loaded from right':

            # unloading boat to left
            for new_boat_to_left_count in range(0, len(boat) + 1):
                for new_boat_to_left in list(set(combinations(boat, new_boat_to_left_count))):
                    new_left = left + ''.join(new_boat_to_left)
                    new_boat = boat
                    new_right = right
                    for passenger in new_boat_to_left:
                        new_boat = new_boat.replace(passenger, '', 1)

                    state = 'Unloaded to left'
                    #                    print(f'    {state} {level}: {new_left} < {new_boat} _ {new_right}')
                    if len(history) > min_path_len:
                        #                        print('        Shorter path exists:', len(history), min_path_len)
                        continue
                    if [new_left, new_boat, new_right, state] in history:
                        #                        print('        Already in history')
                        continue
                    q.append([new_left, new_boat, new_right, state,
                              history + [[new_left, new_boat, new_right, state]], level + 1])

    if min_path == []:
        print('Unfortunately, no pathes found')
        return None
    else:
        print('Top victory:')
        print_history(min_path)
        crossing_count = int(min_path_len / 2)
        print('Crossing count:', crossing_count)
        return crossing_count


if __name__ == '__main__':
    # These "asserts" are used for self-checking and not for an auto-testing

    assert river_crossing(5, 0, 5, 3) is None, 'impossible'

    #raise

    assert river_crossing(1, 1, 1, 1) == 7, 'original'
    assert river_crossing(1, 1, 1, 2) == 3, 'payload +1'
    assert river_crossing(2, 1, 1, 2) == 5, 'payload +1, wolf +1'
    assert river_crossing(1, 2, 1, 1) is None, 'impossible'

    print("Coding complete? Click 'Check' to earn cool rewards!")
