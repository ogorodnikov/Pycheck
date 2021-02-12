def healthy(grid):
    # generate the r-th diamond coordinate
    def diamond(r):
        for i in range(r):
            yield from [(i, r - i), (r - i, -i), (-i, i - r), (i - r, i)]

    # get radius of colony with center (cx, cy)
    def radius(coord):
        cy, cx = coord
        if grid[cy][cx] == 0: return 0
        r = 1
        while True:
            n = [0, 0] # counter of each item
            for dx, dy in diamond(r):
                x, y = cx + dx, cy + dy
                c = grid[y][x] > 0 if 0 <= x < xsize and 0 <= y < ysize else 0
                n[c] += 1
            if n[1] == 0: return r - 1 # found radius r coloony
            if n[0]: return 0 # found unhealthy colony
            r += 1

    xsize, ysize = len(grid[0]), len(grid)
    return max(((y, x) for y in range(ysize) for x in range(xsize)), key=radius)