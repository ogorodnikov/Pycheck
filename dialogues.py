VOWELS = "aeiou"


class Chat:

    def __init__(self):
        self.participants = set()
        self.dialogue = []

    def connect_human(self, human):
        self.participants.add(human)
        human.current_chat = self

    connect_robot = connect_human

    @staticmethod
    def translate_to_robotic(human_phrase):
        robotic_phrase = ''.join('0' if letter in VOWELS + VOWELS.upper() else '1'
                                 for letter in human_phrase)
        return robotic_phrase

    def show_human_dialogue(self):
        dialogue_text = '\n'.join(f'{author.name} said: {phrase}'
                                  for author, phrase in self.dialogue)
        return dialogue_text

    def show_robot_dialogue(self):
        dialogue_text = '\n'.join(f'{author.name} said: {self.translate_to_robotic(phrase)}'
                                  for author, phrase in self.dialogue)
        return dialogue_text


class Author:
    def __init__(self, name):
        self.name = name
        self.current_chat = None

    def send(self, phrase):
        self.current_chat.dialogue.append((self, phrase))


class Human(Author):
    pass


class Robot(Author):
    pass


if __name__ == '__main__':
    chat = Chat()

    karl = Human("Karl")
    bot = Robot("R2D2")

    chat.connect_human(karl)
    chat.connect_robot(bot)

    karl.send("Hi! What's new?")
    bot.send("Hello, human. Could we speak later about it?")

    assert chat.show_human_dialogue() == """Karl said: Hi! What's new?
R2D2 said: Hello, human. Could we speak later about it?"""

    assert chat.show_robot_dialogue() == """Karl said: 101111011111011
R2D2 said: 10110111010111100111101110011101011010011011"""
