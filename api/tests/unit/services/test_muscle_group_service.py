import pytest
from unittest.mock import AsyncMock, MagicMock
from src.services.muscle_group_service import MuscleGroupService
from src.repository.muscle_group_repository import MuscleGroupRepository

@pytest.mark.asyncio
async def test_get_all_muscle_groups():
    # Arrange
    mock_repo = MagicMock(spec=MuscleGroupRepository)
    mock_repo.get_all_muscle_groups = AsyncMock(return_value=["group1", "group2"])
    service = MuscleGroupService(mock_repo)

    # Act
    result = await service.get_all_muscle_groups()

    # Assert
    mock_repo.get_all_muscle_groups.assert_called_once()
    assert result == ["group1", "group2"]

@pytest.mark.asyncio
async def test_create_muscle_group():
    # Arrange
    mock_repo = MagicMock(spec=MuscleGroupRepository)
    mock_repo.create_muscle_group = AsyncMock(return_value="new_group")
    service = MuscleGroupService(mock_repo)
    data = {"group_name": "Costas", "user_id": 1}

    # Act
    result = await service.create_muscle_group(data)

    # Assert
    mock_repo.create_muscle_group.assert_called_once_with(data)
    assert result == "new_group"

@pytest.mark.asyncio
async def test_get_muscle_group_by_name():
    # Arrange
    mock_repo = MagicMock(spec=MuscleGroupRepository)
    mock_repo.get_muscle_group_by_name = AsyncMock(return_value="group_found")
    service = MuscleGroupService(mock_repo)

    # Act
    result = await service.get_muscle_group_by_name("Ombros")

    # Assert
    mock_repo.get_muscle_group_by_name.assert_called_once_with("Ombros")
    assert result == "group_found"

@pytest.mark.asyncio
async def test_update_muscle_group():
    # Arrange
    mock_repo = MagicMock(spec=MuscleGroupRepository)
    mock_repo.update_muscle_group = AsyncMock(return_value="updated_group")
    service = MuscleGroupService(mock_repo)
    data = {"user_id": 2}

    # Act
    result = await service.update_muscle_group("Ombros", data)

    # Assert
    mock_repo.update_muscle_group.assert_called_once_with("Ombros", data)
    assert result == "updated_group"

@pytest.mark.asyncio
async def test_delete_muscle_group():
    # Arrange
    mock_repo = MagicMock(spec=MuscleGroupRepository)
    mock_repo.delete_muscle_group = AsyncMock(return_value="deleted_group")
    service = MuscleGroupService(mock_repo)

    # Act
    result = await service.delete_muscle_group("Ombros")

    # Assert
    mock_repo.delete_muscle_group.assert_called_once_with("Ombros")
    assert result == "deleted_group"
