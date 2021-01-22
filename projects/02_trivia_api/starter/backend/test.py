import json
import unittest

from app import create_app
from db import db, Question, Category


class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config_test')
        self.client = self.app.test_client
        with self.app.app_context():
            self.db = db
            self.reset_db()
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.reset_db()

    def reset_db(self):
        self.db.session.close()
        self.db.drop_all()

    def test_get_questions_page_1(self):
        self.insert_test_data_to_database()

        res = self.client().get('/questions')

        data = json.loads(res.data)
        assert res.status_code == 200
        assert len(data["questions"]) == 10
        assert data["questions"][0] == {"id": 1, "question": "question", "answer": "answer", "category": "category",
                                        "difficulty": 2}
        assert data["questions"][9] == {"id": 10, "question": "question10", "answer": "answer", "category": "category",
                                        "difficulty": 2}
        assert data["total_questions"] == 12
        assert data["categories"] == {"1": "category", "2": "category2"}
        assert data["current_category"] is None

    def test_get_questions_page_2(self):
        self.insert_test_data_to_database()

        res = self.client().get('/questions', query_string={'page': '2'})

        data = json.loads(res.data)
        assert res.status_code == 200
        assert len(data["questions"]) == 2
        assert data["questions"][0] == {"id": 11, "question": "question11", "answer": "hello", "category": "category2",
                                        "difficulty": 5}
        assert data["questions"][1] == {"id": 12, "question": "questionX", "answer": "answerY", "category": "category",
                                        "difficulty": 2}
        assert data["total_questions"] == 12
        assert data["categories"] == {"1": "category", "2": "category2"}
        assert data["current_category"] is None

    def insert_test_data_to_database(self):
        with self.app.app_context():
            self.db.session.add(Question("question", "answer", "category", 2))
            self.db.session.add(Question("question2", "answer", "category", 2))
            self.db.session.add(Question("question3", "answer", "category", 2))
            self.db.session.add(Question("question4", "answer", "category2", 1))
            self.db.session.add(Question("question5", "answer", "category2", 2))
            self.db.session.add(Question("question6", "answer", "category", 2))
            self.db.session.add(Question("question7", "answer", "category", 1))
            self.db.session.add(Question("question8", "answer", "category2", 2))
            self.db.session.add(Question("question9", "answer", "category2", 5))
            self.db.session.add(Question("question10", "answer", "category", 2))
            self.db.session.add(Question("question11", "hello", "category2", 5))
            self.db.session.add(Question("questionX", "answerY", "category", 2))
            self.db.session.add(Category("category"))
            self.db.session.add(Category("category2"))
            self.db.session.commit()


if __name__ == "__main__":
    unittest.main()
