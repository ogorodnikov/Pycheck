from collections import OrderedDict
from functools import lru_cache
from itertools import product
from typing import Set, Tuple, List, Dict


@lru_cache(maxsize=1000)
def get_connected_nodes(network, node, power_range):
    connected_nodes = set(node)
    if power_range < 1:
        return connected_nodes
    for edge in network:
        a, b = edge
        if a == node:
            connected_nodes |= get_connected_nodes(tuple(set(network) - {edge}), b, power_range - 1) | {b}
        elif b == node:
            connected_nodes |= get_connected_nodes(tuple(set(network) - {edge}), a, power_range - 1) | {a}
    return connected_nodes


def power_plants(network: Set[Tuple[str, str]], ranges: List[int]) -> Dict[str, int]:
    print('Network:', network)
    network = tuple(tuple(edge) for edge in network)
    print('Tuple network:', network)
    print('Ranges:', ranges)

    nodes = {node for edge in network for node in edge}
    print('Nodes:', nodes)

    power_ranges = ranges
    placement_variants = [list(product(nodes, [power_range])) for power_range in power_ranges]
    print('Placement variants:', placement_variants)

    for combination in product(*placement_variants):
        print('Combination:', combination)
        connected_nodes = set()
        for placement_variant in combination:
            print('Placement variant:', placement_variant)
            node, power_range = placement_variant
            connected_nodes |= get_connected_nodes(network, node, power_range)
        print('    Connected nodes:', connected_nodes)

        if connected_nodes == nodes:
            print('    = All connected')
            placements = OrderedDict(placement_variant for placement_variant in combination)
            print('    = Placements:', placements)
            print()
            return placements


if __name__ == '__main__':
    assert power_plants({('A', 'B'), ('B', 'C')}, [1]) == {'B': 1}
    assert power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')}, [2]) == {'C': 2}
    assert power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')}, [1, 1]) == {'B': 1, 'E': 1}
    assert power_plants({('A', 'B'), ('B', 'C'), ('A', 'D'), ('B', 'E')}, [1, 0]) == {'B': 1, 'D': 0}

    # assert power_plants(
    #     [["A", "B"], ["B", "C"], ["C", "D"], ["D", "E"], ["F", "G"], ["G", "H"], ["H", "I"], ["I", "J"], ["K", "L"],
    #      ["L", "M"], ["M", "N"], ["N", "O"], ["P", "Q"], ["Q", "R"], ["R", "S"], ["S", "T"], ["U", "V"], ["V", "W"],
    #      ["W", "X"], ["X", "Y"], ["A", "F"], ["B", "G"], ["C", "H"], ["D", "I"], ["E", "J"], ["F", "K"], ["G", "L"],
    #      ["H", "M"], ["I", "N"], ["J", "O"], ["K", "P"], ["L", "Q"], ["M", "R"], ["N", "S"], ["O", "T"], ["P", "U"],
    #      ["Q", "V"], ["R", "W"], ["S", "X"], ["T", "Y"]], [2, 1, 1, 1, 1]) == {}
