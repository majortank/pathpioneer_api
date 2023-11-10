# Path Pioneer API Documentation

## Endpoints

### 1. Retrieve a Random Question

- **Endpoint:** `GET /question/{level}`
- **Description:** Retrieve a random question based on the specified difficulty level.
- **Parameters:**
  - `level` (path parameter): The difficulty level of the question (e.g., "Beginner", "Intermediate").
- **Example Call:**
  ```bash
  curl https://www.pioneerapi.tangikuu.tech/question/Intermediate
  ```
- **Example Response:**
  ```json
  {
    "question": "What is the capital of France?",
    "options": ["Paris", "Berlin", "London", "Madrid"],
    "correct_answer": "Paris",
    "level": "Intermediate",
    "industry": "Geography",
    "focus_area": "European Capitals",
    "topic": "World Geography"
  }
  ```
- **Response:**
  - `200 OK`: Returns a JSON object containing a random question and its options.
  - `404 Not Found`: If no questions are found for the specified level.

### 2. Retrieve All Questions

- **Endpoint:** `GET /question/all/{level}`
- **Description:** Retrieve all questions based on the specified difficulty level.
- **Parameters:**
  - `level` (path parameter): The difficulty level of the questions (e.g., "Beginner", "Intermediate").
- **Example Call:**
  ```bash
  curl https://www.pioneerapi.tangikuu.tech/question/all/Beginner
  ```
- **Example Response:**
  ```json
  [
    {
      "question": "What is 2 + 2?",
      "options": ["2", "3", "4", "5"],
      "correct_answer": "4",
      "level": "Beginner",
      "industry": "Mathematics",
      "focus_area": "Basic Arithmetic",
      "topic": "Math Basics"
    },
    {
      "question": "Who painted the Mona Lisa?",
      "options": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Claude Monet"],
      "correct_answer": "Leonardo da Vinci",
      "level": "Beginner",
      "industry": "Art History",
      "focus_area": "Famous Paintings",
      "topic": "Art"
    }
  ]
  ```
- **Response:**
  - `200 OK`: Returns a JSON array containing all questions and their options for the specified level.
  - `404 Not Found`: If no questions are found for the specified level.

### 3. Create Questions

- **Endpoint:** `POST /question/create/`
- **Description:** Create one or multiple questions.
- **Request Body:** JSON array containing question objects (See QuestionCreate model for object structure).
- **Example Call using Postman:**
  1. Open Postman.
  2. Set the request type to `POST`.
  3. Enter the URL: `https://www.pioneerapi.tangikuu.tech/question/create/`.
  4. Set the headers:
      - `Content-Type: application/json`
  5. Enter the request body as raw JSON:
      ```json
      [
        {
          "question": "What is the capital of Spain?",
          "options": ["Madrid", "Barcelona", "Seville", "Valencia"],
          "correct_answer": "Madrid",
          "level": "Intermediate",
          "industry": "Geography",
          "focus_area": "European Capitals",
          "topic": "World Geography"
        }
      ]
      ```
- **Example Response:**
  ```json
  {
    "message": "Questions created successfully",
    "question_ids": [123]
  }
  ```
- **Response:**
  - `200 OK`: Returns a JSON object indicating the successful creation of questions, including their unique IDs.
  - `422 Unprocessable Entity`: If the request body is not valid or the creation fails.

### 4. Update Question

- **Endpoint:** `PUT /question/update/{question_id}`
- **Description:** Update an existing question based on its ID.
- **Parameters:**
  - `question_id` (path parameter): The unique ID of the question to update.
- **Request Body:** JSON object containing updated question details (See QuestionCreate model for object structure).
- **Example Call using Postman:**
  1. Open Postman.
  2. Set the request type to `PUT`.
  3. Enter the URL: `https://www.pioneerapi.tangikuu.tech/question/update/123`.
  4. Set the headers:
      - `Content-Type: application/json`
  5. Enter the request body as raw JSON:
      ```json
      {
        "question": "What is the capital of Italy?",
        "options": ["Rome", "Milan", "Florence", "Venice"],
        "correct_answer": "Rome",
        "level": "Intermediate",
        "industry": "Geography",
        "focus_area": "European Capitals",
        "topic": "World Geography"
      }
      ```
- **Example Response:**
  ```json
  {
    "message": "Question updated successfully"
  }
  ```
- **Response:**
  - `200 OK`: Returns a JSON object confirming the successful update of the question.
  - `422 Unprocessable Entity`: If the request body is not valid or the update fails.

### 5. Delete Question

- **Endpoint:** `DELETE /question/delete/{question_id}`
- **Description:** Delete an existing question based on its ID.
- **Parameters:**
  - `question_id` (path parameter): The unique ID of the question to delete.
- **Example Call using Postman:**
  1. Open Postman.
  2. Set the request type to `DELETE`.
  3. Enter the URL: `https://www.pioneerapi.tangikuu.tech/question/delete/123`.
- **Example Response:**
  ```json
  {
    "message": "Question deleted successfully"
  }
  ```
- **Response:**
  - `200 OK`: Returns a JSON object confirming the successful deletion of the question.
  - `422 Unprocessable Entity`: If the deletion fails or the specified question ID does not exist.

## Models

### QuestionCreate Model

- `question` (str): The text of the question.
- `options` (List[str]): List of strings representing options for the question.
- `correct_answer` (str): The correct answer for the question.
- `level` (str): The difficulty level of the question (e.g., "Beginner", "Intermediate").
- `industry` (str): The industry related to the question (e.g., "Information Technology").
- `focus_area` (str): The specific focus area related to the question (e.g., "Networking").
- `topic` (str): The topic of the question (e.g., "Intro to Networks").

### QuestionResponse Model

- `question` (str): The text of the question.
- `options` (List[str]): List of strings representing options for the question.

## API Base URL

[https://www.pioneerapi.tangikuu.tech/](https://www.pioneerapi.tangikuu.tech/)
