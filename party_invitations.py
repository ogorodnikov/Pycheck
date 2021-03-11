class Friend:
    invite = 'No party...'

    def __init__(self, name):
        self.name = name

    def show_invite(self):
        return self.invite


class Party:

    def __init__(self, place):
        self.place = place
        self.friends = set()

    def add_friend(self, friend):
        self.friends.add(friend)

    def del_friend(self, friend):
        self.friends.remove(friend)

    def send_invites(self, message):
        for friend in self.friends:
            friend.invite = f'{self.place}: {message}'


if __name__ == '__main__':
    party = Party("Midnight Pub")
    nick = Friend("Nick")
    john = Friend("John")
    lucy = Friend("Lucy")
    chuck = Friend("Chuck")

    party.add_friend(nick)
    party.add_friend(john)
    party.add_friend(lucy)
    party.send_invites("Friday, 9:00 PM")
    party.del_friend(nick)
    party.send_invites("Saturday, 10:00 AM")
    party.add_friend(chuck)

    assert john.show_invite() == "Midnight Pub: Saturday, 10:00 AM"
    assert lucy.show_invite() == "Midnight Pub: Saturday, 10:00 AM"
    assert nick.show_invite() == "Midnight Pub: Friday, 9:00 PM"
    assert chuck.show_invite() == "No party..."

    # mission tests

    party_1 = Party("Celentano")
    party_2 = Party("Itaka")
    party_3 = Party("Disneyland")
    john = Friend('John')
    rose = Friend('Rose')
    gabe = Friend('Gabe')
    party_1.add_friend(john)
    party_2.add_friend(rose)
    party_3.add_friend(gabe)
    party_1.send_invites('Friday, 18:45')
    party_2.send_invites('Saturday, 12:30')
    party_3.send_invites('Sunday, 10:00')
    assert rose.show_invite() == "Itaka: Saturday, 12:30"
