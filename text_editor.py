class Text:
    text = ''
    font = None

    def __repr__(self):
        return f'Text: {self.text} [{self.font}]'

    def write(self, new_text):
        self.text += new_text
        print('Setting text:', self.text)
        print()

    def set_font(self, new_font):
        self.font = new_font

        print('Setting font:', self.font)
        print()

    def show(self):
        font_tag = f'[{self.font}]' if self.font else ''

        print('Show text:', font_tag + self.text + font_tag)
        print()

        return font_tag + self.text + font_tag

    def restore(self, text_memento):

        print('Before:', self)

        print('Restoring form:', text_memento)

        self.text = text_memento.text
        self.font = text_memento.font

        print('After:', self)
        print()

    def copy(self):
        new_text = Text()
        new_text.text = self.text
        new_text.font = self.font

        print('Copying:', self)
        print('New text:', new_text)
        print()

        return new_text


class SavedText:
    text_version = 0
    saved_texts = {}

    def save_text(self, new_text: Text):
        self.saved_texts[self.text_version] = new_text.copy()
        self.text_version += 1

        print('Self saved texts:', self.saved_texts)
        print()

    def get_version(self, text_version):
        return self.saved_texts[text_version]


if __name__ == '__main__':
    text = Text()
    saver = SavedText()

    text.write("At the very beginning ")
    saver.save_text(text)

    text.set_font("Arial")
    saver.save_text(text)

    text.write("there was nothing.")

    assert text.show() == "[Arial]At the very beginning there was nothing.[Arial]"

    text.restore(saver.get_version(0))
    assert text.show() == "At the very beginning "
