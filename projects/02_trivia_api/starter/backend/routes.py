from flask import request, jsonify

from model_mapper import map_success, map_categories_response, map_category, map_questions_response, \
    map_quizzes_response
from db import Question, Category


def init_routes(app):
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()
        current_category = None
        return get_questions_response(questions, current_category)

    @app.route('/questions', methods=['POST'])
    def post_questions():
        search_query = request.get_json().get("searchTerm")
        if search_query:
            return get_questions_by_search_query(search_query)
        else:
            post_question()
            return jsonify(map_success())

    def post_question():
        request_json = request.get_json()
        question = request_json.get("question")
        answer = request_json.get("answer")
        difficulty = request_json.get("difficulty")
        category = request_json.get("category")
        question_db = Question(question, answer, difficulty, category)
        question_db.insert()

    def get_questions_by_search_query(search_query):
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_query))).all()
        current_category = None
        return get_questions_response(questions, current_category)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        question = Question.query.get(question_id)
        question.delete()
        return jsonify(map_success())

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        return jsonify(map_categories_response(categories))

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_of_category(category_id):
        questions = questions_of_category_query(category_id).all()
        current_category = map_category(Category.query.get(category_id))
        return get_questions_response(questions, current_category)

    def get_questions_response(questions, current_category):
        current_page = request.args.get('page', 1, type=int)
        categories = Category.query.all()
        return jsonify(map_questions_response(questions, current_page, categories, current_category))

    @app.route('/quizzes', methods=['POST'])
    def post_quizzes():
        request_json = request.get_json()
        previous_question_ids = request_json.get("previous_questions")
        quiz_category = request_json.get("quiz_category")
        available_questions = questions_of_category_query(quiz_category["id"]) \
            .filter(Question.id.notin_(previous_question_ids)).all()
        return jsonify(map_quizzes_response(available_questions))

    def questions_of_category_query(category_id):
        return Question.query if category_id == 0 else Question.query.filter(Question.category == category_id)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.errorhandler(400)
    def bad_request():
        return jsonify(error="bad request"), 400

    @app.errorhandler(404)
    def not_found():
        return jsonify(error="resource not found"), 404

    @app.errorhandler(405)
    def not_allowed():
        return jsonify(error="method not allowed"), 405

    @app.errorhandler(422)
    def unprocessable():
        return jsonify(error="unprocessable"), 422
