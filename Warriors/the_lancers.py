class Warrior:
    warriors_count = 0
    max_health = 50

    def __init__(self):
        self.health = self.__class__.max_health
        self.attack = 5
        self.defense = 0
        self.vampirism = 0
        self.splash = 0

        self.warrior_id = Warrior.warriors_count
        Warrior.warriors_count += 1

    def __repr__(self):
        return f'{self.__class__.__name__:8} #{self.warrior_id} HP: {self.health}'

    @property
    def is_alive(self):
        return self.health > 0

    def hit(self, defender):
        damage_dealt = defender.receive_hit(self)
        vampirism_dealt = damage_dealt * self.vampirism / 100
        self.health = min(self.__class__.max_health, self.health + vampirism_dealt)

    def splash_hit(self, defender):
        damage_dealt = defender.receive_splash_hit(self)
        vampirism_dealt = damage_dealt * self.vampirism / 100
        self.health = min(self.__class__.max_health, self.health + vampirism_dealt)

    def receive_hit(self, attacker):
        damage = max(attacker.attack - self.defense, 0)
        damage_received = min(damage, self.health)
        self.health -= damage_received
        return damage_received

    def receive_splash_hit(self, attacker):
        damage = max(attacker.splash - self.defense, 0)
        damage_received = min(damage, self.health)
        self.health -= damage_received
        return damage_received


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


class Vampire(Warrior):
    max_health = 40

    def __init__(self):
        super().__init__()
        self.attack = 4
        self.vampirism = 50


class Lancer(Warrior):
    def __init__(self):
        super().__init__()
        self.health = 50
        self.attack = 6
        self.splash = 0.5


class Army:
    armies_count = 0

    def __init__(self, units=[]):
        self.units = units.copy()

        self.army_id = Army.armies_count
        Army.armies_count += 1

    def __repr__(self):
        return f'{self.__class__.__name__} {self.army_id}'

    def add_units(self, unit, unit_count):
        for _ in range(unit_count):
            self.units.append(unit())

    def attack(self, defending_army):
        defending_army.receive_attack(self)

    def receive_attack(self, attacking_army):
        first_defending_unit = self.units[-1]
        first_attacking_unit = attacking_army.units[-1]

        print('        First attacking unit:', first_attacking_unit)
        print('        First defending unit:', first_defending_unit)

        first_attacking_unit.hit(first_defending_unit)

        try:
            second_defending_unit = self.units[-2]
            first_attacking_unit.splash_hit(second_defending_unit)

            if not second_defending_unit.is_alive:
                self.units.remove(second_defending_unit)
        except IndexError:
            pass

        if not first_defending_unit.is_alive:
            self.units.remove(first_defending_unit)


class Battle:
    @staticmethod
    def fight(army_a, army_b):
        # print('Fight between:')
        # print_army(army_a)
        # print_army(army_b)

        level = 0

        while True:
            # for i in range(100):
            print()
            print('Level:', level)
            level += 1

            for attacking_army, defending_army in (army_a, army_b), (army_b, army_a):
                print('Attacking:')
                print_army(attacking_army)
                print('Defending:')
                print_army(defending_army)

                attacking_army.attack(defending_army)

                if not defending_army.units:
                    print('=== Winner:', attacking_army)
                    return defending_army == army_b


def fight(unit_a, unit_b):
    return Battle.fight(Army([unit_a]), Army([unit_b]))


def print_army(army):
    units_count = len(army.units)
    tail_index = max(0, units_count - 2)

    print(army, ':')
    if tail_index > 0:
        print('    ...')
    for i, unit in enumerate(army.units[tail_index:], tail_index):
        print(f'    {i}) {unit} {unit.__dict__}')


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
    eric = Vampire()
    adam = Vampire()
    richard = Defender()
    ogre = Warrior()
    freelancer = Lancer()
    vampire = Vampire()

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
    assert fight(eric, richard) == False
    assert fight(ogre, adam) == True
    assert fight(freelancer, vampire) == True
    assert freelancer.is_alive == True

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 4)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 2)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Lancer, 2)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == True
    assert battle.fight(army_3, army_4) == False

    # # mission check tests
    #
    # army_1 = Army()
    # army_2 = Army()
    # army_1.add_units(Defender, 11)
    # army_1.add_units(Vampire, 3)
    # army_1.add_units(Warrior, 4)
    # army_2.add_units(Warrior, 4)
    # army_2.add_units(Defender, 4)
    # army_2.add_units(Vampire, 13)
    # battle = Battle()
    #
    # assert battle.fight(army_1, army_2) == True
