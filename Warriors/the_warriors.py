class Warrior:
    pass


class Knight(Warrior):
    pass


def fight(unit_1, unit_2):
    return 0


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

if False:
    class Warrior:
        def __init__(self):
            self.hp = 50
            self.attack = 5
            print(self.hp, self.attack)

        @property
        def is_alive(self) -> bool:
            return self.hp > 0


    class Knight(Warrior):
        def __init__(self):
            super().__init__()
            self.attack = 7
            print(self.hp, self.attack)


    def fight(unit_1, unit_2):
        print(f"{unit_1.__class__.__name__}[{unit_1.hp, unit_1.attack}] and " +
              f"{unit_2.__class__.__name__}[{unit_1.hp, unit_1.attack}] are fighting")

        for i in range(100):
            print("Round", i)
            unit_2.hp -= unit_1.attack
            print(unit_1.hp, ">", unit_2.hp)
            if unit_2.hp > 0:
                unit_1.hp -= unit_2.attack
                print(unit_1.hp, "<", unit_2.hp)
            if unit_2.hp <= 0:
                print("Unit 1 won!")
                return True
            if unit_1.hp <= 0:
                print("Unit 2 won!")
                return False
        return 0
