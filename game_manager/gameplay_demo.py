#!/usr/bin/env python3

from Board import Board
from Session import Session
from User import User

DB_URL="http://127.0.0.1:5000"

board = Board(1, DB_URL, name="demo_board")

user1 = User("adam", "aqua")
user2 = User("bethany", "black")
user3 = User("cathy", "crimson")
user4 = User("david", "dusky")
players = [user1, user2, user3, user4]
print(f"Players: {players}")

demo_sesh = Session(board, players)

def player_turn(player) -> bool:
    print("rolling the die...")
    # roll die
    spaces = demo_sesh.roll_die()
    print(f"rolled a {spaces}!")

    print("moving piece...")
    # move die roll
    player.set_coords("A", spaces)

    print("drawing card...")
    # draw card
    return demo_sesh.board.ask_question(player.get_coords())


for player in demo_sesh.players:
    # perform player turn, repeat if question is anwered correctly
    while True:
        print(f"{player.username}'s turn!")
        if not player_turn(player):
            break

print("thanks for playing!")
