from functools import reduce
from itertools import product


def select(img, n):

    # a = 0
    #
    # for x, y in product(range(n * 4 + 1, n * 4 + 4), range(5)):
    #     print('A:', a)
    #     print('    X:', x)
    #     print('    Y:', y)
    #
    #     a = (a << 1) + (img[y][x] in (1, '#'))
    #
    #     print('A:', a)
    #
    # return a

    return reduce(
        lambda a, xy: (a << 1) + (img[xy[1]][xy[0]] in (1, '#')),
        product(range(n * 4 + 1, n * 4 + 4), range(5)),
        0)


FONT = [
    select([
        "·##···#··###·###·#·#·###··##·###·###··##",
        "·#·#·##····#···#·#·#·#···#·····#·#·#·#·#",
        "·#·#··#···##··#··###·##··###··#··###·###",
        "·#·#··#··#·····#···#···#·#·#·#···#·#···#",
        "··##··#··###·###···#·##···##·#···###·##·", ], n)
    for n in range(10)]

print('FONT:', FONT)
quit()


def decode(bits):
    return next(i for i, f in enumerate(FONT) if bin(bits ^ f).count('1') <= 1)


def checkio(image):
    return reduce(
        lambda a, n: a * 10 + decode(select(image, n)),
        range(len(image[0]) // 4),
        0)


if __name__ == '__main__':
    assert checkio([[0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0],
                    [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                    [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
                    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
                    [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]]) == 394, "394 clear"

    # assert checkio([[0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0],
    #                 [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    #                 [0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    #                 [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    #                 [0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0]]) == 394, "again 394 but with noise"

    # assert checkio(
    #     [[0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
    #      [0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    #      [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
    #      [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    #      [0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0]])
