class Army:

    def train_swordsman(self, name):
        return Swordsman(self, name)

    def train_lancer(self, name):
        return Lancer(self, name)

    def train_archer(self, name):
        return Archer(self, name)


class Warrior:
    specialization = ''

    def __init__(self, army, name):
        self.name = name
        self.army_type = army.army_type
        self.unit_type = getattr(army, self.specialization)

    def introduce(self):
        introduction = f'{self.unit_type} {self.name}, {self.army_type} {self.specialization}'
        print(introduction)
        return introduction


class Swordsman(Warrior):
    specialization = 'swordsman'


class Lancer(Warrior):
    specialization = 'lancer'


class Archer(Warrior):
    specialization = 'archer'


class AsianArmy(Army):
    army_type = 'Asian'
    swordsman = 'Samurai'
    lancer = 'Ronin'
    archer = 'Shinobi'


class EuropeanArmy(Army):
    army_type = 'European'
    swordsman = 'Knight'
    lancer = 'Raubritter'
    archer = 'Ranger'


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