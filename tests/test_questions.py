from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core import Answer, Question


class TestListQuestions:
    """Tests for GET /api/questions/ endpoint"""

    async def test_list_questions_empty(self, client: AsyncClient):
        """Test listing questions when there are none"""

        response = await client.get("/api/questions/")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_questions_with_data(
        self, client: AsyncClient, test_question: Question, test_question2: Question
    ):
        """Test listing questions with data"""

        response = await client.get("/api/questions/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("id" in item for item in data)
        assert all("text" in item for item in data)
        assert all("created_at" in item for item in data)
        assert any(item["text"] == test_question.text for item in data)
        assert any(item["text"] == test_question2.text for item in data)


class TestCreateQuestion:
    """Tests for POST /api/questions/ endpoint"""

    async def test_create_question_success(self, client: AsyncClient):
        text = "What is Python?"
        question_data = {"text": text}
        response = await client.post("/api/questions/", json=question_data)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "created_at" in data
        assert "text" in data
        assert data["text"] == text

    async def test_create_question_empty_text(self, client: AsyncClient):
        question_data = {"text": ""}
        response = await client.post("/api/questions/", json=question_data)
        assert response.status_code == 422

    async def test_create_question_missing_text(self, client: AsyncClient):
        """Test creating a question without text field"""

        question_data = {}
        response = await client.post("/api/questions/", json=question_data)
        assert response.status_code == 422


class TestGetQuestion:
    """Tests for GET /api/questions/{id} endpoint"""

    async def test_get_question_success(
        self, client: AsyncClient, test_question: Question
    ):
        """Test getting a question by ID"""

        response = await client.get(f"/api/questions/{test_question.id}")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "text" in data
        assert "created_at" in data
        assert "answers" in data
        assert data["id"] == test_question.id
        assert data["text"] == test_question.text
        assert isinstance(data["answers"], list)


class TestDeleteQuestion:
    """Tests for DELETE /api/questions/{id} endpoint"""

    async def test_delete_question_success(
        self,
        client: AsyncClient,
        test_question: Question,
        test_session: AsyncSession,
    ):
        """Test deleting a question successfully"""
        question_id = test_question.id

        response = await client.delete(f"/api/questions/{question_id}")
        assert response.status_code == 204

        test_session.expire_all()

        deleted_question = await test_session.get(Question, question_id)
        assert deleted_question is None

    async def test_delete_question_with_answers(
        self,
        client: AsyncClient,
        test_question: Question,
        test_answer: Answer,
        test_session: AsyncSession,
    ):
        """Test that deleting a question also deletes its answers"""

        question_id = test_question.id
        answer_id = test_answer.id

        answer = await test_session.get(Answer, answer_id)
        assert answer is not None

        response = await client.delete(f"/api/questions/{question_id}")
        assert response.status_code == 204

        test_session.expire_all()

        deleted_question = await test_session.get(Question, question_id)
        assert deleted_question is None

        deleted_answer = await test_session.get(Answer, answer_id)
        assert deleted_answer is None
