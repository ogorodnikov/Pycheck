from collections import Counter, OrderedDict
from functools import lru_cache
from heapq import heappush, heappop
from itertools import product
from typing import Set, Tuple, List, Dict


@lru_cache(maxsize=10000000)
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

    power_ranges = ranges
    placement_variants = tuple(tuple(product(nodes, [power_range])) for power_range in power_ranges)
    print('Placement variants:')
    for placement_variant in placement_variants:
        print(placement_variant)

    placement_variants_product = list(product(*placement_variants))[:10000]
    placement_variants_product_len = len(placement_variants_product)
    print('Placement variants product len:', placement_variants_product_len)

    id = 0
    placement_heap = []
    for placement_variant in placement_variants_product:
        print('Placement variants:', placement_variant)
        connections = sum(connection_per_node[node] for node, power_range in placement_variant)
        print('Connections:', connections)

        priority = max_connections - connections
        heappush(placement_heap, (priority, id, placement_variant))
        id += 1
    print('Placement heap:', placement_heap)
    placement_heap_len = len(placement_heap)
    print('Placement heap len:', placement_heap_len)
    print()

    tick = 0
    while placement_heap:
        priority, _, placement_variant = heappop(placement_heap)
        print('Placement variant: ', placement_variant)
        tick += 1
        print(f'Tick: {tick} - {tick/placement_heap_len * 100:2.5}% of {placement_heap_len}')
        connected_nodes = set()
        for placement_pair in placement_variant:
            print('   Placement pair: ', placement_pair)
            node, power_range = placement_pair
            connected_nodes |= get_connected_nodes(network, node, power_range)
            print('   Connected nodes:', connected_nodes)

            if connected_nodes == nodes:
                print('=== All covered')
                matched_variant = placement_variant
                placements = OrderedDict()
                for matched_pair in matched_variant:
                    matched_node, matched_power_range = matched_pair
                    placements[matched_node] = matched_power_range
                print('=== Placements:', placements)
                return placements

    print('No variants found')
    return {}


if __name__ == '__main__':
    # assert power_plants({('A', 'B'), ('B', 'C')}, [1]) == {'B': 1}
    # assert power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')}, [2]) == {'C': 2}
    # assert power_plants({('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')}, [1, 1]) == {'B': 1, 'E': 1}
    # assert power_plants({('A', 'B'), ('B', 'C'), ('A', 'D'), ('B', 'E')}, [1, 0]) == {'B': 1, 'D': 0}

    assert power_plants(
        [["A", "B"], ["B", "C"], ["C", "D"], ["D", "E"], ["F", "G"], ["G", "H"], ["H", "I"], ["I", "J"], ["K", "L"],
         ["L", "M"], ["M", "N"], ["N", "O"], ["P", "Q"], ["Q", "R"], ["R", "S"], ["S", "T"], ["U", "V"], ["V", "W"],
         ["W", "X"], ["X", "Y"], ["A", "F"], ["B", "G"], ["C", "H"], ["D", "I"], ["E", "J"], ["F", "K"], ["G", "L"],
         ["H", "M"], ["I", "N"], ["J", "O"], ["K", "P"], ["L", "Q"], ["M", "R"], ["N", "S"], ["O", "T"], ["P", "U"],
         ["Q", "V"], ["R", "W"], ["S", "X"], ["T", "Y"]], [2, 1, 1, 1, 1]) == {}
