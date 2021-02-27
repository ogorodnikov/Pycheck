class Warrior:
    def __init__(self):
        self.health = 50
        self.attack = 5
        self.defense = 0

    @property
    def is_alive(self):
        return self.health > 0

    def hit(self, defender):
        defender.receive_hit(self)

    def receive_hit(self, attacker):
        self.health -= max(attacker.attack - self.defense, 0)


class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.attack = 7


class Defender(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.attack = 3
        self.defense = 2


class Rookie(Warrior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health = 50
        self.attack = 1


class Army:
    def __init__(self):
        self.units = []

    def add_units(self, unit, unit_count):
        for _ in range(unit_count):
            self.units.append(unit())


class Battle:
    @staticmethod
    def fight(army_a, army_b):

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


def fight(unit_a, unit_b):
    while True:
        for attacker, defender in (unit_a, unit_b), (unit_b, unit_a):
            attacker.hit(defender)
            if not defender.is_alive:
                return defender == unit_b


if __name__ == '__main__':

    # fight tests
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()
    bob = Defender()
    mike = Knight()
    rog = Warrior()
    lancelot = Defender()

    assert fight(chuck, bruce) == True
    assert fight(dave, carl) == False
    assert chuck.is_alive == True
    assert bruce.is_alive == False
    assert carl.is_alive == True
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False
    assert fight(bob, mike) == False
    assert fight(lancelot, rog) == True

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Defender, 1)

    army_4 = Army()
    army_4.add_units(Warrior, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == False
    assert battle.fight(army_3, army_4) == True