from typing import List


def bidirect(costs):
    forward_flight_records =  {(a, b, price) for (a, b, price) in costs}
    backward_flight_records = {(b, a, price) for (a, b, price) in costs}
    return forward_flight_records | backward_flight_records


def cheapest_flight(costs: List, a: str, b: str, level=0) -> int:
    routes = bidirect(costs)
    print('Routes: ', sorted(routes))
    print('From, to:', a, b)

    prices = [float('inf')]
    for route in routes:
        print('    Route:', route)
        start, end, price = route
        unused_routes = routes - bidirect({route})
        if start != a:
            print('        Not from:', a)
            continue
        if end == b:
            prices.append(price)
            print('    New price:', price)
            continue
        print('    > Recursion to level:', level + 1)
        sub_price = cheapest_flight(unused_routes, end, b, level + 1)
        prices.append(price + sub_price)
        print('    New price after recursion:', price + sub_price)

    print('Returning prices:     ', prices)
    min_price = min(prices)
    if level == 0:
        if min_price == float('inf'):
            min_price = 0
    print('Returning min price:  ', min_price)
    return min_price


if __name__ == '__main__':
    assert cheapest_flight([['A', 'C', 100],
                            ['A', 'B', 20],
                            ['D', 'F', 900]],
                           'A',
                           'F') == 0
    assert cheapest_flight([['A', 'C', 100],
                            ['A', 'B', 20],
                            ['B', 'C', 50]],
                           'A',
                           'C') == 70
    assert cheapest_flight([['A', 'C', 100],
                            ['A', 'B', 20],
                            ['B', 'C', 50]],
                           'C',
                           'A') == 70
    assert cheapest_flight([['A', 'C', 40],
                            ['A', 'B', 20],
                            ['A', 'D', 20],
                            ['B', 'C', 50],
                            ['D', 'C', 70]],
                           'D',
                           'C') == 60
    assert cheapest_flight([['A', 'B', 10],
                            ['A', 'C', 15],
                            ['B', 'D', 15],
                            ['C', 'D', 10]],
                           'A',
                           'D') == 25
