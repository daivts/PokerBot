import random

from holdem_calc import holdem_calc, parallel_holdem_calc


async def hand(state):
    async with state.proxy() as data:
        hand_list = list(data.values())
        # print(hand_list)
        firts_card, second_card, deck = hand_list

        print(firts_card, second_card)


def generate_card(num):
    VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUITS = ["s", "h", "c", "d"]

    deck = [{"value": value, "suit": suit} for value in VALUES for suit in SUITS]
    random.shuffle(deck)

    def card_to_string(card):
        return f"{card['value']}{card['suit']}"

    return [card_to_string(deck.pop()) for _ in range(num)]


def generate_board(deck):
    if deck == 'Flop':
        return generate_card(3)
    elif deck == 'Tern':
        return generate_card(4)
    else:
        return generate_card(5)


print(holdem_calc.calculate(generate_board("Tern"), True, 1, None, ["As", "Ks"], True))
