import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from src.connections import db_connection
from tests.factories.muscle_group_factory import MuscleGroupFactory

@pytest.fixture
def override_db(mock_async_session):
    async def _db_connection_override():
        yield mock_async_session

    app.dependency_overrides[db_connection] = _db_connection_override
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_all_muscle_groups_route(override_db, mock_async_session):
    # Arrange
    group = MuscleGroupFactory.build(group_name="Peito", deleted=False)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/muscle-groups")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["group_name"] == "Peito" for item in data)

@pytest.mark.asyncio
async def test_create_muscle_group_route_success(override_db):
    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/muscle-groups",
            json={"group_name": "Costas", "user_id": 1}
        )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["group_name"] == "Costas"
    assert data["user_id"] == 1
    assert data["deleted"] is False

@pytest.mark.asyncio
async def test_create_muscle_group_route_duplicate(override_db, mock_async_session):
    # Arrange
    group = MuscleGroupFactory.build(group_name="Bíceps", deleted=False)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/muscle-groups",
            json={"group_name": "Bíceps", "user_id": 1}
        )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Muscle group with this name already exists"

@pytest.mark.asyncio
async def test_get_muscle_group_by_name_route_success(override_db, mock_async_session):
    # Arrange
    group = MuscleGroupFactory.build(group_name="Tríceps", deleted=False)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/muscle-groups/Tríceps")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["group_name"] == "Tríceps"

@pytest.mark.asyncio
async def test_get_muscle_group_by_name_route_not_found(override_db):
    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/muscle-groups/Nonexistent")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Muscle group not found"

@pytest.mark.asyncio
async def test_update_muscle_group_route_success(override_db, mock_async_session):
    # Arrange
    group = MuscleGroupFactory.build(group_name="Ombros", user_id=1, deleted=False)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.put(
            "/muscle-groups/Ombros",
            json={"user_id": 2}
        )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["group_name"] == "Ombros"
    assert data["user_id"] == 2

@pytest.mark.asyncio
async def test_update_muscle_group_route_not_found(override_db):
    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.put(
            "/muscle-groups/Nonexistent",
            json={"user_id": 2}
        )

    # Assert
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_muscle_group_route_success(override_db, mock_async_session):
    # Arrange
    group = MuscleGroupFactory.build(group_name="Cardio", deleted=False)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/muscle-groups/Cardio")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["group_name"] == "Cardio"
    assert data["deleted"] is True

@pytest.mark.asyncio
async def test_delete_muscle_group_route_not_found(override_db):
    # Act
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/muscle-groups/Nonexistent")

    # Assert
    assert response.status_code == 404
