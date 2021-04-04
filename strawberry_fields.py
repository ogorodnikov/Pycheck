def strawberryfield(a, b, c, d):
    # your code

    return 0


# These "asserts" are used for self-checking only and not for an auto-testing
if __name__ == '__main__':
    assert (strawberryfield(100, 100, 100, 100) == 90), "square"
    assert (strawberryfield(150, 100, 150, 100) == 90), "rectangle"
    assert (strawberryfield(150, 100, 50, 100) == 60), "trapezium"
    assert (strawberryfield(203, 123, 82, 117) == 60.8), "quadrilateral"

    print("Looks good so far! . . . How does 'Check' ?")
