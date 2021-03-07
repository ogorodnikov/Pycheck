class Friends:

    def __init__(self, connections):
        self._connections = set()
        for connection in connections:
            self.add(connection)

    def add(self, connection: set) -> bool:
        is_new_connection = connection not in self._connections
        self._connections.add(frozenset(connection))
        return is_new_connection

    def remove(self, connection: set) -> bool:
        is_existing_connection = connection in self._connections
        self._connections.discard(frozenset(connection))
        return is_existing_connection

    def names(self) -> set:
        return {friend for connection in self._connections for friend in connection}

    def connected(self, name):
        raise NotImplementedError


if __name__ == '__main__':
    letter_friends = Friends(({"a", "b"}, {"b", "c"}, {"c", "a"}, {"a", "c"}))
    digit_friends = Friends([{"1", "2"}, {"3", "1"}])

    assert letter_friends.add({"c", "d"}) is True, "Add"
    assert letter_friends.add({"c", "d"}) is False, "Add again"
    assert letter_friends.remove({"c", "d"}) is True, "Remove"
    assert digit_friends.remove({"c", "d"}) is False, "Remove non exists"
    assert letter_friends.names() == {"a", "b", "c"}, "Names"
    # assert letter_friends.connected("d") == set(), "Non connected name"
    # assert letter_friends.connected("a") == {"b", "c"}, "Connected name"
