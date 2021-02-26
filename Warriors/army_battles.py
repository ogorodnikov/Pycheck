class Warrior:
    def __init__(self):
        self.health = 50
        self.attack = 5

    @property
    def is_alive(self):
        return self.health > 0


class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.attack = 7

    @property
    def is_alive(self):
        return self.health > 0


class Army:
    def __init__(self):
        self.units = []

    def add_units(self, unit, unit_count):
        for _ in range(unit_count):
            self.units.append(unit())


class Battle:
    def fight(self, army_a, army_b):

        current_warrior_a = army_a.units.pop()
        current_warrior_b = army_b.units.pop()

        while True:

            is_winner_a = fight(current_warrior_a, current_warrior_b)

            if is_winner_a:
                if army_b.units:
                    current_warrior_b = army_b.units.pop()
                else:
                    return True
            else:
                if army_a.units:
                    current_warrior_a = army_a.units.pop()
                else:
                    return False


def fight(unit_1, unit_2):
    while True:
        for attacker, defender in (unit_1, unit_2), (unit_2, unit_1):
            defender.health -= attacker.attack
            if not defender.is_alive:
                return defender == unit_2


if __name__ == '__main__':
    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()

    assert fight(chuck, bruce) == True
    assert fight(dave, carl) == False
    assert chuck.is_alive == True
    assert bruce.is_alive == False
    assert carl.is_alive == True
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False

    # battle tests
    my_army = Army()
    my_army.add_units(Knight, 3)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 20)
    army_3.add_units(Knight, 5)

    army_4 = Army()
    army_4.add_units(Warrior, 30)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == True
    assert battle.fight(army_3, army_4) == False
