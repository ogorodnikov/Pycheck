from collections import OrderedDict
from functools import lru_cache
from itertools import product
from typing import Set, Tuple, List, Dict


def power_plants(network: Set[Tuple[str, str]], ranges: List[int]) -> Dict[str, int]:


    # @lru_cache(maxsize=1000)
    def get_connected_nodes(node, power_range):
        nonlocal network
        connected_nodes = set(node)
        print('    Start:', node, power_range)
        print('    Start network:', network)
        if power_range < 1:
            return connected_nodes
        for edge in network.copy():
            a, b = edge
            print('        Edge:', edge)
            if a == node:
                network -= {edge}
                print('        Updated network:', network)
                connected_nodes |= get_connected_nodes(b, power_range - 1) | {b}
            elif b == node:
                network -= {edge}
                print('        Updated network:', network)
                connected_nodes |= get_connected_nodes(a, power_range - 1) | {a}
        print('    Returning connected nodes:', connected_nodes)
        return connected_nodes

    print('Network:', network)
    network = {tuple(edge) for edge in network}
    print('Set network:', network)
    print('Ranges:', ranges)

    nodes = {node for edge in network for node in edge}
    print('Nodes:', nodes)

    power_ranges = ranges
    placement_variants = [list(product(nodes, [power_range])) for power_range in power_ranges]
    print('Placement variants:', placement_variants)
    print()

    products = list(product(*placement_variants))
    print('Length of products:', len(products))
    for i, combination in enumerate(products):
        print('Combination:', combination, i, i / len(products) * 100, '%')
        connected_nodes = set()
        for placement_variant in combination:
            print('Placement variant:', placement_variant)
            node, power_range = placement_variant
            network_save = network.copy()
            connected_nodes |= get_connected_nodes(node, power_range)
            network = network_save
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

    assert power_plants(
        [["A", "B"], ["B", "C"], ["C", "D"], ["D", "E"], ["F", "G"], ["G", "H"], ["H", "I"], ["I", "J"], ["K", "L"],
         ["L", "M"], ["M", "N"], ["N", "O"], ["P", "Q"], ["Q", "R"], ["R", "S"], ["S", "T"], ["U", "V"], ["V", "W"],
         ["W", "X"], ["X", "Y"], ["A", "F"], ["B", "G"], ["C", "H"], ["D", "I"], ["E", "J"], ["F", "K"], ["G", "L"],
         ["H", "M"], ["I", "N"], ["J", "O"], ["K", "P"], ["L", "Q"], ["M", "R"], ["N", "S"], ["O", "T"], ["P", "U"],
         ["Q", "V"], ["R", "W"], ["S", "X"], ["T", "Y"]], [2, 1, 1, 1, 1]) == {}
