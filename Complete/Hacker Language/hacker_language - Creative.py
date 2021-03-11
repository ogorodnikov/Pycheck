import re

TRANSPARENT = lambda _, token: token
CHAR_TO_BITS = lambda _, token: f'{ord(token):<07b}'
BITS_TO_CHAR = lambda _, token: chr(int(token.replace('1000000', '100000'), 2))

ENCODE = {r'\d|[^\w\s]': TRANSPARENT, r'.': CHAR_TO_BITS}
DECODE = {r'[0|1]{7}': BITS_TO_CHAR, r'.': TRANSPARENT}


class HackerLanguage:
    _message = ''

    @staticmethod
    def transcode(message, code_dictionary):

        scanner = re.Scanner(list(code_dictionary.items()))
        tokens, unrecognised = scanner.scan(message)
        return ''.join(tokens)

    def write(self, text):
        self._message += text

    def delete(self, symbol_count):
        self._message = self._message[:-symbol_count]

    def send(self):
        return self.transcode(self._message, ENCODE)

    def read(self, text):
        return self.transcode(text, DECODE)


if __name__ == '__main__':
    message_1 = HackerLanguage()

    message_1.write("secrit")
    message_1.delete(2)
    message_1.write("et")
    message_2 = HackerLanguage()

    assert message_1.send() == "111001111001011100011111001011001011110100"
    assert message_2.read("11001011101101110000111010011101100") == "email"

    # mission tests

    message_3 = HackerLanguage()
    assert message_3.read(
        '1001001100000011000011101101100000011101001101001111001011001011100100...') == "I am tired..."
