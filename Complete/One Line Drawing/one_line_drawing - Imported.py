def draw(segments):
    edges = [{s[:2], s[2:]} for s in segments]
    nodes = [node for edge in edges for node in edge]
    odd_nodes = {node for node in nodes if nodes.count(node) % 2}
    print('Edges:', edges)
    print('Nodes:', nodes)
    print('Odd nodes:', odd_nodes)
    print('Length of Odd nodes:', len(odd_nodes))
    print('Odd nodes or Nodes:', odd_nodes or nodes)
    print('Min of Odd nodes or Nodes:', min(odd_nodes or nodes))

    def dfs(a):
        print()
        print('DFS for:', a)
        for b in nodes:
            if {a, b} in edges:
                print((a, b), 'in edges')
                edges.remove({a, b})
                print('Removing:', (a, b))
                print('Edges left:', edges)
                dfs(b)
        print('    Adding:', a)
        path.append(a)
        print('    Path:', path)

    path = []
    if len(odd_nodes) < 4:
        dfs(min(odd_nodes or nodes))
        print('Path:', path)
    else:
        print('Too much Odd nodes')
    return path


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



    # assert checker(draw,
    #                {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5)}), "Example 1"

    # assert checker(draw,
    #                {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7),
    #                 (4, 7, 7, 5), (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2)},
    #                False), "Example 2"

    assert checker(draw,
                   {(1, 2, 1, 5), (1, 2, 7, 2), (1, 5, 4, 7), (4, 7, 7, 5),
                    (7, 5, 7, 2), (1, 5, 7, 2), (7, 5, 1, 2), (1, 5, 7, 5)}), "Example 3"