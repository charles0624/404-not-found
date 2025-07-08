FROM python:3.11-slim

WORKDIR /app

ENV APP="question_editor.py"
ADD ${APP} .

RUN pip install --upgrade pip
RUN pip install requests

CMD python ${APP}
