#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
import requests

DB_URL = "http://127.0.0.1:5000"

# Crud: create single card
def prompt_create_card() -> None:
    print("\ncard creator!")
    print("input card creation data as a single string with fields seperated by a comma")
    print("(deck tags seperated by a colon) and in the order shown:")
    print("category,question,answer,decktag1:decktag2:decktag3")
    print("or 0 to return to main prompt")
    while True:
        card_data = input("> ").split(',')
        if len(card_data) != 4:
            try:
                if int(card_data[0]) == 0:
                    print("finished creating cards")
                    return
            except ValueError:
                pass
            print("invalid card creation data; try again")
            continue
        else:
            data = {"category": card_data[0], "question": card_data[1],
                    "answer": card_data[2], "deck_tags": card_data[3].strip().split(':')}
            try:
                response = requests.post(f"{DB_URL}/create_question", data=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                print(f"ERROR: {err}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            soup_paras_list = soup.find_all('p')
            print(soup_paras_list[0].text)

# cRud: read a single card
def prompt_read_card() -> None:
    print("\ncard reader!")
    print("input card 'question_id' on the line below, or 0 to return to main prompt")
    while True:
        card_data = input("> ")
        try:
            selection = int(card_data)
        except ValueError:
            print("invalid card question id; try again")
            continue

        if selection == 0:
            print("finished reading cards")
            return
        else:
            data = {"question_id": selection}
            try:
                response = requests.get(f"{DB_URL}/question/{selection}")
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                print(f"ERROR: {err}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            soup_paras_list = soup.find_all('p')
            print(soup_paras_list[0].text)

# cRud: read all cards
def prompt_read_cards() -> None:
    print("\ncards reader!")
    print("reading data from all cards...")
    try:
        response = requests.get(f"{DB_URL}/questions")
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"ERROR: {err}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    soup_paras_list = soup.find_all('p')

    for card_data in soup_paras_list:
        print(card_data.text)
    print("finished reading data from all cards")
    return

# crUd: update a single card
def prompt_update_card() -> None:
    print("\ncard updater!")
    print("input new card data on the row below, using the demonstrated ordering:")
    print("question_id,category,question,answer,decktag1:decktag2:decktag3")
    print("...or...")
    print("question_id,,,answer,decktag1:decktag3")
    print("...or 0 to return to main prompt")
    while True:
        card_data = input("> ").split(',')
        try:
            card_id = int(card_data[0])
        except ValueError:
            print("invalid question_id; try again")
            continue

        if card_id == 0:
            print("finished updating cards")
            return

        if len(card_data) != 5:
            print("invalid card update data; try again")
            continue
        else:
            data = dict()
            data["question_id"] = card_id
            if card_data[1]:
                data["category"] = card_data[1]
            if card_data[2]:
                data["question"] = card_data[2]
            if card_data[3]:
                data["answer"] = card_data[3]
            if card_data[4]:
                data["deck_tags"] = card_data[4].strip().split(':')

            if not data:
                print("no card data located; try again")
                continue

            try:
                response = requests.post(f"{DB_URL}/commit_update", data=data)
                response.raise_for_status()
            except requests.exceptions.RequestException as err:
                print(f"ERROR: {err}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            soup_paras_list = soup.find_all('p')
            print(soup_paras_list[0].text)


# cruD: delete a card
def prompt_delete_card() -> None:
    print("\ncard deleter!")
    print("input card 'question_id' on the line below, or 0 to return to main prompt")
    while True:
        card_data = input("> ")
        try:
            selection = int(card_data)
        except ValueError:
            print("invalid card question_id; try again")
            continue

        if selection == 0:
            print("finished deleting cards")
            return

        try:
            response = requests.post(f"{DB_URL}/commit_delete", data={"question_id": selection})
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f"ERROR: {err}")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        soup_paras_list = soup.find_all('p')
        print(soup_paras_list[0].text)



def prompt_welcome() -> int:
    print("question editor!")
    print("select:")
    print("1) create a card")
    print("2) read a card")
    print("3) read all cards")
    print("4) update a card")
    print("5) delete a card")
    print("0) exit")

    try:
        return int(input("> "))
    except:
        print("invalid input")
        return 0

while True:
    x: int = prompt_welcome()
    if x == 1:
        prompt_create_card()
    elif x == 2:
        prompt_read_card()
    elif x == 3:
        prompt_read_cards()
    elif x == 4:
        prompt_update_card()
    elif x == 5:
        prompt_delete_card()
    else:
        break
    print()

print("exiting")
