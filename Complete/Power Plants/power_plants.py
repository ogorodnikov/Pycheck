from typing import Set, Tuple, List, Dict
from itertools import combinations
from collections import namedtuple, Counter


def power_plants(network: Set[Tuple[str, str]], ranges: List[int]) -> Dict[str, int]:
    """ Based on solution by Ylliw:
    https://py.checkio.org/mission/power-plants/publications/Ylliw/python-3/first-fully-documented-great-mission
    """
    plants_counter = Counter(ranges)
    print('Plants counter:', plants_counter)
    cities = {city for edge in network for city in edge}
    print('Cities:', cities)

    def get_reachable_cities(max_power: int) -> Dict[str, Dict[int, Set[str]]]:
        """ Get reachable cities: reachable_cities[city][distance] """

        reachable_cities = {city: {0: set(city), 1: set()} for city in cities}
        for a, b in network:
            reachable_cities[a][1] |= {b}
            reachable_cities[b][1] |= {a}

        for distance in range(0, max_power):
            for city in cities:
                currently_reachable = reachable_cities[city][distance]
                new_reachable = {b for a in currently_reachable for b in reachable_cities[a][1]}
                reachable_cities[city][distance + 1] = currently_reachable | new_reachable

        return reachable_cities

    reachable_cities = get_reachable_cities(max(plants_counter))

    Step = namedtuple('Step', ['unpowered', 'plants', 'plants_counter'])
    q = [Step(unpowered=cities, plants=(), plants_counter=plants_counter)]

    while q:
        unpowered, plants, plants_counter = q.pop()

        current_plant_type = max(plants_counter)
        current_plant_type_count = plants_counter[current_plant_type]

        print('Pop:')
        print('    Unpowered:', unpowered)
        print('    Plants:', plants)
        print('    Plants counter:', plants_counter)
        print('    Current plant type:', current_plant_type)
        print('    Current plant type count:', current_plant_type_count)
        print()

        for combination in combinations(unpowered, current_plant_type_count):

            new_powered = set()
            new_plants = dict(plants)
            for city in combination:
                new_powered |= reachable_cities[city][current_plant_type]
                new_plants[city] = current_plant_type
            new_unpowered = unpowered - new_powered

            if new_unpowered:
                new_plants_counter = dict(plants_counter)
                del new_plants_counter[current_plant_type]
                if new_plants_counter:
                    q.append(Step(unpowered=new_unpowered, plants=new_plants, plants_counter=new_plants_counter))
            else:
                print('Plants:', new_plants)
                return new_plants

        q.sort(key=lambda step: -len(step.unpowered))

    return dict()


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
         ["Q", "V"], ["R", "W"], ["S", "X"], ["T", "Y"]], [2, 1, 1, 1, 1]) == {'M': 2, 'U': 1, 'A': 1, 'Y': 1, 'E': 1}
