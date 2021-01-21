import random

QUESTIONS_PER_PAGE = 10


def map_questions_response(questions, current_page, categories, current_category):
    return {
        'questions': map_questions(questions, current_page),
        'total_questions': len(questions),
        'categories': map_categories(categories),
        'current_category': current_category
    }


def map_questions(questions, current_page):
    start = (current_page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    return [map_question(question) for question in questions[start:end]]


def map_question(question):
    return {
        'id': question.id,
        'question': question.question,
        'answer': question.answer,
        'category': question.category,
        'difficulty': question.difficulty
    }


def map_categories_response(categories):
    return {
        'categories': map_categories(categories)
    }


def map_categories(categories):
    return dict(map_category(category) for category in categories)


def map_category(category):
    return category.id, category.type.lower()


def map_success():
    return {
        'success': True
    }


def map_quizzes_response(available_questions):
    return {
        'question': map_question(random.choice(available_questions)) if available_questions else None
    }
