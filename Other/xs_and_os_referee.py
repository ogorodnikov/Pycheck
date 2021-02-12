from typing import List

VECTORS = {((0, 0), (0, 1), (0, 2)),
           ((1, 0), (1, 1), (1, 2)),
           ((2, 0), (2, 1), (2, 2)),
           ((0, 0), (1, 1), (2, 2)),
           ((0, 2), (1, 1), (2, 0))}


def checkio(game_result: List[str]) -> str:
    print('Game result:', game_result)

    reversed_vectors = {tuple(tuple(reversed(coordinate)) for coordinate in coordinates) for coordinates in VECTORS}
    print('Reversed vectors:', reversed_vectors)
    all_vectors = VECTORS | reversed_vectors
    print('All vectors:', all_vectors)

    if any(all(game_result[y][x] == 'X' for x, y in vector) for vector in all_vectors):
        print('X won')
        return 'X'
    elif any(all(game_result[y][x] == 'O' for x, y in vector) for vector in all_vectors):
        print('O won')
        return 'O'
    else:
        print('Draw')
        return 'D'


if __name__ == '__main__':
    print("Example:")
    print(checkio(["X.O",
                   "XX.",
                   "XOO"]))

    # These "asserts" using only for self-checking and not necessary for auto-testing
    assert checkio([
        "X.O",
        "XX.",
        "XOO"]) == "X", "Xs wins"
    assert checkio([
        "OO.",
        "XOX",
        "XOX"]) == "O", "Os wins"
    assert checkio([
        "OOX",
        "XXO",
        "OXX"]) == "D", "Draw"
    assert checkio([
        "O.X",
        "XX.",
        "XOO"]) == "X", "Xs wins again"
    print("Coding complete? Click 'Check' to review your tests and earn cool rewards!")
