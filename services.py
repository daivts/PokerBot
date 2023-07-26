import random
from holdem_calc import holdem_calc


async def hand(state):
    async with state.proxy() as data:
        hand_list = list(data.values())
        first_card, second_card, deck = hand_list

        board = generate_board(deck, first_card, second_card)

        result = holdem_calc.calculate(
            None, True, 100, None, [first_card, second_card], False
        )
        print(result)

        return get_best_combination(result)


def get_best_combination(result):
    normalize = {k: v for k, v in result.items() if v is not None}
    best_combo = max(normalize, key=normalize.get)
    chance = normalize[best_combo] * 100
    return best_combo, chance


def generate_card(num, *args):
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    suits = ["s", "h", "c", "d"]

    deck = [
        {"value": value, "suit": suit} for value in values for suit in suits
    ]

    excluded_cards = [{"value": card[:-1], "suit": card[-1]} for card in args]

    for card in excluded_cards:
        if card and card in deck:
            deck.remove(card)

    random.shuffle(deck)

    def card_to_string(card):
        return f"{card['value']}{card['suit']}"

    return [card_to_string(deck.pop()) for _ in range(num)]


def generate_board(deck, first_card, second_card):
    if deck == 'Flop':
        return generate_card(3, first_card, second_card)
    elif deck == 'Tern':
        return generate_card(4, first_card, second_card)
    else:
        return generate_card(5, first_card, second_card)
