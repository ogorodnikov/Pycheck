from contextlib import suppress


class Warrior:
    warriors_count = 0
    max_health = 50
    equipment = []

    def __init__(self):
        self.max_health = type(self).max_health
        self._health = self.max_health
        self.attack = 5
        self.defense = 0
        self.vampirism = 0
        self.splash = 0
        self.heal_power = 0
        self.warrior_id = Warrior.warriors_count
        Warrior.warriors_count += 1

    @property
    def health(self):
        health_by_equipment = sum(e.health for e in self.equipment)
        return self._health + health_by_equipment

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
        vampirism_hp_received = int(damage_dealt * self.vampirism / 100)
        hp_to_maximum = self.__class__.max_health - self.health

        vampirism_hp_used = min(vampirism_hp_received, hp_to_maximum)
        self.health += vampirism_hp_used

    def heal(self, heal_target):
        if not heal_target.is_alive or not self.is_alive:
            return
        hp_to_maximum = heal_target.__class__.max_health - heal_target.health
        healed_hp = min(self.heal_power, hp_to_maximum)
        heal_target.health += healed_hp

    def equip_weapon(self, weapon_name):
        self.equipment.append(weapon_name)

        print('Equipping:', weapon_name)
        print('Equipment:', self.equipment)


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
        self.heal_power = 2


class Weapon:
    health = 0
    attack = 0
    defense = 0
    vampirism = 0
    heal_power = 0

    def __init__(self, health=0, attack=0, defense=0, vampirism=0, heal_power=0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.vampirism = vampirism
        self.heal_power = heal_power


class Sword(Weapon):
    health = 5
    attack = 2


class Shield(Weapon):
    health = 20
    attack = -1
    defense = 2


class GreatAxe(Weapon):
    health = -15
    attack = 5
    defense = -2
    vampirism = 10


class Katana(Weapon):
    health = -20
    attack = 6
    defense = -5
    vampirism = 50


class MagicWand(Weapon):
    health = 30
    attack = 3
    heal_power = 3


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
            for unit_a, unit_b in zip(reversed(army_a.units.copy()),
                                      reversed(army_b.units.copy())):

                is_defender_perished = fight(unit_a, unit_b)

                if is_defender_perished:
                    army_b.units.remove(unit_b)
                else:
                    army_a.units.remove(unit_a)

            if not army_b.units:
                # print('Army A won')
                return True

            if not army_a.units:
                # print('Army B won')
                return False


def fight(unit_a, unit_b):
    return Battle.fight(Army([unit_a]), Army([unit_b]))


if __name__ == '__main__':
    ogre = Warrior()
    lancelot = Knight()
    richard = Defender()
    eric = Vampire()
    freelancer = Lancer()
    priest = Healer()

    sword = Sword()
    shield = Shield()
    axe = GreatAxe()
    katana = Katana()
    wand = MagicWand()
    super_weapon = Weapon(50, 10, 5, 150, 8)

    ogre.equip_weapon(sword)
    ogre.equip_weapon(shield)
    ogre.equip_weapon(super_weapon)
    lancelot.equip_weapon(super_weapon)
    richard.equip_weapon(shield)
    eric.equip_weapon(super_weapon)
    freelancer.equip_weapon(axe)
    freelancer.equip_weapon(katana)
    priest.equip_weapon(wand)
    priest.equip_weapon(shield)

    assert ogre.health == 125
    lancelot.attack == 17
    richard.defense == 4
    eric.vampirism == 200
    freelancer.health == 15
    priest.heal_power == 5

    fight(ogre, eric) == False
    fight(priest, richard) == False
    fight(lancelot, freelancer) == True

    my_army = Army()
    my_army.add_units(Knight, 1)
    my_army.add_units(Lancer, 1)

    enemy_army = Army()
    enemy_army.add_units(Vampire, 1)
    enemy_army.add_units(Healer, 1)

    my_army.units[0].equip_weapon(axe)
    my_army.units[1].equip_weapon(super_weapon)

    enemy_army.units[0].equip_weapon(katana)
    enemy_army.units[1].equip_weapon(wand)

    battle = Battle()

    battle.fight(my_army, enemy_army) == True
