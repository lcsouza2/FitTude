import pytest
from api.tests.factories.muscle_factory import MuscleFactory
from api.src.repository.muscle_repository import MuscleRepository
from api.src.models import MuscleGroup

@pytest.mark.asyncio()
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