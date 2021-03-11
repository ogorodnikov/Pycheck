class Lamp:

    def __init__(self):
        self._colors = ['Green', 'Red', 'Blue', 'Yellow']

    def light(self):
        try:
            color = self._colors.pop(0)
            return color
        finally:
            self._colors.append(color)


if __name__ == '__main__':
    lamp_1 = Lamp()
    lamp_2 = Lamp()

    lamp_1.light()  # Green
    lamp_1.light()  # Red
    lamp_2.light()  # Green

    assert lamp_1.light() == "Blue"
    assert lamp_1.light() == "Yellow"
    assert lamp_1.light() == "Green"
    assert lamp_2.light() == "Red"
    assert lamp_2.light() == "Blue"
