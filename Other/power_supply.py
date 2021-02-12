def get_connected_nodes(network, node, power_range):
    connected_nodes = {node}
    if power_range < 1:
        return connected_nodes
    for edge in network:
        a, b = edge
        if a == node:
            connected_nodes |= get_connected_nodes(network - {edge}, b, power_range - 1) | {b}
        elif b == node:
            connected_nodes |= get_connected_nodes(network - {edge}, a, power_range - 1) | {a}
    return connected_nodes


def power_supply(network, power_plants):
    network = {tuple(edge) for edge in network}
    print('Network:', network)
    unpowered = {node for edge in network for node in edge}

    for power_plant, power_range in power_plants.items():
        print('Power plant:', power_plant)
        print('Power range:', power_range)
        unpowered -= get_connected_nodes(network, power_plant, power_range)

    print('Unpowered:', unpowered)
    print()
    return unpowered


if __name__ == '__main__':
    assert power_supply([['p1', 'c1'], ['c1', 'c2']], {'p1': 1}) == set(['c2']), 'one blackout'
    assert power_supply([['c0', 'c1'], ['c1', 'p1'], ['c1', 'c3'], ['p1', 'c4']], {'p1': 1}) == set(
        ['c0', 'c3']), 'two blackout'
    assert power_supply([['p1', 'c1'], ['c1', 'c2'], ['c2', 'c3']], {'p1': 3}) == set([]), 'no blackout'
    assert power_supply([['c0', 'p1'], ['p1', 'c2']], {'p1': 0}) == set(['c0', 'c2']), 'weak power-plant'
    assert power_supply([['p0', 'c1'], ['p0', 'c2'], ['c2', 'c3'], ['c3', 'p4'], ['p4', 'c5']],
                        {'p0': 1, 'p4': 1}) == set([]), 'cooperation'

    assert power_supply([['c0', 'p1'], ['p1', 'c2'], ['c2', 'c3'], ['c2', 'c4'], ['c4', 'c5'],
                         ['c5', 'c6'], ['c5', 'p7']],
                        {'p1': 1, 'p7': 1}) == set(['c3', 'c4', 'c6']), 'complex cities 1'

    assert power_supply([['p0', 'c1'], ['p0', 'c2'], ['p0', 'c3'],
                         ['p0', 'c4'], ['c4', 'c9'], ['c4', 'c10'],
                         ['c10', 'c11'], ['c11', 'p12'], ['c2', 'c5'],
                         ['c2', 'c6'], ['c5', 'c7'], ['c5', 'p8']],
                        {'p0': 1, 'p12': 4, 'p8': 1}) == set(['c6', 'c7']), 'complex cities 2'

    assert power_supply([['c1', 'c2'], ['c2', 'c3']], {}) == set(['c1', 'c2', 'c3']), 'no power plants'
    assert power_supply([['p1', 'c2'], ['p1', 'c4'], ['c4', 'c3'], ['c2', 'c3']], {'p1': 1}) == set(['c3']), 'circle'
    assert power_supply([['p1', 'c2'], ['p1', 'c4'], ['c2', 'c3']], {'p1': 4}) == set([]), 'more than enough'
