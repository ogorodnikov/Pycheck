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


def fight(unit_1, unit_2):
    while True:
        for attacker, defender in (unit_1, unit_2), (unit_2, unit_1):
            defender.health -= attacker.attack
            if not defender.is_alive:
                return defender == unit_2


if __name__ == '__main__':
    chuck = Warrior()
    bruce = Warrior()
    carl = Knight()
    dave = Warrior()
    mark = Warrior()

    assert fight(chuck, bruce) == True
    assert fight(dave, carl) == False
    assert chuck.is_alive == True
    assert bruce.is_alive == False
    assert carl.is_alive == True
    assert dave.is_alive == False
    assert fight(carl, mark) == False
    assert carl.is_alive == False
