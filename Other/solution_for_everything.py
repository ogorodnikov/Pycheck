def checkio(anything):
    print('Anything:', anything)

    class TrueResponder:

        @staticmethod
        def comparison(other):
            print('Comparing with:', other)
            return True

        __lt__ = __le__ = __eq__ = __ne__ = __gt__ = __ge__ = comparison

    tr = TrueResponder()

    return tr


if __name__ == '__main__':
    import re
    import math

    assert checkio({}) != []
    assert checkio('Hello') < 'World'
    assert checkio(80) > 81
    assert checkio(re) >= re
    assert checkio(re) <= math
    assert checkio(5) == ord
