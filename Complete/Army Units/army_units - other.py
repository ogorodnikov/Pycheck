class Army:
    def train_swordsman(self, name): return Swordsman(self, name)

    def train_lancer(self, name): return Lancer(self, name)

    def train_archer(self, name): return Archer(self, name)


class Soldier:
    def __init__(self, army, name):
        self.name = name
        self.descent = army.descent
        self.title = getattr(army, self.category)

    def introduce(self):
        return f'{self.title} {self.name}, {self.descent} {self.category}'


class Swordsman(Soldier): category = 'swordsman'


class Lancer(Soldier): category = 'lancer'


class Archer(Soldier): category = 'archer'


class AsianArmy(Army):
    descent = 'Asian'
    swordsman, lancer, archer = 'Samurai', 'Ronin', 'Shinobi'


class EuropeanArmy(Army):
    descent = 'European'
    swordsman, lancer, archer = 'Knight', 'Raubritter', 'Ranger'


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
