def merge_intervals(intervals):
    print('Input intervals:', intervals)

    for i in range(len(intervals) - 1):
        a1, a2 = intervals[i]
        b1, b2 = intervals[i + 1]
        if b1 <= a2 + 1:
            c1 = min(a1, b1)
            c2 = max(a2, b2)
            intervals[i] = None
            intervals[i + 1] = (c1, c2)

    output_intervals = list(filter(None, intervals))
    print('Output intervals:', output_intervals)
    print()
    return output_intervals


if __name__ == '__main__':
    assert merge_intervals([(1, 4), (2, 6), (8, 10), (12, 19)]) == [(1, 6), (8, 10), (12, 19)], "First"
    assert merge_intervals([(1, 12), (2, 3), (4, 7)]) == [(1, 12)], "Second"
    assert merge_intervals([(1, 5), (6, 10), (10, 15), (17, 20)]) == [(1, 15), (17, 20)], "Third"


# # Imported - reduce
# from functools import reduce
#
#
# def merge_intervals(intervals):
#
#     def combine(value, element):
#         if value:
#             last_begin, last_end = value[-1]
#             if element[0] <= last_end + 1:
#                 value[-1] = (last_begin, max(last_end, element[1]))
#             else:
#                 value.append(element)
#         else:
#             value = [element]
#         return value
#
#     return reduce(combine, intervals, [])