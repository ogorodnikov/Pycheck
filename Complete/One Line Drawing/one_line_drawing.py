from heapq import heapify, heappush, heappop

def draw(segments):
    vertexes = []
    for segment in segments:
        vertexes.append((segment[0], segment[1]))
        vertexes.append((segment[2], segment[3]))
    vertexes = list(set(vertexes))

    print('Segments:', *segments)
    print('Vertexes:', *vertexes)

    for start_vertex in vertexes:
        print('Starting from vertex:', start_vertex)
        q = [(0, 0, start_vertex, [start_vertex], [])]
        while q:
            priority, level, a, points, path = heappop(q)
            if level >= 30:
                print('Break on level 30')
                return[]
            for b in vertexes:
                edge1 = a[0], a[1], b[0], b[1]
                edge2 = b[0], b[1], a[0], a[1]
                for segment in segments:
                    if segment in path:
                        continue
                    if segment == edge1 or segment == edge2:
                        new_path = path + [segment]
                        new_points = points + [b]
                        priority = -level
                        if set(new_path) == set(segments):
                            print('All segments traversed')
                            print('Points:', *new_points)
                            print()
                            return new_points
                        heappush(q, (priority, level + 1, b, new_points, new_path))
                        print('Adding:', (priority, level + 1, b, new_points, new_path))

    print('No paths found')
    print()
    return []


if __name__ == '__main__':
    # These "asserts" using only for self-checking and not necessary for auto-testing
    def checker(func, in_data, is_possible=True):
        user_result = func(in_data)
        if not is_possible:
            if user_result:
                print("How did you draw this?")
                return False
            else:
                return True
        if len(user_result) < 2:
            print("More points please.")
            return False
        data = list(in_data)
        for i in range(len(user_result) - 1):
            f, s = user_result[i], user_result[i + 1]
            if (f + s) in data:
                data.remove(f + s)
            elif (s + f) in data:
                data.remove(s + f)
            else:
                print("The wrong segment {}.".format(f + s))
                return False
        if data:
            print("You forgot about {}.".format(data[0]))
            return False
        return True


    # assert checker(draw, {(1, 2, 1, 5), (1, 2, 7, 2), (7, 5, 1, 2), (4, 7, 7, 5), (1, 5, 4, 7), (7, 5, 7, 2),
    #                       (1, 5, 7, 2)}), "Test 3"

    assert checker(draw,
                   {(8, 4, 8, 6), (4, 8, 6, 2), (6, 8, 8, 6), (4, 8, 8, 6), (2, 6, 4, 2), (6, 2, 8, 4), (6, 8, 6, 2),
                    (2, 6, 6, 2), (2, 4, 8, 4), (6, 8, 8, 4), (4, 2, 6, 2), (4, 2, 8, 6), (2, 4, 2, 6), (4, 2, 6, 8),
                    (4, 2, 4, 8), (2, 4, 6, 2), (2, 4, 4, 8), (4, 8, 6, 8), (6, 2, 8, 6), (4, 8, 8, 4), (2, 6, 8, 6),
                    (2, 6, 6, 8), (2, 4, 4, 2), (4, 2, 8, 4), (2, 4, 6, 8), (2, 6, 4, 8), (2, 6, 8, 4),
                    (2, 4, 8, 6)}), "Edge 3"

    assert checker(draw,
                   {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5)}), "Example 1"
    assert checker(draw,
                   {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7),
                    (4, 7, 7, 5), (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2)},
                   False), "Example 2"
    assert checker(draw,
                   {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5),
                    (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2), (1, 5, 7, 5)}), "Example 3"
