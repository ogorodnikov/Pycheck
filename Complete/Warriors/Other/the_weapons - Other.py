from contextlib import suppress
from collections import namedtuple

Weapon = namedtuple('Weapon', 'health attack defense vampirism heal_power',
                    defaults=(0, 0, 0, 0, 0))


class Sword(Weapon):
    def __new__(cls):
        return super().__new__(cls, health=5, attack=2)


class Shield(Weapon):
    def __new__(cls):
        return super().__new__(cls, health=20, attack=-1, defense=2)


class GreatAxe(Weapon):
    def __new__(cls):
        return super().__new__(cls, health=-15, attack=5, defense=-2, vampirism=10)


class Katana(Weapon):
    def __new__(cls):
        return super().__new__(cls, health=-20, attack=6, defense=-5, vampirism=50)


class MagicWand(Weapon):
    def __new__(cls):
        return super().__new__(cls, health=30, attack=3, heal_power=3)


class Weapons(list):
    def total(self, attrname):
        return sum(getattr(weapon, attrname) for weapon in self)


class Warrior:
    warriors_count = 0
    _health = 50
    _attack = 5

    def __init__(self):
        self.weapons = Weapons()

        self.warrior_id = Warrior.warriors_count
        Warrior.warriors_count += 1

    def __getattr__(self, attrname):
        if attrname in Weapon._fields:
            return max(getattr(self, '_' + attrname) + self.weapons.total(attrname), 0)
        else:
            raise AttributeError

    def __setattr__(self, attrname, value):
        if attrname in Weapon._fields:
            setattr(self, '_' + attrname, value - self.weapons.total(attrname))
        else:
            super().__setattr__(attrname, value)

    def __repr__(self):

        header = f'{self.__class__.__name__} ({self.warrior_id}) '
        header += f'HP: {self.health}/{self.max_health}({type(self)._health})'
        # equipment = ''.join(str(f'{element}\n') for element in self.equipment)
        # basic = f'Basic:    A:{type(self)._attack} D:{type(self)._defense} '
        # basic += f'V:{type(self)._vampirism} S:{type(self)._splash} H:{type(self)._heal_power}'

        # if any(getattr(self, '_' + parameter) != getattr(type(self), '_' + parameter)
        #        for parameter in 'attack defense vampirism splash heal_power'.split()):
        #     modified = f'Modified: A:{self.attack} D:{self.defense} '
        #     modified += f'V:{self.vampirism} S:{self.splash} H:{self.heal_power}'
        # else:
        #     modified = ''

        repr_string = header
        return repr_string

    @property
    def max_health(self):
        return max(type(self)._health + self.weapons.total('health'), 0)

    def hit_by(self, enemy_attack):
        self.health -= enemy_attack
        return enemy_attack

    def strike(self, enemy):
        enemy.hit_by(self.attack)

    @property
    def is_alive(self):
        return self.health > 0

    def equip_weapon(self, weapon):
        self.weapons.append(weapon)


class Knight(Warrior):
    _attack = 7


class Defender(Warrior):
    _health = 60
    _attack = 3
    _defense = 2

    def hit_by(self, enemy_attack):
        damage = max(enemy_attack - self.defense, 0)
        self.health -= damage
        return damage


class Vampire(Warrior):
    _health = 40
    _attack = 4
    _vampirism = 50

    def strike(self, enemy):
        damage = enemy.hit_by(self.attack)

        vampirism_hp_received = int(damage * self.vampirism / 100)
        hp_to_maximum = self.max_health - self.health

        vampirism_hp_used = min(vampirism_hp_received, hp_to_maximum)
        if vampirism_hp_used:
            print('>>> Vampirism hp used:', vampirism_hp_used)

        self.health = min(self.health + int(damage * self.vampirism / 100), self.max_health)


class Lancer(Warrior):
    _health = 50
    _attack = 6

    def strike(self, enemy):
        damage = enemy.hit_by(self.attack)
        with suppress(AttributeError):
            enemy.next_unit.hit_by(int(damage / 2))


class Healer(Warrior):
    _health = 60
    _attack = 0
    _heal_power = 2

    def heal(self, ally):
        ally.health = min(ally.health + self.heal_power, ally.max_health)


def fight(unit_1, unit_2):
    attacker, defender = unit_1, unit_2
    while True:
        print(f'{attacker}    VS    {defender}')
        attacker.strike(defender)
        with suppress(AttributeError):
            attacker.next_unit.heal(attacker)
        if not defender.is_alive:
            return attacker is unit_1
        attacker, defender = defender, attacker


