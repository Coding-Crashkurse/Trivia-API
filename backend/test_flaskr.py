import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

         binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
             create all tables
            self.db.create_all()

        self.test_question = {
            "question": "What is the capital of bavaria in germany?",
            "answer": "Munich",
            "difficulty": 2,
            "category": 2,
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

     def test_categories(self):
         res = self.client().get("/categories")
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 200)
         self.assertTrue(len(data["categories"]))
         self.assertTrue(data["success"])

     def test_questions(self):
         res = self.client().get("/questions")
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 200)
         self.assertTrue(data["success"])
         self.assertTrue(len(data["categories"]))
         self.assertTrue(len(data["questions"]))

     def test_pagination_error(self):
         res = self.client().get("/questions?page=9999")
         data = json.loads(res.data)
         self.assertTrue(res.status_code, 404)
         self.assertTrue(data["message"], "not found")
         self.assertFalse(data["success"])

     def test_delete_question(self):
         new_question = self.test_question
         question = Question(
             question=new_question["question"],
             answer=new_question["answer"],
             difficulty=new_question["difficulty"],
             category=new_question["category"],
         )
         question.insert()

         all_questions = Question.query.all()
         new_question = Question.query.filter(
             Question.question == "What is the capital of bavaria in germany?"
         ).first()
         res = self.client().delete(f"/questions/{new_question.id}")
         data = json.loads(res.data)
         question_after_delete = Question.query.all()
         self.assertGreater(len(all_questions), len(question_after_delete))

     def test_search_question(self):
         res = self.client().post("/questions", json={"searchTerm": "what"})
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 200)
         self.assertTrue(data["success"])

     def test_search_question_error(self):
         res = self.client().post("/questions", json={"searchTerm": "aaaaaaaaaaa"})
         data = json.loads(res.data)
         self.assertEqual(res.status_code, 404)
         self.assertFalse(data["success"])

     def test_create_question(self):
         current_questions = Question.query.all()
         res = self.client().post("/questions", json=self.test_question)
         data = json.loads(res.data)
         new_questions = Question.query.all()
         self.assertGreater(len(new_questions), len(current_questions))
         self.assertEqual(res.status_code, 200)
         self.assertTrue(data["success"])

     def test_create_question_error(self):
         res = self.client().post("/questions", json={"test": "I produce an error"})
         data = json.loads(res.data)
         self.assertFalse(data["success"])
         self.assertEqual(res.status_code, 422)

    def test_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["current_category"], "Science")

    def test_questions_by_category_error(self):
        res = self.client().get("/categories/10/questions")
        data = json.loads(res.data)
        self.assertFalse(data["success"])
        self.assertEqual(res.status_code, 404)

    def test_quizzes(self):
        res = self.client().post(
            "/quizzes",
            json={
                "previous_questions": [20, 21],
                "quiz_category": {"type": "Science", "id": 1},
            },
        )
        data = json.loads(res.data)
        self.assertTrue(data["success"])
        self.assertEqual(data["question"]["category"], 1)

    def test_quizzes_error(self):
        res = self.client().post("/quizzes", json={})
        data = json.loads(res.data)
        res.assertEqual(res.status_code, 404)
        res.assertFalse(data["success"], False)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


 Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
