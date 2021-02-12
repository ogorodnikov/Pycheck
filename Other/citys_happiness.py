from itertools import chain, combinations


# Imported:
# # 16-liner: almost easy
# przemyslaw.daniel
#
# def subnetworks(net, crush):
#     result = {x: {x} for x in sum(net, []) if x not in crush}
#     for a, b in net*len(net):
#         if set(crush) & {a, b}: continue
#         result[a] |= result[b] | {a, b}
#         result[b] |= result[a] | {a, b}
#     return {frozenset(x) for x in result.values()}


def get_clusters(connections, faulty_nodes=None):
    if faulty_nodes is None:
        faulty_nodes = set()
    clusters = []
    sorted_connections = sorted(connections)
    for a in sorted_connections:
        # print('    a:', a)
        a_cluster = set(a) - set(faulty_nodes)
        if not a_cluster:
            # print('    All faulty')
            continue
        if any(a_cluster & existing_cluster for existing_cluster in clusters):
            # print('    Already in clusters')
            continue
        for b in sorted_connections:
            # print('        b:', b)
            b_cluster = set(b) - set(faulty_nodes)
            if a_cluster & b_cluster:
                # print(f'        Clusters intersect: {a_cluster} & {b_cluster}')
                a_cluster |= b_cluster
        # print('Adding cluster:', a_cluster)
        clusters.append(a_cluster)
    return clusters


def most_crucial(net, users):
    print('Network:', net)
    print('Users:', users)

    nodes = set(chain.from_iterable(net))
    print('Nodes:', nodes)

    overall_happinesses = []
    for faulty_nodes in combinations(nodes, 1):
        print('Faulty nodes:', faulty_nodes)
        clusters = get_clusters(net, faulty_nodes=set(faulty_nodes))
        print('    Clusters:', clusters)
        happiness_per_cluster = [pow(sum(users[node] for node in cluster), 2) for cluster in clusters]
        print('    Happiness per cluster:', happiness_per_cluster)
        happiness_for_disconnected_users = sum(users[node] for node in faulty_nodes)
        print('    Happiness for disconnected users:', happiness_for_disconnected_users)
        overall_happiness = sum(happiness_per_cluster) + happiness_for_disconnected_users
        print('    Overall happiness:', overall_happiness)
        overall_happinesses.append((faulty_nodes, overall_happiness))
        print()

    _, min_overall_happiness = min(overall_happinesses, key=lambda o: o[1])
    minimum_happiness_filter = sorted(filter(lambda o: o[1] == min_overall_happiness, overall_happinesses))
    most_crucial_nodes = [''.join(faulty_nodes) for faulty_nodes, overall_happiness in minimum_happiness_filter]
    print('Most crucial nodes:', most_crucial_nodes)
    print('Min overall happiness:', min_overall_happiness)
    print()
    return most_crucial_nodes


if __name__ == '__main__':

    assert most_crucial([
        ['A', 'B'],
        ['B', 'C'],
        ['C', 'A']
    ], {
        'A': 10,
        'B': 5,
        'C': 10
    }) == ['A', 'C'], 'Extra 1'

    assert most_crucial([
        ['A', 'B'],
        ['A', 'C'],
        ['E', 'D'],
        ['D', 'F']
    ], {
        'A': 0,
        'B': 10,
        'C': 10,
        'D': 10,
        'E': 10,
        'F': 10
    }) == ['D'], 'Test'

    assert most_crucial([
        ['A', 'B'],
        ['A', 'C'],
        ['A', 'D'],
        ['A', 'E']
    ], {
        'A': 0,
        'B': 10,
        'C': 10,
        'D': 10,
        'E': 10
    }) == ['A'], 'Third'

    assert most_crucial([
        ['A', 'B'],
        ['B', 'C']
    ], {
        'A': 10,
        'B': 10,
        'C': 10
    }) == ['B'], 'First'

    assert most_crucial([
        ['A', 'B']
    ], {
        'A': 20,
        'B': 10
    }) == ['A'], 'Second'

    assert most_crucial([
        ['A', 'B'],
        ['B', 'C'],
        ['C', 'D']
    ], {
        'A': 10,
        'B': 20,
        'C': 10,
        'D': 20
    }) == ['B'], 'Forth'