class HackerLanguage:
    _message = ''

    @staticmethod
    def encode(message):
        return message

    @staticmethod
    def decode(message):
        return message

    def write(self, text):
        self._message += text

    def delete(self, symbol_count):
        self._message = self._message[:len(self._message) - symbol_count]

    def send(self):
        return self.encode(self._message)

    def read(self, text):
        return self.decode(text)


if __name__ == '__main__':

    message_1 = HackerLanguage()
    message_1.write("secrit")
    message_1.delete(2)
    message_1.write("et")
    message_2 = HackerLanguage()

    assert message_1.send() == "111001111001011100011111001011001011110100"
    assert message_2.read("11001011101101110000111010011101100") == "email"
