import re


class HackerLanguage:
    _message = ''

    @staticmethod
    def encode(message):

        def write_transparently(_, token):
            return token

        def write_ascii_code(_, token):
            return f'{ord(token):<07b}'

        scanner = re.Scanner([(r'\d|[^\w\s]', write_transparently),
                              (r'.', write_ascii_code)])

        tokens, unrecognised = scanner.scan(message)

        return ''.join(tokens)

    @staticmethod
    def decode(message):

        def read_transparently(_, token):
            return token

        def read_ascii_code(_, token):
            return chr(int(token.replace('1000000', '100000'), 2))

        scanner = re.Scanner([(r'[0|1]{7}', read_ascii_code),
                              (r'.', read_transparently)])

        tokens, unrecognised = scanner.scan(message)

        return ''.join(tokens)

    def write(self, text):
        self._message += text

    def delete(self, symbol_count):
        self._message = self._message[:-symbol_count]

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

    # mission tests

    message_3 = HackerLanguage()
    assert message_3.read('1001001100000011000011101101100000011101001101001111001011001011100100...') == "I am tired..."
