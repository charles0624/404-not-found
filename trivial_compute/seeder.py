#!/usr/bin/env python3

import json
import requests

from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import Iterable

DB_URL = "http://127.0.0.1:5000"


@dataclass
class DefaultQuestion:
    question: str
    answer: str
    category: str
    tags: Iterable[str] = ()


def seed_question_database() -> None:
    defaults = [
        DefaultQuestion(
            "What is the capital of France?",
            "Paris",
            "Geography",
            ("General", "Classic"),
        ),
        DefaultQuestion(
            "Which river runs through Egypt?", "Nile", "Geography", ("General",)
        ),
        DefaultQuestion(
            "Who was the first President of the United States?",
            "George Washington",
            "History",
            ("Beginner",),
        ),
        DefaultQuestion(
            "In what year did World War II end?",
            "1945",
            "History",
            ("General", "Classic"),
        ),
        DefaultQuestion(
            "What planet is known as the Red Planet?", "Mars", "Science", ("General",)
        ),
        DefaultQuestion(
            "What gas do plants primarily absorb for photosynthesis?",
            "Carbon Dioxide",
            "Science",
            ("Beginner",),
        ),
        DefaultQuestion(
            "How many players are on a standard soccer team on the field?",
            "11",
            "Sports",
            ("General",),
        ),
        DefaultQuestion(
            "Which country has won the most FIFA World Cups?",
            "Brazil",
            "Sports",
            ("Classic",),
        ),
        DefaultQuestion(
            "Who played Jack Dawson in Titanic?",
            "Leonardo DiCaprio",
            "Entertainment",
            ("General",),
        ),
        DefaultQuestion(
            "Which movie features the quote 'May the Force be with you'?",
            "Star Wars",
            "Entertainment",
            ("Classic",),
        ),
    ]

    for dq in defaults:
        data = {
            "category": dq.category,
            "question": dq.question,
            "answer": dq.answer,
            "deck_tags": dq.tags,
        }
        try:
            response = requests.post(f"{DB_URL}/create_question", data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(f"ERROR: {err}")
            break

        soup = BeautifulSoup(response.content, "html.parser")
        soup_paras_list = soup.find_all("p")
        print(soup_paras_list[0].text)

    print("✅ Seeded default questions.")


if __name__ == "__main__":
    seed_question_database()
    print("exiting")
