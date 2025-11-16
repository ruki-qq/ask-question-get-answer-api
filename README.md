# ask-question-get-answer-api

This is an API for QA service.
It's currently supports listing, posting, getting and deleting questions and same for answers.
Also it has logging, tests and a simple users system to post answers to questions.

## Usage

### Clone repo
```bash
git clone https://github.com/ruki-qq/ask-question-get-answer-api.git
cd ask-question-get-answer-api
```

### Running locally
```bash
poetry install
cd src
python main.py
```

### Running via Docker-compose
```bash
docker-compose up
# you'll get db(PostgreSQL 16) + app containers
# all dependencies will install via pip from requirements.txt
# alembic migrations will apply automatically
```

After running you'll be able to create questions, users and answers(first log-in with created user)

## Testing

```bash
python -m pytest -vvv
python -m pytest --cov src # check tests coverage
```

## Available endpoints examples

### Request

GET /api/questions/

    curl -iH 'GET' \
    'http://localhost:8000/api/questions/' \
    -H 'accept: application/json'

### Response

    HTTP/1.1 200 OK
    date: Sun, 16 Nov 2025 21:33:51 GMT
    server: uvicorn
    content-length: 353
    content-type: application/json

    [
        {
            "text":"What is FastAPI?",
            "id":1,
            "created_at":"2025-11-16T12:51:27.536294Z"
        },
        {
            "text":"sosi gui",
            "id":3,
            "created_at":"2025-11-16T12:51:45.565318Z"
        }
    ]

### Request

GET /api/questions/{question_id}

    curl -iH 'GET' \
    'http://localhost:8000/api/questions/1' \
    -H 'accept: application/json'

### Response

    HTTP/1.1 200 OK
    date: Sun, 16 Nov 2025 21:39:37 GMT
    server: uvicorn
    content-length: 756
    content-type: application/json

    {
        "text":"What is FastAPI?",
        "id":1,
        "created_at":"2025-11-16T12:51:27.536294Z",
        "answers":[
            {
                "text":"FastAPI is asynchronous web framework",
                "id":9,
                "question_id":1,
                "user_id":"1f92cea0-9152-486d-aa29-e977c6c5c8cd",
                "created_at":"2025-11-16T12:54:01.521235Z"
            },
            {
                "text":"I don't know",
                "id":10,
                "question_id":1,
                "user_id":"cacb25a0-9152-454d-aa29-e977c674b8db",
                "created_at":"2025-11-16T12:54:03.512239Z"
            }
        ]
    }  

Look other endpoints at **/docs**
