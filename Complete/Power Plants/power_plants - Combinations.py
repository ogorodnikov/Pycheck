from collections import Counter, OrderedDict
from functools import lru_cache
from heapq import heappush, heappop
from itertools import product
from typing import Set, Tuple, List, Dict


@lru_cache(maxsize=1000000)
def get_connected_nodes(network, node, power_range):
    connected_nodes = set(node)
    if power_range < 1:
        return connected_nodes
    for edge in network:
        a, b = edge
        if a == node:
            connected_nodes |= get_connected_nodes(tuple(node for node in network if node != edge), b, power_range - 1) | {b}
        elif b == node:
            connected_nodes |= get_connected_nodes(tuple(node for node in network if node != edge), a, power_range - 1) | {a}
    return connected_nodes


def power_plants(network: Set[Tuple[str, str]], ranges: List[int]) -> Dict[str, int]:
    network = tuple(sorted(tuple(edge) for edge in network))
    nodes = {node for edge in network for node in edge}
    print('Network:', network)
    print('Ranges:', ranges)
    print('Nodes:', nodes)

    connection_per_node = Counter(node for edge in network for node in edge)
    print('Connection per node:', connection_per_node)
    max_connections = max(count for node, count in connection_per_node.items())
    print('Max connections:', max_connections)
    print()

    variants = []
    for range in ranges:
        for node in nodes:
            variants.append((range, node, get_connected_nodes(network, node, range)))

    sorted_variants = sorted(variants, key=lambda v: (-len(v[2]), v[0]))
    print('Sorted variants:')
    for sorted_variant in sorted_variants:
        print(sorted_variant)
    print()


    combinations = []
    connected_regions = []
    while sorted_variants:
        connected_region = set()
        spare_ranges = ranges.copy()
        spare_cities = list(nodes).copy()
        for variant in sorted_variants.copy():
            print('Variant:', variant)

            range, powered_city, connected_cities = variant

            if range not in spare_ranges:
                print('   Range already used')
                continue
            if powered_city not in spare_cities:
                print('   City already powered')
                continue

            range_index = spare_ranges.index(range)
            spare_ranges = spare_ranges[:range_index] + spare_ranges[range_index+1:]

            city_index = spare_cities.index(powered_city)
            spare_cities = spare_cities[:city_index] + spare_cities[city_index+1:]

            combinations.append(variant)
            print('+ Adding variant:', variant)
            connected_region |= connected_cities
            connected_regions.append(connected_region)
            print('+ Adding connected region:', connected_cities)

            variant_index = sorted_variants.index(variant)
            sorted_variants = sorted_variants[:variant_index] + sorted_variants[variant_index + 1:]



    print('Combinations:')
    for combination in combinations:
        print(combination)
    print()

    print('Nodes:')
    print(nodes)
    print()

    print('Connected regions:')
    for connected_region in connected_regions:
        print(connected_region)
    print()










    return {}


if __name__ == '__main__':
    # assert power_plants({('A', 'B'), ('B', 'C')}, [1]) == {'B': 1}
    # assert power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')}, [2]) == {'C': 2}
    # assert power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')}, [1, 1]) == {'B': 1, 'E': 1}
    assert power_plants({('A', 'B'), ('B', 'C'), ('A', 'D'), ('B', 'E')}, [1, 0]) == {'B': 1, 'D': 0}

    # assert power_plants(
    #     [["A", "B"], ["B", "C"], ["C", "D"], ["D", "E"], ["F", "G"], ["G", "H"], ["H", "I"], ["I", "J"], ["K", "L"],
    #      ["L", "M"], ["M", "N"], ["N", "O"], ["P", "Q"], ["Q", "R"], ["R", "S"], ["S", "T"], ["U", "V"], ["V", "W"],
    #      ["W", "X"], ["X", "Y"], ["A", "F"], ["B", "G"], ["C", "H"], ["D", "I"], ["E", "J"], ["F", "K"], ["G", "L"],
    #      ["H", "M"], ["I", "N"], ["J", "O"], ["K", "P"], ["L", "Q"], ["M", "R"], ["N", "S"], ["O", "T"], ["P", "U"],
    #      ["Q", "V"], ["R", "W"], ["S", "X"], ["T", "Y"]], [2, 1, 1, 1, 1]) == {'M': 2, 'U': 1, 'A': 1, 'Y': 1, 'E': 1}
