def flatten(dictionary):
    print('Input dictionary:', dictionary)

    output_dictionary = dict()
    for input_key, input_value in dictionary.items():
        if input_value == {}:
            print('    Empty dictionary:', input_value)
            output_dictionary[input_key] = ""
        elif isinstance(input_value, str):
            print('    String:', input_value)
            output_dictionary[input_key] = input_value
        elif isinstance(input_value, dict):
            print('    Dictionary:', input_value)
            for inner_key, inner_value in flatten(input_value).items():
                output_key = input_key + '/' + inner_key
                output_value = inner_value
                output_dictionary[output_key] = output_value

    print('Output dictionary:', output_dictionary)
    print()
    return output_dictionary


if __name__ == '__main__':

    assert flatten({"key": "value"}) == {"key": "value"}, "Simple"

    assert flatten(
        {"key": {"deeper": {"more": {"enough": "value"}}}}
    ) == {"key/deeper/more/enough": "value"}, "Nested"

    assert flatten({"empty": {}}) == {"empty": ""}, "Empty value"

    assert flatten({"name": {
                        "first": "One",
                        "last": "Drone"},
                    "job": "scout",
                    "recent": {},
                    "additional": {
                        "place": {
                            "zone": "1",
                            "cell": "2"}}}
    ) == {"name/first": "One",
          "name/last": "Drone",
          "job": "scout",
          "recent": "",
          "additional/place/zone": "1",
          "additional/place/cell": "2"}
