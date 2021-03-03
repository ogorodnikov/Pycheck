class Warrior:

    def __init__(self, unit_type, name, army_type, specialization):
        self.unit_type = unit_type
        self.name = name
        self.army_type = army_type
        self.specialization = specialization

    def introduce(self):
        introduction = f'{self.unit_type} {self.name}, {self.army_type} {self.specialization}'
        print(introduction)
        return introduction


class Swordsman(Warrior):
    pass


class Lancer(Warrior):
    pass


class Archer(Warrior):
    pass


class Army:

    def train_swordsman_(self, unit_type, name, army_type):
        return Swordsman(unit_type, name, army_type, 'swordsman')

    def train_lancer_(self, unit_type, name, army_type):
        return Lancer(unit_type, name, army_type, 'lancer')

    def train_archer_(self, unit_type, name, army_type):
        return Archer(unit_type, name, army_type, 'archer')


class AsianArmy(Army):
    army_type = 'Asian'

    def train_swordsman(self, name):
        unit_type = 'Samurai'
        return super().train_swordsman_(unit_type, name, type(self).army_type)

    def train_lancer(self, name):
        unit_type = 'Ronin'
        return super().train_lancer_(unit_type, name, type(self).army_type)

    def train_archer(self, name):
        unit_type = 'Shinobi'
        return super().train_archer_(unit_type, name, type(self).army_type)


class EuropeanArmy(Army):
    army_type = 'European'

    def train_swordsman(self, name):
        unit_type = 'Knight'
        return super().train_swordsman_(unit_type, name, type(self).army_type)

    def train_lancer(self, name):
        unit_type = 'Raubritter'
        return super().train_lancer_(unit_type, name, type(self).army_type)

    def train_archer(self, name):
        unit_type = 'Ranger'
        return super().train_archer_(unit_type, name, type(self).army_type)


if __name__ == '__main__':
    my_army = EuropeanArmy()
    enemy_army = AsianArmy()

    soldier_1 = my_army.train_swordsman("Jaks")
    soldier_2 = my_army.train_lancer("Harold")
    soldier_3 = my_army.train_archer("Robin")

    soldier_4 = enemy_army.train_swordsman("Kishimoto")
    soldier_5 = enemy_army.train_lancer("Ayabusa")
    soldier_6 = enemy_army.train_archer("Kirigae")

    assert soldier_1.introduce() == "Knight Jaks, European swordsman"
    assert soldier_2.introduce() == "Raubritter Harold, European lancer"
    assert soldier_3.introduce() == "Ranger Robin, European archer"

    assert soldier_4.introduce() == "Samurai Kishimoto, Asian swordsman"
    assert soldier_5.introduce() == "Ronin Ayabusa, Asian lancer"
    assert soldier_6.introduce() == "Shinobi Kirigae, Asian archer"
