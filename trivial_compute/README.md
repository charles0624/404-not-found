# 404: Trivial Compute

## Run the server
```
# from this directory:
python3 trivialpursuit.py
```

## Add questions to the database
**create_question:**\
    fill in the presented fields and click 'submit'

**update_question:**\
    specify the question id of the question you want to edit, and use the other fields to provide
    the information pertaining to that question to update. then click 'submit'.

## Additional database operations
**read_a_question:**\
    view the presented information

**read_all_questions:**\
    view the presented informtaion

**delete_a_question:**\
    specify the question id of the question you want to delete and click 'submit'.

see section 'Routes' below for further documentation

## Routes
```
# CREATE a question
http://127.0.0.1:5000/create_question

# READ a question
http://127.0.0.1:5000/question/<question_id>

# READ all questions
http://127.0.0.1:5000/questions

# UPDATE a question
http://127.0.0.1:5000/update_question

# DELETE a question
http://127.0.0.1:5000/delete_question
```

## Failures
No docker whatsoever at the present.  That is shifting right hardcore - I don't know how to get
sqlalchemy to create/use a docker container db.
