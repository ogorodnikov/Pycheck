from itertools import combinations

RANKS = "AKQJT98765432"
SUITS = "hdcs"

COMBINATION_SIZE = 5

HANDS = {'Straight flush': [((0, 1, 2, 3, 4), True)],
         'Four of a kind': [((0, 0, 0, 0), False)],
         'Full house': [((0, 0, 0), False), ((0, 0), False)],
         'Flush': [((None, None, None, None, None), True)],
         'Straight': [((0, 1, 2, 3, 4), False)],
         'Three of a kind': [((0, 0, 0), False)],
         'Two pair': [((0, 0), False), ((0, 0), False)],
         'One pair': [((0, 0), False)],
         'High card': [((None, None, None, None, None), False)]}


def cards_to_str(cards):
    for rank, suit in cards:
        yield RANKS[rank] + SUITS[suit]


def str_to_cards(card_string):
    for rank, suit in card_string.split(','):
        yield RANKS.index(rank), SUITS.index(suit)


def find_hand(card_strings, hand_patterns):

    unused_cards = sorted(str_to_cards(card_strings))
    found_cards = []

    for subhand_patterns in hand_patterns:
        rank_pattern, is_suits_must_match = subhand_patterns

        # print('Rank pattern:', rank_pattern)
        # print('Unused cards:', unused_cards)

        is_subhand_found = False
        for combination in combinations(unused_cards, len(rank_pattern)):

            ranks = [rank for rank, _ in combination]
            suits = [suit for _, suit in combination]

            rank_deltas = [rank - pattern if pattern is not None else None for rank, pattern in zip(ranks, rank_pattern)]

            is_ranks_pass = len(set(rank_deltas)) == 1
            is_same_suits = len(set(suits)) == 1
            is_suits_pass = is_same_suits or not is_suits_must_match

            # print('    Rank pattern:', rank_pattern)
            # print('    Ranks:       ', ranks)
            # print('    Rank deltas: ', rank_deltas)
            # print('    Suits:       ', suits)
            # print('    Ranks pass:  ', is_ranks_pass)
            # print('    Suits pass:  ', is_suits_pass)
            # print()

            if is_ranks_pass and is_suits_pass:
                unused_cards = sorted(set(unused_cards) - set(combination))
                found_cards.extend(combination)
                is_subhand_found = True
                break

        if not is_subhand_found:
            return None

    kickers_len = COMBINATION_SIZE - len(found_cards)
    kickers = unused_cards[:kickers_len]

    # print('Unused cards: ', unused_cards)
    # print('Kickers:      ', kickers)
    # print()

    found_combination = ','.join(cards_to_str(sorted(found_cards + kickers)))
    return found_combination


def texas_referee(cards_str):
    print('Cards str:', cards_str)

    for hand_name, hand_patterns in HANDS.items():
        print('Checking hand:', hand_name)
        found_cards_string = find_hand(cards_str, hand_patterns)

        if found_cards_string:
            print('Found cards string:', found_cards_string)
            print()
            return found_cards_string


if __name__ == '__main__':
    assert texas_referee("Kh,Qh,Ah,9s,2c,Th,Jh") == "Ah,Kh,Qh,Jh,Th", "High Straight Flush"
    assert texas_referee("Qd,Ad,9d,8d,Td,Jd,7d") == "Qd,Jd,Td,9d,8d", "Straight Flush"
    assert texas_referee("5c,7h,7d,9s,9c,8h,6d") == "9c,8h,7h,6d,5c", "Straight"
    assert texas_referee("Ts,2h,2d,3s,Td,3c,Th") == "Th,Td,Ts,3c,3s", "Full House"
    assert texas_referee("Jh,Js,9h,Jd,Th,8h,Td") == "Jh,Jd,Js,Th,Td", "Full House vs Flush"
    assert texas_referee("Js,Td,8d,9s,7d,2d,4d") == "Td,8d,7d,4d,2d", "Flush"
    assert texas_referee("Ts,2h,Tc,3s,Td,3c,Th") == "Th,Td,Tc,Ts,3c", "Four of Kind"
    assert texas_referee("Ks,9h,Th,Jh,Kd,Kh,8s") == "Kh,Kd,Ks,Jh,Th", "Three of Kind"
    assert texas_referee("2c,3s,4s,5s,7s,2d,7h") == "7h,7s,5s,2d,2c", "Two Pairs"
    assert texas_referee("2s,3s,4s,5s,2d,7h,8h") == "8h,7h,5s,2d,2s", "One Pair"
    assert texas_referee("3h,4h,Th,6s,Ad,Jc,2h") == "Ad,Jc,Th,6s,4h", "High Cards"
