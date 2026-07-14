import pytest

from api.src.repository.muscle_group_repository import MuscleGroupRepository
from api.tests.factories.muscle_group_factory import MuscleGroupFactory

@pytest.mark.asyncio
async def test_get_all_muscle_groups(mock_async_session):
    # Plan
    repo = MuscleGroupRepository(mock_async_session)

    groups = [MuscleGroupFactory.build() for _ in range(2)]

    for group in groups:
        mock_async_session.add(group)

    await mock_async_session.flush()

    # Act
    muscle_groups = await repo.get_all_muscle_groups()

    # Assert
    assert isinstance(muscle_groups, list)
    for group in groups:
        assert any(mg.group_name == group.group_name for mg in muscle_groups)
