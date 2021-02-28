from contextlib import suppress


class Warrior:
    warriors_count = 0
    max_health = 50

    def __init__(self):
        self.health = self.__class__.max_health
        self.attack = 5
        self.defense = 0
        self.vampirism = 0
        self.splash = 0
        self.healing = 0
        self.warrior_id = Warrior.warriors_count
        Warrior.warriors_count += 1

    def __repr__(self):
        return f'{self.__class__.__name__:8} #{self.warrior_id:2} HP: {self.health:4}'

    @property
    def is_alive(self):
        return self.health > 0

    def hit(self, defender, hit_mode):
        damage_dealt = defender.receive_hit(self, hit_mode)
        self.vampirate(damage_dealt)

    def receive_hit(self, attacker, hit_mode):
        if hit_mode == 'attack':
            damage = attacker.attack
        elif hit_mode == 'splash':
            damage = attacker.attack * attacker.splash
        else:
            raise ValueError

        damage_limited = max(damage - self.defense, 0)
        damage_received = min(damage_limited, self.health)

        self.health -= damage_received
        return damage_received

    def vampirate(self, damage_dealt):
        vampirism_hp_received = damage_dealt * self.vampirism / 100
        hp_to_maximum = self.__class__.max_health - self.health

        vampirism_hp_used = min(vampirism_hp_received, hp_to_maximum)
        self.health += vampirism_hp_used

    def heal(self, heal_target):
        if not heal_target.is_alive or not self.is_alive:
            return
        hp_to_maximum = heal_target.__class__.max_health - heal_target.health
        healed_hp = min(self.healing, hp_to_maximum)
        heal_target.health += healed_hp


class Knight(Warrior):
    def __init__(self):
        super().__init__()
        self.attack = 7


class Defender(Warrior):
    max_health = 60

    def __init__(self):
        super().__init__()
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
        self.attack = 6
        self.splash = 0.5


class Healer(Warrior):
    max_health = 60

    def __init__(self):
        super().__init__()
        self.attack = 0
        self.healing = 2


class Army:
    armies_count = 0

    def __init__(self, units=None):
        if units is None:
            units = []
        self.units = units.copy()
        self.army_id = Army.armies_count
        Army.armies_count += 1

    def __repr__(self):
        return f'{self.__class__.__name__} {self.army_id}'

    def add_units(self, unit, unit_count):
        for _ in range(unit_count):
            self.units.insert(0, unit())

    def attack(self, defending_army):
        return defending_army.receive_attack(self)

    def receive_attack(self, attacking_army):
        first_defending_unit = self.units[-1]
        first_attacking_unit = attacking_army.units[-1]
        first_attacking_unit.hit(first_defending_unit, hit_mode='attack')

        with suppress(IndexError):
            second_defending_unit = self.units[-2]
            first_attacking_unit.hit(second_defending_unit, hit_mode='splash')
            second_defending_unit.heal(first_defending_unit)

            if not second_defending_unit.is_alive:
                self.units.remove(second_defending_unit)

        if not first_defending_unit.is_alive:
            self.units.remove(first_defending_unit)
            return True


class Battle:
    @staticmethod
    def fight(army_a, army_b):

        while True:
            for attacking_army, defending_army in (army_a, army_b), (army_b, army_a):

                is_defender_perished = attacking_army.attack(defending_army)

                if not defending_army.units:
                    # print('Winner:', attacking_army)
                    return defending_army == army_b

                if is_defender_perished:
                    break

    @staticmethod
    def straight_fight(army_a, army_b):

        while True:
            for unit_a, unit_b in zip(army_a.units, army_b.units):
                # print('Pair:', (unit_a, unit_b))

                is_defender_perished = fight(unit_a, unit_b)
                # print('Is defender perished:', is_defender_perished)
                if is_defender_perished:
                    army_b.units.remove(unit_b)
                else:
                    army_a.units.remove(unit_a)

                # print('Army A units:', army_a.units)
                # print('Army B units:', army_b.units)

            if not army_b.units:
                print('Army A won')
                # print('Army A units:', army_a.units)
                # print('Army B units:', army_b.units)
                return True

            if not army_a.units:
                print('Army B won')
                # print('Army A units:', army_a.units)
                # print('Army B units:', army_b.units)
                return False


def fight(unit_a, unit_b):
    return Battle.fight(Army([unit_a]), Army([unit_b]))


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
    priest = Healer()

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
    assert freelancer.health == 14
    priest.heal(freelancer)
    assert freelancer.health == 16

    # battle tests
    my_army = Army()
    my_army.add_units(Defender, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Vampire, 2)
    my_army.add_units(Lancer, 2)
    my_army.add_units(Healer, 1)
    my_army.add_units(Warrior, 1)

    enemy_army = Army()
    enemy_army.add_units(Warrior, 2)
    enemy_army.add_units(Lancer, 4)
    enemy_army.add_units(Healer, 1)
    enemy_army.add_units(Defender, 2)
    enemy_army.add_units(Vampire, 3)
    enemy_army.add_units(Healer, 1)

    army_3 = Army()
    army_3.add_units(Warrior, 1)
    army_3.add_units(Lancer, 1)
    army_3.add_units(Healer, 1)
    army_3.add_units(Defender, 2)

    army_4 = Army()
    army_4.add_units(Vampire, 3)
    army_4.add_units(Warrior, 1)
    army_4.add_units(Healer, 1)
    army_4.add_units(Lancer, 2)

    army_5 = Army()
    army_5.add_units(Warrior, 10)

    army_6 = Army()
    army_6.add_units(Warrior, 6)
    army_6.add_units(Lancer, 5)

    battle = Battle()

    assert battle.fight(my_army, enemy_army) == False
    assert battle.fight(army_3, army_4) == True
    assert battle.straight_fight(army_5, army_6) == False

    # mission check tests

    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Lancer, 7)
    army_1.add_units(Vampire, 3)
    army_1.add_units(Warrior, 4)
    army_1.add_units(Defender, 2)
    army_2.add_units(Warrior, 4)
    army_2.add_units(Defender, 4)
    army_2.add_units(Vampire, 6)
    army_2.add_units(Lancer, 4)

    battle = Battle()

    assert battle.straight_fight(army_1, army_2) == True