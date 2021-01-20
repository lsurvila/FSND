

def map_questions_response(questions, questions_per_page, current_page, categories, current_category):
    return {
        'questions': map_questions(questions),
        'total_questions': len(questions),
        'categories': map_categories(categories),
        'current_category': current_category
    }


def map_questions(questions):
    data_questions = []
    for question in questions:
        data_questions.append(map_question(question))
    return data_questions


def map_question(question):
    return {
        'id': question.id,
        'question': question.question,
        'answer': question.answer,
        'category': question.category,
        'difficulty': question.difficulty
    }


def map_categories(categories):
    data_categories = {}
    for category in categories:
        map_category(category, data_categories)
    return data_categories


def map_category(category, data_categories):
    data_categories[category.id] = category.type.lower()
