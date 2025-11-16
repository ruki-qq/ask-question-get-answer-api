import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.app import app
from core import Answer, Base, Question
from users import User, jwt_strategy
from .utils import create_answer, create_question, create_user, override_db_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Instance of event loop for the test session"""

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine() -> AsyncGenerator:
    """Test db engine"""

    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    @event.listens_for(engine.sync_engine, "connect")
    def set_sqlite_pragma(dbapi_conn, _):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator:
    """Test db session"""

    async_session_maker = async_sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        # Cleaning before each test

        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()

        yield session
        await session.close()


@pytest.fixture
async def client(
    test_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    """Test client with overridden database session"""

    override_db_session(test_session)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_session: AsyncSession) -> User:
    return await create_user("test@example.com", "test_password", test_session)


@pytest.fixture
async def test_user2(test_session: AsyncSession) -> User:
    return await create_user("test2@example.com", "test_password2", test_session)


@pytest.fixture
async def authenticated_client(
    test_session: AsyncSession, test_user: User
) -> AsyncGenerator[AsyncClient, None]:
    """Authenticated test client for test_user"""

    override_db_session(test_session)

    token = await jwt_strategy.write_token(test_user)

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"Authorization": f"Bearer {token}"},
    ) as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest.fixture
async def authenticated_client2(
    test_session: AsyncSession, test_user2: User
) -> AsyncGenerator[AsyncClient, None]:
    """Authenticated test client for test_user2"""

    override_db_session(test_session)

    token = await jwt_strategy.write_token(test_user2)

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={"Authorization": f"Bearer {token}"},
    ) as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest.fixture
async def test_question(test_session: AsyncSession) -> Question:
    return await create_question("What is FastAPI?", test_session)


@pytest.fixture
async def test_question2(test_session: AsyncSession) -> Question:
    return await create_question("What is pytest?", test_session)


@pytest.fixture
async def test_answer(
    test_session: AsyncSession,
    test_question: Question,
    test_user: User,
) -> Answer:
    answer = await create_answer(
        "FastAPI is a modern web framework",
        test_question.id,
        test_user.id,
        test_session,
    )
    return answer
