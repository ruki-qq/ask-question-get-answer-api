from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core import Answer, Question
from users import User


class TestGetAnswer:
    """Tests for GET /api/answers/{id} endpoint"""

    async def test_get_answer_success(self, client: AsyncClient, test_answer: Answer):
        """Test getting an answer by ID"""

        response = await client.get(f"/api/answers/{test_answer.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_answer.id
        assert data["text"] == test_answer.text
        assert data["question_id"] == test_answer.question_id
        assert data["user_id"] == str(test_answer.user_id)
        assert "created_at" in data

    async def test_get_answer_not_found(self, client: AsyncClient):
        """Test getting a non-existent answer"""

        response = await client.get("/api/answers/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestDeleteAnswer:
    """Tests for DELETE /api/answers/{id} endpoint"""

    async def test_delete_answer_success(
        self,
        authenticated_client: AsyncClient,
        test_answer: Answer,
        test_session: AsyncSession,
    ):
        """Test deleting own answer successfully"""

        answer_id = test_answer.id

        response = await authenticated_client.delete(f"/api/answers/{answer_id}")
        assert response.status_code == 204

        test_session.expire_all()

        deleted_answer = await test_session.get(Answer, answer_id)
        assert deleted_answer is None

    async def test_delete_answer_requires_authentication(
        self, client: AsyncClient, test_answer: Answer
    ):
        response = await client.delete(f"/api/answers/{test_answer.id}")
        assert response.status_code == 401

    async def test_delete_answer_only_own(
        self,
        authenticated_client2: AsyncClient,
        test_answer: Answer,
        test_session: AsyncSession,
    ):
        """Test that user can only delete their own answers"""

        answer_id = test_answer.id

        response = await authenticated_client2.delete(f"/api/answers/{answer_id}")
        assert response.status_code == 403
        assert "own" in response.json()["detail"].lower()

        test_session.expire_all()

        answer_still_exists = await test_session.get(Answer, answer_id)
        assert answer_still_exists is not None

    async def test_delete_answer_not_found(self, authenticated_client: AsyncClient):
        """Test deleting a non-existent answer"""

        response = await authenticated_client.delete("/api/answers/99999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestAnswerRelationships:
    """Tests for answer relationships and cascading"""

    async def test_answer_has_user_id(
        self,
        client: AsyncClient,
        test_answer: Answer,
        test_user: User,
    ):
        """Test that answer has correct user_id"""

        response = await client.get(f"/api/answers/{test_answer.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == str(test_user.id)


class TestCreateAnswer:
    """Tests for POST /api/questions/{id}/answers/ endpoint"""

    async def test_create_answer_success(
        self,
        authenticated_client: AsyncClient,
        test_question: Question,
        test_user: User,
    ):
        text = "FastAPI is a web framework"
        answer_data = {"text": text}
        response = await authenticated_client.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "text" in data
        assert "question_id" in data
        assert "user_id" in data
        assert "created_at" in data
        assert data["text"] == text
        assert data["question_id"] == test_question.id
        assert data["user_id"] == str(test_user.id)

    async def test_create_answer_requires_authentication(
        self, client: AsyncClient, test_question: Question
    ):
        answer_data = {"text": "This should fail"}
        response = await client.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data
        )
        assert response.status_code == 401

    async def test_create_answer_uses_logged_in_user_id(
        self,
        authenticated_client: AsyncClient,
        authenticated_client2: AsyncClient,
        test_question: Question,
        test_user: User,
        test_user2: User,
    ):
        answer_data = {"text": "Answer from user 1"}
        response = await authenticated_client.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data
        )
        assert response.status_code == 201
        assert response.json()["user_id"] == str(test_user.id)

        answer_data2 = {"text": "Answer from user 2"}
        response2 = await authenticated_client2.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data2
        )
        assert response2.status_code == 201
        assert response2.json()["user_id"] == str(test_user2.id)

    async def test_create_answer_nonexistent_question(
        self, authenticated_client: AsyncClient
    ):
        """Test that cannot create answer to non-existent question"""

        answer_data = {"text": "This should fail"}
        response = await authenticated_client.post(
            "/api/questions/99999/answers", json=answer_data
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    async def test_create_multiple_answers_same_user(
        self,
        authenticated_client: AsyncClient,
        test_question: Question,
        test_user: User,
    ):
        """Test that same user can create multiple answers to one question"""

        answer_data1 = {"text": "First answer"}
        answer_data2 = {"text": "Second answer"}
        answer_data3 = {"text": "Third answer"}

        response1 = await authenticated_client.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data1
        )
        response2 = await authenticated_client.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data2
        )
        response3 = await authenticated_client.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data3
        )

        assert response1.status_code == 201
        assert response2.status_code == 201
        assert response3.status_code == 201
        assert response1.json()["user_id"] == str(test_user.id)
        assert response2.json()["user_id"] == str(test_user.id)
        assert response3.json()["user_id"] == str(test_user.id)
        assert response1.json()["question_id"] == test_question.id
        assert response2.json()["question_id"] == test_question.id
        assert response3.json()["question_id"] == test_question.id

    async def test_create_answer_empty_text(
        self, authenticated_client: AsyncClient, test_question: Question
    ):
        answer_data = {"text": ""}
        response = await authenticated_client.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data
        )
        assert response.status_code == 422

    async def test_create_answer_missing_text(
        self, authenticated_client: AsyncClient, test_question: Question
    ):
        """Test creating an answer without text field"""

        answer_data = {}
        response = await authenticated_client.post(
            f"/api/questions/{test_question.id}/answers", json=answer_data
        )
        assert response.status_code == 422
