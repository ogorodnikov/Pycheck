
def find_loop(connections, path):

    print('Path:', path)

    if len(path) > 2 and path[-1] in path[:-1]:
        looped_element = path[-1]
        print('Looped element:', looped_element)
        first_occurence = path.index(looped_element)
        print('First occurence:', first_occurence)

        loop = path[first_occurence:]
        print('Loop:', loop)
        # input()
        return tuple(loop)

    loops = set()

    for connection in set(connections) - set(path):
        print('Connection:', connection)

        if not path:
            path = [connection[0]]

        if path[-1] in connection:
            new_step = [e for e in connection if e != path[-1]]
            print('Recursion:', path + new_step)
            loops.add(find_loop(connections, path + new_step))

    print('Loops:', loops)
    return max(loops, key=len)


def find_cycle(connections):
    print('Connections:', connections)
    
    longest_loop = find_loop(connections, [])

    print('Longest loop:', longest_loop)
    # quit()

    return longest_loop


if __name__ == '__main__':

    def checker(function, connections, best_size):
        user_result = function(connections)
        if not isinstance(user_result, (tuple, list)) or not all(isinstance(n, int) for n in user_result):
            print("You should return a list/tuple of integers.")
            return False
        if not best_size and user_result:
            print("Where did you find a cycle here?")
            return False
        if not best_size and not user_result:
            return True
        if len(user_result) < best_size + 1:
            print("You can find a better loop.")
            return False
        if user_result[0] != user_result[-1]:
            print("A cycle starts and ends in the same node.")
            return False
        if len(set(user_result)) != len(user_result) - 1:
            print("Repeat! Yellow card!")
            return False
        for n1, n2 in zip(user_result[:-1], user_result[1:]):
            if (n1, n2) not in connections and (n2, n1) not in connections:
                print("{}-{} is not exist".format(n1, n2))
                return False
        return True, "Ok"


    assert checker(find_cycle,
                   ((1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 6),
                    (8, 5), (8, 4), (1, 5), (2, 4), (1, 8)), 6), "Example"

    assert checker(find_cycle,
                   ((1, 2), (2, 3), (3, 4), (4, 5), (5, 7), (7, 6), (8, 4), (1, 5), (2, 4)), 5), "Second"
