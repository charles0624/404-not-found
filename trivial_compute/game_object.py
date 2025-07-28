#!/usr/bin/env python3

from game_manager.Board import Board
from game_manager.Session import Session
from game_manager.User import User

COLORS = ["red", "orange", "yellow", "blue", "green", "violet"]

def get_player(player_name, player_color) -> User:
    return User(player_name, player_color)
