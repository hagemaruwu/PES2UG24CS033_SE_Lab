# Lab 7 - vending machine input checks

VALID_COINS = {5, 10, 25, 50, 100}
MAX_INPUT_LENGTH = 4096
MAX_COINS = 1000
MAX_NUMBER_DIGITS = 12


def clean_text(value):
    if not isinstance(value, str) or len(value) > MAX_INPUT_LENGTH:
        return None
    return value.strip()


def read_number(text):
    # Check this before int(), especially for very long numbers.
    if not 1 <= len(text) <= MAX_NUMBER_DIGITS:
        return None
    if not text.isascii() or not text.isdecimal():
        return None
    return int(text)


def parse_coins(coins_csv):
    text = clean_text(coins_csv)
    if text is None:
        return None
    if text == "":
        return []

    parts = text.split(",")
    if len(parts) > MAX_COINS:
        return None

    coins = []
    for part in parts:
        coin = read_number(part.strip())
        if coin not in VALID_COINS:
            return None
        coins.append(coin)
    return coins


def slot_position(code):
    text = clean_text(code)
    if text is None or len(text) < 2:
        return None

    letter = text[0]
    if not ("A" <= letter <= "Z" or "a" <= letter <= "z"):
        return None
    column = read_number(text[1:])
    if column is None or column < 1:
        return None

    row = ord(letter.upper()) - ord("A")
    return row, column - 1


def change_due(payment):
    text = clean_text(payment)
    if text is None:
        return None
    parts = text.split("/")
    if len(parts) != 2:
        return None

    paid = read_number(parts[0].strip())
    price = read_number(parts[1].strip())
    if paid is None or price is None or paid < price:
        return None

    change = paid - price
    # Don't lose the leftover amount by using // straight away.
    if change % 5 != 0:
        return None
    return str(change // 5) + " five-coins"


def main():
    try:
        print("==== Running parse_coins ====")
        user_input = input("Enter coin values as CSV (e.g. 5,10,25): ")
        result = parse_coins(user_input)
        if result is None:
            print("Invalid coin input.")
        else:
            print("Coins:", result)

        print("\n==== Running slot_position ====")
        user_input = input("Enter a slot code (e.g. B7): ")
        result = slot_position(user_input)
        if result is None:
            print("Invalid slot code.")
        else:
            print("Row and Column:", result)

        print("\n==== Running change_due ====")
        user_input = input("Enter paid/price (e.g. 200/150): ")
        result = change_due(user_input)
        if result is None:
            print("Invalid payment or unavailable exact change.")
        else:
            print("Change Due:", result)
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")


if __name__ == "__main__":
    main()
