from typing import Iterable


def flat_list(array):
    print('Array:', array)

    def flatten(node):
        if isinstance(node, int):
            print('Integer: ', node)
            yield node
        elif isinstance(node, Iterable):
            print('Iterable:', node)
            for subnode in node:
                yield from flatten(subnode)

    output_list = list(flatten(array))
    print('Output list:', output_list)
    print()
    return output_list


if __name__ == '__main__':
    assert flat_list([1, 2, 3]) == [1, 2, 3], "First"
    assert flat_list([1, [2, 2, 2], 4]) == [1, 2, 2, 2, 4], "Second"
    assert flat_list([[[2]], [4, [5, 6, [6], 6, 6, 6], 7]]) == [2, 4, 5, 6, 6, 6, 6, 6, 7], "Third"
    assert flat_list([-1, [1, [-2], 1], -1]) == [-1, 1, -2, 1, -1], "Four"
    print('Done! Check it')