import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from model_mapper import map_questions_response, map_category, map_categories_response
from models import Question, Category, setup_db

app = Flask(__name__)
app.config.from_object('config')
CORS(app)
setup_db(app)


'''
@TODO:
Create an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
'''


@app.route('/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    current_category = None
    return get_questions_response(questions, current_category)


@app.route('/questions', methods=['POST'])
def get_questions_by_search_query():
    search_query = request.get_json().get("searchTerm")
    questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_query))).all()
    current_category = None
    return get_questions_response(questions, current_category)


@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify(map_categories_response(categories))


@app.route('/categories/<int:category_id>/questions', methods=['GET'])
def get_questions_of_category(category_id):
    questions = Question.query.filter(Question.category == category_id).all()
    current_category = map_category(Category.query.get(category_id))
    return get_questions_response(questions, current_category)


def get_questions_response(questions, current_category):
    current_page = request.args.get('page', 1, type=int)
    categories = Category.query.all()
    return jsonify(map_questions_response(questions, current_page, categories, current_category))


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


'''
@TODO:
Create an endpoint to handle GET requests
for all available categories.
'''

'''
@TODO:
Create an endpoint to handle GET requests for questions,
including pagination (every 10 questions).
This endpoint should return a list of questions,
number of total questions, current category, categories.

TEST: At this point, when you start the application
you should see questions and categories generated,
ten questions per page and pagination at the bottom of the screen for three pages.
Clicking on the page numbers should update the questions.
'''

'''
@TODO:
Create an endpoint to DELETE question using a question ID.

TEST: When you click the trash icon next to a question, the question will be removed.
This removal will persist in the database and when you refresh the page.
'''

'''
@TODO:
Create an endpoint to POST a new question,
which will require the question and answer text,
category, and difficulty score.

TEST: When you submit a question on the "Add" tab,
the form will clear and the question will appear at the end of the last page
of the questions list in the "List" tab.
'''

'''
@TODO:
Create a POST endpoint to get questions based on a search term.
It should return any questions for whom the search term
is a substring of the question.

TEST: Search by any phrase. The questions list will update to include
only question that include that string within their question.
Try using the word "title" to start.
'''

'''
@TODO:
Create a GET endpoint to get questions based on category.

TEST: In the "List" tab / main screen, clicking on one of the
categories in the left column will cause only questions of that
category to be shown.
'''

'''
@TODO:
Create a POST endpoint to get questions to play the quiz.
This endpoint should take category and previous question parameters
and return a random questions within the given category,
if provided, and that is not one of the previous questions.

TEST: In the "Play" tab, after a user selects "All" or a category,
one question at a time is displayed, the user is allowed to answer
and shown whether they were correct or not.
'''

'''
@TODO:
Create error handlers for all expected errors
including 404 and 422.
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
