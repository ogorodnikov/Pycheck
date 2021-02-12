from itertools import chain
from math import sin, cos, pi

INITIAL_ANGLE = pi / 2


def get_vertices(polygon):
    top_x, top_y, edge_len, vertices_count = polygon

    # # vertex_angle_degrees = (vertices_count - 2) * 180 / vertices_count
    # vertex_angle_degrees = 180 * (1 - 2 / vertices_count)
    # vertex_angle_radians = pi * (1 - 2 / vertices_count)
    # print('Vertex angle degrees:', vertex_angle_degrees)
    # print('Vertex angle radians:', vertex_angle_radians)
    #
    # dx = edge_len * sin(vertex_angle_radians / 2)
    # dy = edge_len * cos(vertex_angle_radians / 2)
    # print('    dx, dy:', (dx, dy))
    #
    # x = top_x + dx
    # y = top_y - dy
    # print('    x,  y: ', (x, y))
    #
    # radius = edge_len / 2 / cos(vertex_angle_radians / 2)
    # print('Radius:', radius)

    circumradius = edge_len / 2 / sin(pi / vertices_count)
    print('Circumradius:', circumradius)

    center_x = top_x + circumradius * cos(-INITIAL_ANGLE)
    center_y = top_y + circumradius * sin(-INITIAL_ANGLE)
    print('Center:', (center_x, center_y))

    sector_angle = 2 * pi / vertices_count

    for vertex_index in range(vertices_count):
        print('Vertex index:', vertex_index)
        angle = INITIAL_ANGLE + vertex_index * sector_angle
        print('    Angle:', angle)

        dx = circumradius * cos(angle)
        dy = circumradius * sin(angle)
        print('    dx, dy:', dx, dy)

        vertex_x = center_x + dx
        vertex_y = center_y + dy
        print('    Coordinates:', (vertex_x, vertex_y))
        yield vertex_x, vertex_y


def is_in_circle(point, circle_x, circle_y, radius):
    point_x, point_y = point
    dx = point_x - circle_x
    dy = point_y - circle_y
    return dx ** 2 + dy ** 2 <= radius ** 2


def searchlights(polygons, lights):
    # all_vertices = iter(())
    # for polygon in polygons:
    #     print('Polygon:', polygon)
    #     vertices = get_vertices(polygon)
    #     print('Vertices:', vertices)
    #     all_vertices = chain(all_vertices, vertices)
    #     print('All vertices:', all_vertices)

    print('Polygons:', polygons)
    print('Lights:', lights)

    vertices = chain.from_iterable(get_vertices(polygon) for polygon in polygons)

    lighted_vertices_count = sum(any(is_in_circle(vertex, *light) for light in lights)
                                 for vertex in vertices
                                 if vertex[0] > 0 and vertex[1] > 0)
    print('Lighted vertices count:', lighted_vertices_count)
    print()
    return lighted_vertices_count


if __name__ == '__main__':
    assert (searchlights([(2, 3, 2, 3)], [(1, 2, 1)])) == 1, 'regular triangle'
    assert (searchlights([(4, 5, 2, 4)], [(4, 4, 3)])) == 4, 'square'
    assert (searchlights([(6, 7, 2, 5)], [(2, 3, 2)])) == 0, 'regular pentagon'
    assert (searchlights([(4, 2, 2, 6)], [(4, 2, 3)])) == 3, 'regular hexagon'
    assert (searchlights([(1, 7, 2, 8)], [(0, 5, 4)])) == 5, 'regular octagon'
