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
        equipment = '\n'.join(str(f'{element}') for element in self.weapons)
        # basic = f'Basic:    A:{type(self)._attack} D:{type(self)._defense} '
        # basic += f'V:{type(self)._vampirism} S:{type(self)._splash} H:{type(self)._heal_power}'

        # if any(getattr(self, '_' + parameter) != getattr(type(self), '_' + parameter)
        #        for parameter in 'attack defense vampirism splash heal_power'.split()):
        #     modified = f'Modified: A:{self.attack} D:{self.defense} '
        #     modified += f'V:{self.vampirism} S:{self.splash} H:{self.heal_power}'
        # else:
        #     modified = ''

        repr_string = header + equipment
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

    @classmethod
    def can_join(cls, army):
        return True


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


class Warlord(Defender):
    _health = 100
    _attack = 4
    _defense = 2

    @classmethod
    def can_join(cls, army):
        return not army.has_type(cls)


class Rookie(Warrior):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health = 50
        self.attack = 1


def fight(unit_1, unit_2, check_next=False):
    attacker, defender = unit_1, unit_2
    while True:

        attacker_str = f'{attacker}'[:50]
        defender_str = f'{defender}'[:50]
        print(f'{attacker_str:50}    VS    {defender_str:50}')

        attacker.strike(defender)
        with suppress(AttributeError):
            attacker.next_unit.heal(attacker)
        if not defender.is_alive:
            return attacker is unit_1
        if check_next:
            with suppress(AttributeError):
                if not defender.next_unit.is_alive:
                    break
        attacker, defender = defender, attacker


class Army(list):
    units = property(lambda self: self)  # for army.units[0]...

    def add_units(self, unit_cls, n):
        for _ in range(n):
            if unit_cls.can_join(self):
                self.append(unit_cls())

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

    def has_type(self, unit_cls):
        return any(isinstance(unit, unit_cls) for unit in self)

    def move_units(self):
        # as there are no rules for the dead units, move them to graveyard
        self[:] = [unit for unit in self if unit.is_alive]

        print()
        print('<<< Before')
        [print(unit) for unit in self]
        print()

        # rule 6:
        warlord = next((unit for unit in self if isinstance(unit, Warlord)), None)
        if warlord is None:
            print('No Warlord')
            return
        self.remove(warlord)

        # rule 1:
        self.sort(key=lambda unit: not isinstance(unit, Lancer))

        # rule 2:
        healers = [unit for unit in self if isinstance(unit, Healer)]
        not_healers = [unit for unit in self if not isinstance(unit, Healer)]
        self[:] = not_healers[:1] + healers + not_healers[1:]

        # rule 3:
        if not self.has_type(Lancer):
            attacker_index = next((i for i, unit in enumerate(self) if unit.attack > 0), None)
            if attacker_index:  # neither None nor 0
                self[0], self[attacker_index] = self[attacker_index], self[0]

        # rule 4:
        self.append(warlord)

        print('>>> After:')
        [print(unit) for unit in self]
        print()


class Battle:
    def fight(self, army1, army2):
        while True:
            army1.move_units()
            unit1 = army1.first_alive()
            if unit1 is None:
                return False
            army2.move_units()
            unit2 = army2.first_alive()
            if unit2 is None:
                return True
            fight(unit1, unit2, True)

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

    # mission tests

    army_1 = Army()
    army_2 = Army()
    army_1.add_units(Warrior, 2)
    army_1.add_units(Lancer, 3)
    army_1.add_units(Defender, 1)
    army_1.add_units(Warlord, 1)
    army_2.add_units(Warlord, 5)
    army_2.add_units(Vampire, 1)
    army_2.add_units(Rookie, 1)
    army_2.add_units(Knight, 1)
    army_1.units[0].equip_weapon(Sword())
    army_2.units[0].equip_weapon(Shield())
    army_1.move_units()
    army_2.move_units()

    battle = Battle()

    assert battle.straight_fight(army_1, army_2) == False