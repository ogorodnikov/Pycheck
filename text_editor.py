class Text:
    text = font = ''

    def write(self, new_text):
        self.text += new_text

    def set_font(self, new_font):
        self.font = new_font

    def restore(self, text_memento):
        self.text = text_memento.text
        self.font = text_memento.font

    def copy(self):
        new_text = Text()
        new_text.text = self.text
        new_text.font = self.font
        return new_text

    def show(self):
        font_tag = self.font and f'[{self.font}]'
        return font_tag + self.text + font_tag


class SavedText:
    current_version = 0
    saved_texts = {}

    def save_text(self, text_to_save):
        self.saved_texts[self.current_version] = text_to_save.copy()
        self.current_version += 1

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
