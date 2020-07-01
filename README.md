# Trivia Full Stack Project

This project is a a clone of the "trivia" game where users can create and answer questions. The project contains a pre built frontend built with the React library. The task was to create a REST-ful API with Flask, write a test suite and write an API documentation. The API provides the following functionalities:

1. Display all questions
2. Delete questions
3. Add questions
4. Search for questions and display questions which match the searchstring
5. Play the actual game

# How to get started

## Installing the dependencies

You need >= Python 3.6 since this project makes use of the f-string syntax. To run the frontend you have to use `npm` (node package manager).

### Frontend

If you want to run the frontend you have to use the following commands:

```
npm install
npm start
```

The frontend runs on port 3000. You reach reach it by using your favorite browser (please do not use IE ;-) ): http://localhost:3000

### Backend

The frontend will throw an warning message without a running backend.
Use `cd` into `/backend` and run the following directory to install the depencencies:<br>

```
pip install -r requirements.txt
```

After installing the dependencies you have to use setup your local environment you be able to start the API:

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

If you are on Linux or Mac, use `export` instead of `set`.
The API runs on http://localhost:5000

## API Testing

Do not use the production database for testing. Please use the following code for setup a test database with test data:

```
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## Endpoints with examples

### GET /categories

Get all categories:

Example: `curl http://127.0.0.1:5000/categories`

```
  {
      "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
      },
      "success": true
  }
```

GET /questions

Get paginated questions

Example: `curl http://127.0.0.1:5000/questions`

```
  {
      "categories": {
          "1": "Science",
          "2": "Art",
          "3": "Geography",
          "4": "History",
          "5": "Entertainment",
          "6": "Sports"
      },
      "questions": [
          {
              "answer": "Colorado, New Mexico, Arizona, Utah",
              "category": 3,
              "difficulty": 3,
              "id": 164,
              "question": "Which four states make up the 4 Corners region of the US?"
          },
          {
              "answer": "Muhammad Ali",
              "category": 4,
              "difficulty": 1,
              "id": 9,
              "question": "What boxer's original name is Cassius Clay?"
          },
          {
              "answer": "Apollo 13",
              "category": 5,
              "difficulty": 4,
              "id": 2,
              "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
          },
          {
              "answer": "Tom Cruise",
              "category": 5,
              "difficulty": 4,
              "id": 4,
              "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
          },
          {
              "answer": "Edward Scissorhands",
              "category": 5,
              "difficulty": 3,
              "id": 6,
              "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
          },
          {
              "answer": "Brazil",
              "category": 6,
              "difficulty": 3,
              "id": 10,
              "question": "Which is the only team to play in every soccer World Cup tournament?"
          },
          {
              "answer": "Uruguay",
              "category": 6,
              "difficulty": 4,
              "id": 11,
              "question": "Which country won the first ever soccer World Cup in 1930?"
          },
          {
              "answer": "George Washington Carver",
              "category": 4,
              "difficulty": 2,
              "id": 12,
              "question": "Who invented Peanut Butter?"
          },
          {
              "answer": "Lake Victoria",
              "category": 3,
              "difficulty": 2,
              "id": 13,
              "question": "What is the largest lake in Africa?"
          },
          {
              "answer": "The Palace of Versailles",
              "category": 3,
              "difficulty": 3,
              "id": 14,
              "question": "In which royal palace would you find the Hall of Mirrors?"
          }
      ],
      "success": true,
      "total_questions": 19
  }
```

### DELETE /questions/<<int:id>>

To delete questions by their id:

Example: `curl http://127.0.0.1:5000/questions/5 -X DELETE`

    {
      "deleted_id": 5,
      "success": true

}

### POST /questions

Option 1: Provide no searchterm: Will create a new questions with information in the request body. You will get back a paginated result

Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is the capital city of Bavavia, Germany?", "answer": "Munich", "difficulty": 2, "category": "3" }'`

```
{
    "created": 83,
    "question_created": "What is the capital city of Bavavia, Germany?",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?",
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?",
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?",
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?",
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?",
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?",
        },
    ],
    "success": true,
    "total_questions": 70,
}
```

Option 2: Provide a searchterm: You will get back a subset of all questions matching that searchterm

Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Tom Hanks"}'`

```
{"questions":[
    {"answer":"Apollo 13",
    "category":5,"difficulty":4,
    "id":2,
    "question":"What movie earned Tom Hanks his third straight Oscar omination, in 1996?"}
    ]"
```

### GET /categories/<<int:id>>/questions

Will return a subset of questions (only questions matching the requested category)

Example: `curl http://127.0.0.1:5000/categories/1/questions`

```
  {
      "current_category": "Science",
      "questions": [
          {
              "answer": "The Liver",
              "category": 1,
              "difficulty": 4,
              "id": 20,
              "question": "What is the heaviest organ in the human body?"
          },
          {
              "answer": "Alexander Fleming",
              "category": 1,
              "difficulty": 3,
              "id": 21,
              "question": "Who discovered penicillin?"
          },
          {
              "answer": "Blood",
              "category": 1,
              "difficulty": 4,
              "id": 22,
              "question": "Hematology is a branch of medicine involving the study of what?"
          }
      ],
      "success": true,
      "total_questions": 18
  }
```

### POST /quizzes

Allows you to play the actual game. You need to provde an array with previous questions in that category (check the /questions endpoint) as well as a question in the database.

Example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21], "quiz_category": {"type": "Science", "id": "1"}}'`

```
  {
      "question": {
          "answer": "Blood",
          "category": 1,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
      },
      "success": true
  }
```

### Error handling

If you make a great request which can not be resolved, the API will return an error.

Example: `curl http://127.0.0.1:5000/categories/1000/questions`

```
{
    "code":404,
    "message":"not found",
    "success":false
}
```

The following errors are returned:

- 400: "not found"
- 422: "unprocessable entity"
