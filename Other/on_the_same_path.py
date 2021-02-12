from typing import Iterable, List, Tuple, Union
Node = Union[int, str]
Tree = Tuple[Node, List['Tree']]


def get_indexes(tree, index_prefix='M'):
    child, ancestors = tree
    indexes = {child: index_prefix}
    if ancestors:
        for i, ancestor in enumerate(ancestors):
            indexes.update(get_indexes(ancestor, index_prefix + str(i)))
    return indexes


def on_same_path(tree: Tree, pairs: List[Tuple[Node, Node]]) -> Iterable[bool]:
    print('Tree:', tree)
    print('Pairs:', pairs)

    indexes = get_indexes(tree)
    print('Indexes:', indexes)

    is_same_path = [all(a == b for a, b in zip(indexes[person_a], indexes[person_b]))
                    for person_a, person_b in pairs]
    print('Is same path:', is_same_path)
    print()
    return is_same_path


if __name__ == '__main__':

    TESTS = (
        (
            ('Me', [('Daddy', [('Grandpa', []),
                               ('Grandma', [])]),
                    ('Mom', [('Granny', []),
                             ('?', [])])]),
            [('Grandpa', 'Me'), ('Daddy', 'Granny')],
            [True, False],
        ),
        (
            (1, [(2, [(4, []),
                      (5, [(7, []),
                           (8, []),
                           (9, [])])]),
                 (3, [(6, [])])]),
            [(1, 5), (2, 9), (2, 6)],
            [True, True, False],
        ),
        (
            (0, [(1, [(2, []),
                      (3, [])]),
                 (4, [(5, []),
                      (6, [])]),
                 (7, [(8, []),
                      (9, [])])]),
            [(4, 2), (0, 5), (2, 3), (9, 2), (6, 4), (7, 8), (8, 1)],
            [False, True, False, False, True, True, False],
        ),
    )

    for test_nb, (tree, pairs, answers) in enumerate(TESTS, 1):
        user_result = list(on_same_path(tree, pairs))
        if user_result != answers:
            print(f'You failed the test #{test_nb}.')
            print(f'Your result: {user_result}')
            print(f'Right result: {answers}')
            break

