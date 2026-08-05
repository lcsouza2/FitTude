import pytest
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from src.repository.muscle_group_repository import MuscleGroupRepository
from tests.factories.muscle_group_factory import MuscleGroupFactory

@pytest.mark.asyncio
async def test_get_all_muscle_groups(mock_async_session):
    # Plan
    repo = MuscleGroupRepository(mock_async_session)

    groups = [
        MuscleGroupFactory.build(deleted=False),
        MuscleGroupFactory.build(deleted=True)  # Soft-deleted group
    ]

    for group in groups:
        mock_async_session.add(group)

    await mock_async_session.flush()

    # Act
    muscle_groups = await repo.get_all_muscle_groups()

    # Assert
    assert isinstance(muscle_groups, list)
    # Only non-deleted groups should be returned
    assert any(mg.group_name == groups[0].group_name for mg in muscle_groups)
    assert not any(mg.group_name == groups[1].group_name for mg in muscle_groups)

@pytest.mark.asyncio
async def test_create_muscle_group_success(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)
    group_data = {
        "user_id": 1,
        "group_name": "Costas",
        "deleted": False
    }

    # Act
    result = await repo.create_muscle_group(group_data)

    # Assert
    assert result is not None
    assert result.group_name == "Costas"
    assert result.user_id == 1
    assert result.deleted is False

@pytest.mark.asyncio
async def test_create_muscle_group_duplicate(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)
    group = MuscleGroupFactory.build(group_name="Bíceps")
    mock_async_session.add(group)
    await mock_async_session.flush()

    duplicate_data = {
        "user_id": 2,
        "group_name": "Bíceps",
        "deleted": False
    }

    # Act & Assert
    with pytest.raises(IntegrityError):
        await repo.create_muscle_group(duplicate_data)

@pytest.mark.asyncio
async def test_get_muscle_group_by_name_success(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)
    group = MuscleGroupFactory.build(group_name="Tríceps", deleted=False)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    result = await repo.get_muscle_group_by_name("Tríceps")

    # Assert
    assert result is not None
    assert result.group_name == "Tríceps"

@pytest.mark.asyncio
async def test_get_muscle_group_by_name_not_found(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)

    # Act
    result = await repo.get_muscle_group_by_name("Nonexistent")

    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_get_muscle_group_by_name_soft_deleted(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)
    group = MuscleGroupFactory.build(group_name="Perna", deleted=True)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    result = await repo.get_muscle_group_by_name("Perna")

    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_update_muscle_group_success(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)
    group = MuscleGroupFactory.build(group_name="Ombros", user_id=1, deleted=False)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    result = await repo.update_muscle_group("Ombros", {"user_id": 2})

    # Assert
    assert result is not None
    assert result.group_name == "Ombros"
    assert result.user_id == 2

@pytest.mark.asyncio
async def test_update_muscle_group_not_found(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)

    # Act
    result = await repo.update_muscle_group("Nonexistent", {"user_id": 2})

    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_delete_muscle_group_success(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)
    group = MuscleGroupFactory.build(group_name="Cardio", deleted=False)
    mock_async_session.add(group)
    await mock_async_session.flush()

    # Act
    result = await repo.delete_muscle_group("Cardio")

    # Assert
    assert result is not None
    assert result.group_name == "Cardio"
    assert result.deleted is True
    assert isinstance(result.deleted_at, datetime)

@pytest.mark.asyncio
async def test_delete_muscle_group_not_found(mock_async_session):
    # Arrange
    repo = MuscleGroupRepository(mock_async_session)

    # Act
    result = await repo.delete_muscle_group("Nonexistent")

    # Assert
    assert result is None
