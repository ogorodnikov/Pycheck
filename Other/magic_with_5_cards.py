RANKS = tuple('A 2 3 4 5 6 7 8 9 10 J Q K'.split())
SUITS = tuple('♣♦♥♠')


def card_to_tuple(card):
    rank, suit = card.split(' ')
    return RANKS.index(rank), SUITS.index(suit)


def tuple_to_card(tup):
    rank, suit = tup
    return RANKS[rank] + ' ' + SUITS[suit]


def bot(*cards, n=1):
    print('Bot')
    print('Cards:', cards)

    card_set = {card_to_tuple(card) for card in cards}

    ranks, suits = zip(*card_set)
    print('Ranks:', ranks)
    print('Suits:', suits)

    duplicate_suit = [suit for suit in suits if suits.count(suit) >= 2][0]
    print('Duplicate suit:', duplicate_suit, SUITS[duplicate_suit])

    card_a, card_b = [(rank, suit) for rank, suit in card_set if suit == duplicate_suit][:2]
    print('Card a:', card_a, tuple_to_card(card_a))
    print('Card b:', card_b, tuple_to_card(card_b))

    a_rank, a_suit = card_a
    b_rank, b_suit = card_b

    if a_rank > b_rank:
        clockwise_delta = len(RANKS) - a_rank + b_rank
    else:
        clockwise_delta = b_rank - a_rank
    counter_clockwise_delta = 13 - clockwise_delta
    print('Clockwise delta:', clockwise_delta)
    print('Counter clockwise delta:', counter_clockwise_delta)

    deltas = (clockwise_delta, counter_clockwise_delta)
    print('Deltas:', deltas)

    delta = min(deltas)
    print('Delta:', delta)

    if clockwise_delta > counter_clockwise_delta:
        hidden_card, visible_card = card_a, card_b
    else:
        hidden_card, visible_card = card_b, card_a
    print('Hidden card:', hidden_card, tuple_to_card(hidden_card))
    print('Visible card:', visible_card, tuple_to_card(visible_card))

    c1, c2, c3 = sorted(card_set - {hidden_card} - {visible_card})
    print('c1, c2, c3:', c1, c2, c3)
    print('c1, c2, c3:', *map(tuple_to_card, (c1, c2, c3)))

    if delta in (6, 5):
        f2 = c1
        if delta % 2:
            f3, f4 = c2, c3
        else:
            f3, f4 = c3, c2
    elif delta in (4, 3):
        f2 = c2
        if delta % 2:
            f3, f4 = c1, c3
        else:
            f3, f4 = c3, c1
    else:
        f2 = c3
        if delta % 2:
            f3, f4 = c1, c2
        else:
            f3, f4 = c2, c1

    bot_phrase = [f2, f3, f4]
    print('Bot phrase:', *bot_phrase)
    print('Bot phrase:', *map(tuple_to_card, bot_phrase))

    print('N:', n)
    visible_card_index = (n - 1) % (len(cards) - 1)
    print('Visible card index:', visible_card_index)

    bot_phrase.insert(visible_card_index, visible_card)
    print('Bot phrase with inserted visible card:', *bot_phrase)
    print('Bot phrase with inserted visible card:', *map(tuple_to_card, bot_phrase))

    bot_list = list(map(tuple_to_card, bot_phrase))
    print('Bot list:', bot_list)
    print()
    return bot_list


def magician(*cards, n=1):
    print('Magician')
    print('Cards:', cards)

    card_list = [card_to_tuple(card) for card in cards]
    print('Card list:', card_list)

    print('N:', n)
    visible_card_index = (n - 1) % len(cards)
    print('Visible card index:', visible_card_index)

    visible_card = card_list.pop(visible_card_index)
    print('Visible card:', visible_card)
    print('Visible card:', tuple_to_card(visible_card))

    visible_card_rank, visible_card_suit = visible_card
    hidden_card_suit = visible_card_suit
    print('Hidden card suit:', hidden_card_suit, SUITS[hidden_card_suit])

    print('Card list:', card_list)
    print('Card list:', *map(tuple_to_card, card_list))

    f2, f3, f4 = card_list
    print('f2, f3, f4:', f2, f3, f4)

    c1, c2, c3 = sorted(card_list)
    print('c1, c2, c3:', c1, c2, c3)

    if f2 == c1:
        if (f3, f4) == (c2, c3):
            delta = 5
        else:
            delta = 6
    elif f2 == c2:
        if (f3, f4) == (c1, c3):
            delta = 3
        else:
            delta = 4
    else:
        if (f3, f4) == (c1, c2):
            delta = 1
        else:
            delta = 2

    print('Delta:', delta)

    hidden_card_rank = (visible_card_rank + delta) % len(RANKS)
    print('Hidden card rank:', hidden_card_rank)

    hidden_card = (hidden_card_rank, hidden_card_suit)
    print('Hidden card:', hidden_card)

    hidden_card_string = tuple_to_card(hidden_card)
    print('Hidden card string:', hidden_card_string)
    print()
    return hidden_card_string


if __name__ == '__main__':
    assert list(bot('A ♥', '3 ♦', 'K ♠', 'Q ♣', 'J ♦')) == ['J ♦', 'A ♥', 'Q ♣', 'K ♠']
    assert magician('J ♦', 'A ♥', 'Q ♣', 'K ♠') == '3 ♦'

    assert list(bot('10 ♦', 'J ♣', 'Q ♠', 'K ♥', '7 ♦', n=2)) == ['Q ♠', '7 ♦', 'J ♣', 'K ♥']
    assert magician('Q ♠', '7 ♦', 'J ♣', 'K ♥', n=2) == '10 ♦'

    assert list(bot('K ♦', 'K ♠', '2 ♣', '8 ♠', '10 ♠', n=3)) in [['K ♠', 'K ♦', '8 ♠', '2 ♣'],
                                                                  ["8 ♠", "2 ♣", "10 ♠", "K ♦"]]

    assert list(bot('2 ♦', '9 ♥', 'K ♦', '4 ♥', '2 ♥', n=5)) in [["K ♦", "9 ♥", "4 ♥", "2 ♥"],
                                                                 ["4 ♥", "2 ♦", "2 ♥", "K ♦"],
                                                                 ["9 ♥", "2 ♦", "K ♦", "4 ♥"],
                                                                 ["2 ♥", "K ♦", "9 ♥", "2 ♦"]]

    assert magician('K ♥', 'J ♥', 'A ♥', '10 ♥', n=4) == "Q ♥"
    assert magician('9 ♥', '2 ♦', 'K ♦', '4 ♥', n=5) == "2 ♥"
