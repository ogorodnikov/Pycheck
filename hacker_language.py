import re


class HackerLanguage:
    _message = ''

    # - all letters and whitespaces will be converted into their ASCII codes and than into the binary numbers.
    #
    # Except
    # the whitespaces - their binary form should be '1000000' not '100000'.
    #
    # - numbers, dates (in the 'dd.mm.yyyy'
    # format), time (in the 'hh:mm' format)
    #
    # and special signs ('.', ':', '!', '?', '@', '$', '%') won't be converted.

    @staticmethod
    def encode(message):

        print('Encode message:', message)

        def write_transparently(_, token):
            return token

        def write_ascii_code(_, token):
            return f'{ord(token):<07b}'

        scanner = re.Scanner([(r'\d|[^\w\s]', write_transparently),
                              (r'\w|\s', write_ascii_code)])

        tokens, unrecognised = scanner.scan(message)

        print('Tokens:', tokens)
        print('Unrecognised:', unrecognised)

        return ''.join(tokens)

    # @staticmethod
    # def encode(message):
    #     print('Encode message:', message)
    #
    #     encoded_message = ''
    #     for symbol in message:
    #         if symbol == ' ':
    #             binary = WHITESPACE_BINARY
    #         else:
    #             binary = f'{ord(symbol):b}'
    #         print('Binary:', binary)
    #         encoded_message += binary
    #     return encoded_message

    @staticmethod
    def decode(message):
        return message

    def write(self, text):
        self._message += text

    def delete(self, symbol_count):
        print('Before:')
        print('Self message:', self._message)

        self._message = self._message[:-symbol_count]

        print('After:')
        print('Self message:', self._message)

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
    # assert message_2.read("11001011101101110000111010011101100") == "email"
