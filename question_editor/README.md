# Question Editor
This represents the component which allows users to interact with the questions in the database.

## Quickstart
Ensure the question database is already up!

Ensure the `DB_URL` variable in `question_editor.py` is correctly set to the database URL.

From a terminal:
```
# build the docker image
docker build -t question_editor .

# run the docker image as a container
docker run -it question_editor
```
