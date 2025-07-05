#!/usr/bin/env python3

from Card import Card
from Deck import Deck

def prompt_edit_deck():
    print("\ndeck editor!")
    # function to print deck options in the database
    # print(database_read(db, deck_names))
    print("select deck to edit or 0 to return to main prompt")
    while True:
        deck_choice = input("> ")
        try:
            if int(deck_choice) == 0:
                print("returning")
                return
        except ValueError:
            print("invalid deck creation data; try again")
            continue

        # function to print cards in selected deck from the database in
        # the format 'card_id : card_question'
        # card_id = database_read(db, deck_names[deck_choice])
        # print(f"{card_id} : {database_read(db, card_id).question}")

def prompt_create_deck() -> None:
    print("\ndeck creator!")
    print("input deck creation data (ex: name,description)")
    print("or 0 to return to main prompt")
    while True:
        deck_data = input("> ").split(',')
        if len(deck_data) != 2:
            try:
                if int(deck_data[0]) == 0:
                    print("returning")
                    return
            except ValueError:
                pass
            print("invalid deck creation data; try again")
            continue
        else:
            new_deck = Deck(deck_data[0], deck_data[1])
            print(new_deck)
            # function to save the deck into the database
            # database_create(db, new_deck)


def prompt_welcome() -> int:
    print("question editor!")
    print("select:")
    print("1) create a new deck")
    print("2) edit an editing deck")
    print("0) exit")

    try:
        x = int(input("> "))
    except:
        print("invalid input")
        return 0
    return x

while True:
    x = prompt_welcome()
    if x == 1:
        prompt_create_deck()
    elif x == 2:
        prompt_edit_deck()
    else:
        break
    print()

print("exiting")
