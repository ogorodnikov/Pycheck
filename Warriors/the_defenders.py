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


class Defender(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 60
        self.attack = 3
        self.defense = 2


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


def fight(unit_a, unit_b):
    while True:
        for attacker, defender in (unit_a, unit_b), (unit_b, unit_a):
            defender.health -= attacker.attack
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

if False:
    class Warrior:
        def __init__(self):
            self.health = 50
            self.attack = 5
            self.defense = 0

        @property
        def is_alive(self) -> bool:
            return self.health > 0


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


    ####################################################################

    class Army:
        def __init__(self):
            self.soldiers = []

        def add_units(self, unit, quantity):
            print("Adding:", unit.__name__, quantity)
            self.soldiers += [unit() for i in range(quantity)]
            print(len(self.soldiers), "total")


    class Battle:
        def fight(self, army_1, army_2):
            print("Battle:", len(army_1.soldiers), "vs", len(army_2.soldiers))
            for i in range(1000):
                print("Scene", i)
                alive_1 = [s.is_alive for s in army_1.soldiers]
                alive_2 = [s.is_alive for s in army_2.soldiers]
                print(''.join(['+' * a + '_' * (not a) for a in alive_1]))
                print(''.join(['+' * a + '_' * (not a) for a in alive_2]))
                if not any(alive_2):
                    print("Army 1 won!\n")
                    return True
                elif not any(alive_1):
                    print("Army 2 won!\n")
                    return False
                else:
                    current_1 = [s for s in army_1.soldiers if s.is_alive][0]
                    current_2 = [s for s in army_2.soldiers if s.is_alive][0]
                    fight(current_1, current_2)


    def fight(unit_1, unit_2):
        print(f"{unit_1.__class__.__name__}[{unit_1.health} {unit_1.attack} {unit_1.defense}] vs " +
              f"{unit_2.__class__.__name__}[{unit_2.health} {unit_2.attack} {unit_2.defense}]")
        for i in range(100):
            unit_2.health -= max(unit_1.attack - unit_2.defense, 0)
            print(f"Round {i}: {unit_1.health:2} > {unit_2.health:2}")
            if unit_2.health > 0:
                unit_1.health -= max(unit_2.attack - unit_1.defense, 0)
                print(f"{unit_1.health:{11 + i // 10}} < {unit_2.health:2}")
            if unit_2.health <= 0:
                print("Unit 1 won!\n")
                return True
            if unit_1.health <= 0:
                print("Unit 2 won!\n")
                return False
        return None