from itertools import combinations


def ranges_len(ranges):
    return 1 + sum(end - start for start, end in ranges)


def range_union(range_a, range_b):
    a1, a2 = range_a
    b1, b2 = range_b

    if b1 <= a2 + 1 and b2 >= a1 - 1:
        return {tuple((min(a1, b1), max(a2, b2)))}


def merge_ranges(ranges_list):
    # print('Ranges list', ranges_list)

    ranges = set(tuple(r) for r in ranges_list)
    # print('Ranges:', ranges)
    # print()

    is_changed = True
    while is_changed:
        is_changed = False
        for a, b in combinations(ranges, 2):
            # print('A, B:', (a, b))
            a_b_union = range_union(a, b)
            # print('Union:', a_b_union)
            if a_b_union:
                is_changed = True
                ranges = ranges - {a} - {b} | a_b_union
                # print('Ranges:', ranges)
        # print()
    # print('Merged ranges:', ranges)
    return ranges


def checkio(required, operations):
    print('Operations:', operations)
    print('Required:', required)

    for i in range(1, len(operations) + 1):
        print('I:', i)
        print('Operations:', operations[:i])
        painted_ranges = merge_ranges(operations[:i])
        print('Painted ranges:', painted_ranges)
        painted_length = ranges_len(painted_ranges)
        print('Painted length:', painted_length)

        if painted_length >= required:
            print('= Required length reached')
            print('= Operation count:', i)
            print()
            return i

    print('= Not enough commands')
    print()
    return -1


if __name__ == '__main__':
    assert checkio(5, [[1, 5], [11, 15], [2, 14], [21, 25]]) == 1, "1st"
    assert checkio(6, [[1, 5], [11, 15], [2, 14], [21, 25]]) == 2, "2nd"
    assert checkio(11, [[1, 5], [11, 15], [2, 14], [21, 25]]) == 3, "3rd"
    assert checkio(16, [[1, 5], [11, 15], [2, 14], [21, 25]]) == 4, "4th"
    assert checkio(21, [[1, 5], [11, 15], [2, 14], [21, 25]]) == -1, "not enough"
    assert checkio(1000000011, [[1, 1000000000], [11, 1000000010]]) == -1, "large"

    assert checkio(620000000000000, [[858310018365524, 902063077244091], [932665378449117, 1028409672338264],
                                     [882165278163239, 957945652291761], [155331862264691, 231608087199557],
                                     [309323812898016, 328794059405147], [311727991597994, 391226174154816],
                                     [826415306967097, 893972043882819], [170753995991478, 221100797836809],
                                     [472995836315594, 478902758061898], [779003863306990, 822734502976504],
                                     [539843675072188, 554844466580541], [977564633426502, 991018537238369],
                                     [889461015856698, 901719104033374], [268288887276466, 292053591549963],
                                     [87698520389374, 109261297832598], [650723837467456, 729926149124749],
                                     [627448683684809, 644021001384284], [264317870081369, 322309330307873],
                                     [238729907671924, 290743490959244], [938382837602825, 955450166170994]]) == -1

    assert checkio(612742616513000, [[858310018365524, 902063077244091], [932665378449117, 1028409672338264],
                                     [882165278163239, 957945652291761], [155331862264691, 231608087199557],
                                     [309323812898016, 328794059405147], [311727991597994, 391226174154816],
                                     [826415306967097, 893972043882819], [170753995991478, 221100797836809],
                                     [472995836315594, 478902758061898], [779003863306990, 822734502976504],
                                     [539843675072188, 554844466580541], [977564633426502, 991018537238369],
                                     [889461015856698, 901719104033374], [268288887276466, 292053591549963],
                                     [87698520389374, 109261297832598], [650723837467456, 729926149124749],
                                     [627448683684809, 644021001384284], [264317870081369, 322309330307873],
                                     [238729907671924, 290743490959244], [938382837602825, 955450166170994]]) == 19
