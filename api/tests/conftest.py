import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from api.src.models.base_models import BaseOrmModel
from typing import AsyncGenerator
from api.src.config import SETTINGS

engine = create_async_engine(SETTINGS.POSTGRES_TEST_URL, echo=False)

@pytest.fixture(scope="session")
def event_loop():
    """
    Fixture que cria um loop de eventos para os testes. Necessário para testes assíncronos.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session", loop_scope="session", autouse=True)
async def setup_test_db():
    """
    Fixture que prepara o banco para os testes. Cria as tabelas antes de qualquer teste e as remove após todos os testes.
    """
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrmModel.metadata.drop_all)
        await conn.run_sync(BaseOrmModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrmModel.metadata.drop_all)
    await engine.dispose()

@pytest_asyncio.fixture
async def mock_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture que cria e injeta AsyncSessions para os testes. Cada teste recebe uma sessão isolada que é descartada após o teste.
    """
    async with AsyncSession(bind=engine) as session:
        transaction = await session.begin()
        yield session
        await transaction.rollback()