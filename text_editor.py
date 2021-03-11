class Text:
    text = ''
    font = None

    def write(self, new_text):
        self.text += new_text
        print('Self text:', self.text)

    def set_font(self, new_font):
        self.font = new_font
        print('Self font:', self.font)

    def show(self):
        font_tag = self.font and f'[{self.font}]'
        print('Show text:', font_tag + self.text + font_tag)
        return font_tag + self.text + font_tag


class SavedText:

    def save_text(self, text):
        pass


if __name__ == '__main__':
    text = Text()
    saver = SavedText()

    text.write("At the very beginning ")
    saver.save_text(text)
    text.set_font("Arial")
    saver.save_text(text)
    text.write("there was nothing.")

    assert text.show() == "[Arial]At the very beginning there was nothing.[Arial]"

    # text.restore(saver.get_version(0))
    # assert text.show() == "At the very beginning "