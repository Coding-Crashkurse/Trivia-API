import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# function to only return 10 items
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    todos = [item.format() for item in selection]
    current_todos = todos[start:end]

    return current_todos


# function to return a single random element from an array
def create_random_question(arr):
    return arr[random.sample(range(0, len(arr)), 1)[0]]


def check_if_used(question, previous):
    return question.id in previous


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # make sure that api is available from different sources
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    """
    @TODO: 
    Create an endpoint to handle GET requests 
    for all available categories.
    """

    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()

        pre_formatted_categories = [category.format() for category in categories]
        formatted_categories = {}

        # unnest data
        for question in pre_formatted_categories:
            d = {question["id"]: question["type"]}
            formatted_categories.update(d)

        if len(formatted_categories) == 0:
            abort(404)

        return jsonify({"success": True, "categories": formatted_categories})

    """
    @TODO: 
    Create an endpoint to handle GET requests for questions, 
    including pagination (every 10 questions). 
    This endpoint should return a list of questions, 
    number of total questions, current category, categories. 

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    """

    @app.route("/questions")
    def get_questions():
        categories = Category.query.all()

        pre_formatted_categories = [category.format() for category in categories]
        formatted_categories = {}

        # unnest data
        for question in pre_formatted_categories:
            d = {question["id"]: question["type"]}
            formatted_categories.update(d)

        questions = Question.query.all()
        formatted_questions = paginate_questions(request, questions)

        if len(formatted_questions) == 0:
            abort(404)

        return jsonify(
            {
                "categories": formatted_categories,
                "questions": formatted_questions,
                "success": True,
                "total_questions": len(questions),
            }
        )

    """
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    """

    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        question_to_delete = Question.query.filter_by(id=id).one_or_none()

        try:
            if question_to_delete is None:
                abort(404)
            else:
                question_to_delete.delete()

            return jsonify({"success": True, "deleted_id": id})

        except:
            abort(422)

    """
    @TODO:
     
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  

    
    """

    """
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 

    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    """

    @app.route("/questions", methods=["POST"])
    def create_question():
        body = request.get_json()
        searchterm = body.get("searchTerm")
        if searchterm is not None:
            # case insensitive matching
            questions = Question.query.filter(
                Question.question.ilike(f"%{searchterm}%")
            ).all()
            if len(questions) == 0:
                abort(404)

            paginated_questions = paginate_questions(request, questions)

            return jsonify(
                {
                    "success": True,
                    "questions": paginated_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        else:
            new_question = body.get("question")
            new_answer = body.get("answer")
            new_difficulty = body.get("difficulty")
            new_category = body.get("category")

            if None in [new_question, new_answer, new_difficulty, new_category]:
                abort(422)

            try:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category,
                )
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        "success": True,
                        "created": question.id,
                        "question_created": question.question,
                        "questions": current_questions,
                        "total_questions": len(Question.query.all()),
                    }
                )

            except:
                abort(422)

    """
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    """

    @app.route("/categories/<int:id>/questions")
    def get_questions_per_category(id):

        category = Category.query.filter_by(id=id).one_or_none()

        if category is None:
            abort(404)

        questions = Question.query.filter_by(category=id).all()
        paginated_questions = paginate_questions(request, questions)

        return jsonify(
            {
                "success": True,
                "questions": paginated_questions,
                "total_questions": len(Question.query.all()),
                "current_category": category.type,
            }
        )

    """
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 


    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    """

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        body = request.get_json()

        category = body.get("quiz_category")

        # array with questions already asked
        previous_questions = body.get("previous_questions")

        if category["id"] == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter_by(category=category["id"]).all()

        question = create_random_question(questions)

        # use while loop to make sure the new question was not asked before
        while check_if_used(question, previous_questions):
            question = create_random_question(questions)

            if len(previous_questions) == len(questions):
                return jsonify({"success": True})

        return jsonify({"success": True, "question": question.format()})

    """
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "code": 404, "message": "not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "code": 422, "message": "unprocessable entity"}),
            422,
        )

    return app

