FROM python:3.11

WORKDIR /app

ADD question_editor_interface_stub.py .
ADD Card.py .
ADD Deck.py .

RUN pip install pydantic

CMD [ "python", "question_editor_interface_stub.py" ]
