# data_access_stub.py

class QuestionDataAccessStub:
    def get_mock_question(self):
        print("[Stub] Data Access Layer got request from Game Logic")
        return {"question": "What is 2 + 2?", "answer": "4"}