class Rookie(Warrior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health = 50
        self.attack = 1


class Army(list):
    units = property(lambda self: self)  # for army.units[0]...

    def add_units(self, unit_cls, n):
        self.extend(unit_cls() for _ in range(n))

    def alive(self):
        return (x for x in self if x.is_alive)

    @property
    def has_alive(self):
        return any(x.is_alive for x in self)

    def first_alive(self):
        alive = self.alive()
        unit = next(alive, None)
        if unit is not None:
            unit.next_unit = next(alive, None)
        return unit


class Battle:
    def fight(self, army1, army2):
        while True:
            unit1 = army1.first_alive()
            if unit1 is None:
                return False
            unit2 = army2.first_alive()
            if unit2 is None:
                return True
            fight(unit1, unit2)

    def straight_fight(self, army1, army2):
        level = 0
        while True:
            print()
            print('=== Level:', level)
            print()
            level += 1
            print('Army 0:')
            [print(unit) for unit in army1 if unit.is_alive]
            print()
            print('Army 1:')
            [print(unit) for unit in army2 if unit.is_alive]
            print()

            for unit1, unit2 in zip(army1.alive(), army2.alive()):
                is_defender_perished = fight(unit1, unit2)
                if is_defender_perished:
                    victor = unit1
                else:
                    victor = unit2
                print(victor, 'won')
                print()
            if not army1.has_alive:
                return False
            elif not army2.has_alive:
                return True


if __name__ == '__main__':
    # ogre = Warrior()
    # lancelot = Knight()
    # richard = Defender()
    # eric = Vampire()
    # freelancer = Lancer()
    # priest = Healer()
    #
    # sword = Sword()
    # shield = Shield()
    # axe = GreatAxe()
    # katana = Katana()
    # wand = MagicWand()
    # super_weapon = Weapon(50, 10, 5, 150, 8)
    #
    # ogre.equip_weapon(sword)
    # ogre.equip_weapon(shield)
    # ogre.equip_weapon(super_weapon)
    # lancelot.equip_weapon(super_weapon)
    # richard.equip_weapon(shield)
    # eric.equip_weapon(super_weapon)
    # freelancer.equip_weapon(axe)
    # freelancer.equip_weapon(katana)
    # priest.equip_weapon(wand)
    # priest.equip_weapon(shield)
    #
    # assert ogre.health == 125
    # assert lancelot.attack == 17
    # assert richard.defense == 4
    # assert eric.vampirism == 200
    # assert freelancer.health == 15
    # assert priest.heal_power == 5
    #
    # assert fight(ogre, eric) == False
    # assert fight(priest, richard) == False
    # assert fight(lancelot, freelancer) == True
    #
    # my_army = Army()
    # my_army.add_units(Knight, 1)
    # my_army.add_units(Lancer, 1)
    #
    # enemy_army = Army()
    # enemy_army.add_units(Vampire, 1)
    # enemy_army.add_units(Healer, 1)
    #
    # my_army.units[0].equip_weapon(axe)
    # my_army.units[1].equip_weapon(super_weapon)
    #
    # enemy_army.units[0].equip_weapon(katana)
    # enemy_army.units[1].equip_weapon(wand)
    #
    # battle = Battle()
    #
    # assert battle.fight(my_army, enemy_army) == True
    #
    # # mission tests
    #
    # weapon_1 = Katana()
    # weapon_2 = Shield()
    #
    # my_army = Army()
    # my_army.add_units(Vampire, 2)
    # my_army.add_units(Rookie, 2)
    #
    # enemy_army = Army()
    # enemy_army.add_units(Warrior, 1)
    # enemy_army.add_units(Defender, 2)
    #
    # my_army.units[0].equip_weapon(weapon_1)
    # my_army.units[1].equip_weapon(weapon_1)
    # my_army.units[2].equip_weapon(weapon_2)
    #
    # enemy_army.units[0].equip_weapon(weapon_1)
    # enemy_army.units[1].equip_weapon(weapon_2)
    # enemy_army.units[2].equip_weapon(weapon_2)
    #
    # battle = Battle()
    #
    # assert battle.straight_fight(my_army, enemy_army) == True

    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Lancer, 7)
    army_1.add_units(Vampire, 3)
    army_1.add_units(Healer, 1)
    army_1.add_units(Warrior, 4)
    army_1.add_units(Healer, 1)
    army_1.add_units(Defender, 2)
    army_2.add_units(Warrior, 4)
    army_2.add_units(Defender, 4)
    army_2.add_units(Healer, 1)
    army_2.add_units(Vampire, 6)
    army_2.add_units(Lancer, 4)

    battle = Battle()

    assert battle.straight_fight(army_1, army_2) == False
