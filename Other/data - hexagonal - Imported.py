# imported functions:

def calc_distance(a, b):
    y0, y1 = ord(a[0])-65, ord(b[0])-65
    x0, x1 = int(a[1])-y0 // 2-1, int(b[1])-y1 // 2-1
    return max(abs(x1-x0), abs(y1-y0), abs(x1-x0+y1-y0))

def calc_angle(a, b):
    from math import pi, acos
    x0, y0, x1, y1 = map(ord, a+b)
    y0, y1 = y0-(x0 % 2)/2, y1-(x1 % 2)/2
    x0, x1 = 3**0.5/2*x0, 3**0.5/2*x1
    c = ((x0-x1)**2+(y0-y1)**2)**0.5
    result = acos((x0-x1)/c)*[-1, 1][y0 > y1]
    return 180+round(result/pi*180)






MOVES = {'NW': (-1, 1, 0), 'N': (0, 1, -1), 'NE': (1, 0, -1),
         'SW': (-1, 0, 1), 'S': (0, -1, 1), 'SE': (1, -1, 0)}
min_dot_prod = {0: 2, 60: 1.5, 120: 1}

def cube_coords(point: str):
    c, r = (ord(x) - ord(a) for x, a in zip(point, 'A1')) # offset coords
    return c, - c - r + (c // 2), r - (c // 2)     # now it's cube coords

vector = lambda A, B: tuple(map(sub, B, A))
dot_product = lambda u, v: sum(map(mul, u, v))
cube_distance = lambda A, B: max(map(abs, vector(A, B)))






# Return the coordinates resulting from a move in the specified direction.
def move(coord, direction):
    col, row = coord
    if direction == 0: # N
        return (col, row - 1)
    if direction == 1: # NE
        return (col + 1, (row - 1 if col % 2 else row))
    if direction == 2: # SE
        return (col + 1, (row if col % 2 else row + 1))
    if direction == 3: # S
        return (col, row + 1)
    if direction == 4: # SW
        return (col - 1, (row if col % 2 else row + 1))
    if direction == 5: # NW
        return (col - 1, (row - 1 if col % 2 else row))
