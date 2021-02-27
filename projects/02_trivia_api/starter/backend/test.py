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
            self.reset_database()

    def test_get_questions_page_1(self):
        with self.app.app_context():
            self.insert_categories_to_database()
            self.insert_questions_to_database()

            res = self.client().get('/questions')

            data = json.loads(res.data)
            assert res.status_code == 200
            assert len(data['questions']) == 10
            assert data['questions'][0] == {'id': 1, 'question': 'question', 'answer': 'answer', 'category': 'category',
                                            'difficulty': 2}
            assert data['questions'][9] == {'id': 10, 'question': 'question10', 'answer': 'answer',
                                            'category': 'category', 'difficulty': 2}
            assert data['total_questions'] == 12
            assert data['categories'] == {'1': 'category', '2': 'category2'}
            assert data['current_category'] is None

    def test_get_questions_page_2(self):
        with self.app.app_context():
            self.insert_data_to_database()

            res = self.client().get('/questions', query_string={'page': '2'})

            data = json.loads(res.data)
            assert res.status_code == 200
            assert len(data['questions']) == 2
            assert data['questions'][0] == {'id': 11, 'question': 'question11', 'answer': 'hello',
                                            'category': 'category2', 'difficulty': 5}
            assert data['questions'][1] == {'id': 12, 'question': 'questionX', 'answer': 'answerY',
                                            'category': 'category', 'difficulty': 2}
            assert data['total_questions'] == 12
            assert data['categories'] == {'1': 'category', '2': 'category2'}
            assert data['current_category'] is None

    # valid case after user deletes all questions
    def test_get_questions_no_questions_with_categories(self):
        with self.app.app_context():
            self.insert_categories_to_database()

            res = self.client().get('/questions')

            data = json.loads(res.data)
            assert res.status_code == 200
            assert len(data['questions']) == 0
            assert data['total_questions'] == 0
            assert data['categories'] == {'1': 'category', '2': 'category2'}
            assert data['current_category'] is None

    def test_get_questions_no_questions_no_categories(self):
        with self.app.app_context():
            res = self.client().get('/questions')

            data = json.loads(res.data)
            assert res.status_code == 404
            assert data['error'] == 'resource not found'

    def test_post_questions_search(self):
        with self.app.app_context():
            self.insert_data_to_database()
            request_json = {'searchTerm': 'x'}

            res = self.client().post('/questions', json=request_json)

            data = json.loads(res.data)
            assert res.status_code == 200
            assert len(data['questions']) == 1
            assert data['questions'][0] == {'id': 12, 'question': 'questionX', 'answer': 'answerY',
                                            'category': 'category', 'difficulty': 2}
            assert data['total_questions'] == 1
            assert data['categories'] == {'1': 'category', '2': 'category2'}
            assert data['current_category'] is None

    def test_post_questions_search_no_results(self):
        with self.app.app_context():
            self.insert_data_to_database()
            request_json = {'searchTerm': 'y'}

            res = self.client().post('/questions', json=request_json)

            data = json.loads(res.data)
            assert res.status_code == 200
            assert len(data['questions']) == 0
            assert data['total_questions'] == 0
            assert data['categories'] == {'1': 'category', '2': 'category2'}
            assert data['current_category'] is None

    def test_post_questions_add_new_question(self):
        with self.app.app_context():
            self.insert_data_to_database()
            request_json = {
                'question': 'new question',
                'answer': 'new answer',
                'difficulty': 4,
                'category': 'category2'
            }

            res = self.client().post('/questions', json=request_json)

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data['success']
            question_in_db = self.db.session.query(Question).filter(Question.question == 'new question').all()[0]
            assert question_in_db.question == 'new question'
            assert question_in_db.answer == 'new answer'
            assert question_in_db.difficulty == 4
            assert question_in_db.category == 'category2'

    def test_post_questions_add_new_question_with_no_question(self):
        with self.app.app_context():
            self.insert_data_to_database()
            request_json = {
                'question': '',
                'answer': 'new answer',
                'difficulty': 4,
                'category': 'category2'
            }

            res = self.client().post('/questions', json=request_json)

            data = json.loads(res.data)
            assert res.status_code == 400
            assert data['error'] == 'bad request'

    def test_post_questions_add_new_question_with_no_answer(self):
        with self.app.app_context():
            self.insert_data_to_database()
            request_json = {
                'question': 'new question',
                'answer': '',
                'difficulty': 4,
                'category': 'category2'
            }

            res = self.client().post('/questions', json=request_json)

            data = json.loads(res.data)
            assert res.status_code == 400
            assert data['error'] == 'bad request'

    def test_delete_question(self):
        with self.app.app_context():
            self.insert_data_to_database()

            res = self.client().delete('/questions/1')

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data['success']
            questions = self.db.session.query(Question).all()
            assert len(questions) == 11

    def test_delete_question_does_not_exist(self):
        with self.app.app_context():
            self.insert_data_to_database()

            res = self.client().delete('/questions/100')

            data = json.loads(res.data)
            assert res.status_code == 422
            assert data['error'] == 'unprocessable'
            questions = self.db.session.query(Question).all()
            assert len(questions) == 12

    def test_get_categories(self):
        with self.app.app_context():
            self.insert_data_to_database()

            res = self.client().get('/categories')

            data = json.loads(res.data)
            assert res.status_code == 200
            assert data['categories'] == {'1': 'category', '2': 'category2'}

    def reset_database(self):
        with self.app.app_context():
            self.db.session.close()
            self.db.drop_all()
            self.db.create_all()

    def insert_data_to_database(self):
        with self.app.app_context():
            self.insert_categories_to_database()
            self.insert_questions_to_database()

    def insert_categories_to_database(self):
        with self.app.app_context():
            self.db.session.add(Category('category'))
            self.db.session.add(Category('category2'))
            self.db.session.commit()

    def insert_questions_to_database(self):
        with self.app.app_context():
            self.db.session.add(Question('question', 'answer', 'category', 2))
            self.db.session.add(Question('question2', 'answer', 'category', 2))
            self.db.session.add(Question('question3', 'answer', 'category', 2))
            self.db.session.add(Question('question4', 'answer', 'category2', 1))
            self.db.session.add(Question('question5', 'answer', 'category2', 2))
            self.db.session.add(Question('question6', 'answer', 'category', 2))
            self.db.session.add(Question('question7', 'answer', 'category', 1))
            self.db.session.add(Question('question8', 'answer', 'category2', 2))
            self.db.session.add(Question('question9', 'answer', 'category2', 5))
            self.db.session.add(Question('question10', 'answer', 'category', 2))
            self.db.session.add(Question('question11', 'hello', 'category2', 5))
            self.db.session.add(Question('questionX', 'answerY', 'category', 2))
            self.db.session.commit()


if __name__ == '__main__':
    unittest.main()
