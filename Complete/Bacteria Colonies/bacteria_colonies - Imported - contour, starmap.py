from itertools import chain, product, starmap


def healthy(grid, default=(0, 0), diffs=((-1, 0), (1, 0), (0, -1), (0, 1))):
    cells = product(*map(range, map(len, (grid, grid[0]))))
    bacteria = {(r, c) for r, c in cells if grid[r][c] == 1}

    around = lambda r, c: {(r + y, c + x) for y, x in diffs}
    contour = lambda shape: set(chain(*starmap(around, shape))) - shape

    def getsize(cell):
        shape, size = {cell}, 0
        while contour(shape) <= bacteria:
            shape |= contour(shape)
            size += 1
        return 0 if contour(shape) & bacteria else size

    if not bacteria: return default
    center = max(bacteria, key=getsize)
    return center if getsize(center) else default


# "if contour(shape) & bacteria" condition to make sure the eventual contour have only zeros.