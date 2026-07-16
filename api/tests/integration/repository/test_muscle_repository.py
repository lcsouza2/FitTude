import pytest
from api.tests.factories.muscle_factory import MuscleFactory
from api.src.repository.muscle_repository import MuscleRepository
from api.src.models import MuscleGroup

@pytest.mark.asyncio
async def test_get_muscle_by_id_returns_muscle(mock_async_session):
    # Arrange
    repo = MuscleRepository(mock_async_session)

    muscle_group = MuscleGroup(
        user_id=1,
        group_name="Peito",
        deleted=False,
        deleted_at=None
    )
    mock_async_session.add(muscle_group)
    await mock_async_session.flush()

    muscle = MuscleFactory.build()
    muscle.group_name = muscle_group.group_name
    muscle.user_id = None

    mock_async_session.add(muscle)
    await mock_async_session.flush()

    # Act
    result = await repo.get_muscle_by_id(muscle.id)

    # Assert
    assert result is not None
    assert result.id == muscle.id
    assert result.muscle_name == muscle.muscle_name

@pytest.mark.asyncio
async def test_get_muscle_by_id_returns_none_for_nonexistent_muscle(mock_async_session):
    # Arrange
    repo = MuscleRepository(mock_async_session)

    # Act
    result = await repo.get_muscle_by_id(999)  # Assuming 999 is a non-existent ID

    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_get_all_muscles_returns_all_muscles(mock_async_session):
    # Arrange
    repo = MuscleRepository(mock_async_session)

    muscle_group = MuscleGroup(
        user_id=1,
        group_name="Peito",
        deleted=False,
        deleted_at=None
    )
    mock_async_session.add(muscle_group)
    await mock_async_session.flush()

    muscle1 = MuscleFactory.build()
    muscle1.group_name = muscle_group.group_name
    muscle1.user_id = None

    muscle2 = MuscleFactory.build()
    muscle2.group_name = muscle_group.group_name
    muscle2.user_id = None

    mock_async_session.add_all([muscle1, muscle2])
    await mock_async_session.flush()

    # Act
    result = await repo.get_all_muscles()

    # Assert
    assert len(result) == 2
    assert any(m.id == muscle1.id for m in result)
    assert any(m.id == muscle2.id for m in result)

@pytest.mark.asyncio
async def test_create_muscle_adds_muscle_to_database(mock_async_session):
    repo = MuscleRepository(mock_async_session)

    muscle = MuscleFactory.build()
    muscle.user_id = None  # Set user_id to None for testing

    muscle_group = MuscleGroup(
        user_id=1,
        group_name=muscle.group_name,
        deleted=False,
        deleted_at=None
    )
    mock_async_session.add(muscle_group)
    await mock_async_session.flush()

    muscle_as_dict = {
        "muscle_name": muscle.muscle_name,
        "group_name": muscle.group_name,
        "user_id": muscle.user_id,
        "deleted": muscle.deleted,
        "deleted_at": muscle.deleted_at,
        "created_at": muscle.created_at
    }

    # Act
    result = await repo.create_muscle(muscle_as_dict)

    # Assert
    assert result is not None
    assert result.muscle_name == muscle.muscle_name