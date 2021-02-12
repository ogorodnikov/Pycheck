import heapq
from typing import List
from itertools import tee


def delivery_drone(orders: List[int]) -> int:
    print('Orders:', *orders)

    def drone_drop_and_pick():
        nonlocal id
        id += 1
        print('New load at:', (new_position, new_index))
        new_load = packages[new_position][new_index]
        print('    ==== Packages', packages)
        new_packages = [[e for e in element_list] for element_list in packages]
        print('    ==== New packages', new_packages)
        new_packages[new_position][new_index] = load
        distance = abs(new_position - position)
        new_moves = moves + distance
        new_path = path + [(new_position, new_index, new_load)]
        drone_vector = [[new_load] if location == new_position else [0]
                        for location, package_list in enumerate(new_packages)]

        print('Pushing:')
        print('        Old load:', load)
        print('        New load:', new_load)
        print('        Old position:', position)
        print('        New position:', new_position)
        print('        Distance:', distance)
        print('        Total moves:', new_moves)
        print('       ', drone_vector)
        print('       ', new_packages)

        heapq.heappush(heap, [priority, id, level + 1, new_moves, new_position,
                              new_load, new_packages, new_path])

        is_arranged = True
        for location, element_list in enumerate(new_packages):
            for element in element_list:
                if element != 0 and element != location:
                    is_arranged = False

        if new_load == 0 and is_arranged:
            print('All delivered:', new_moves + new_position)
            print(new_packages)
            print()
            return new_moves + new_position

    ### main loop
    id = 0
    orders_list = [[element] for element in orders]
    heap = [[0, 0, 0, 0, 0, 0, orders_list, []]]
    while heap:
        priority, _, level, moves, position, load, packages, path = heapq.heappop(heap)
        drone_vector = [[load] if location == position else [0]
                        for location, package_list in enumerate(packages)]

        print('Popping:')
        print(f'    {id} {level} {priority}')
        print('    Position:', position)
        print('    Load:', load)
        print('   ', drone_vector)
        print('   ', packages)

        if load == 0:
            variants = []
            for location, element_list in enumerate(packages):
                for index, element in enumerate(element_list):
                    if element != location and element != 0:
                        variants.append((location, index))
        else:
            variants = [(load, len(packages[load]) - 1)]
            if packages[load][0] != 0:
                packages[load].append(0)
                variants.append((load, len(packages[load]) - 1))

        for new_position, new_index in variants:
            total_moves = drone_drop_and_pick()
            if total_moves:
                return total_moves

    print('End of delivery')


if __name__ == '__main__':
    assert delivery_drone([0, 0, 1, 2]) == 6

    assert delivery_drone([0, 2, 0]) == 4

    assert delivery_drone([0, 2, 4, 0, 1, 0, 5]) == 12
