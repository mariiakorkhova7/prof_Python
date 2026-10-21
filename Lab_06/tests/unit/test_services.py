import pytest
from unittest.mock import Mock, AsyncMock
from grades.services import GradingService, AsyncReportService

def test_register_grade_success(sample_record):
    repo = Mock()
    repo.save.return_value = True
    notifier = Mock()
    
    service = GradingService(repo, notifier)
    service.register_grade(sample_record)
    
    repo.save.assert_called_once_with(sample_record)
    notifier.send.assert_called_once()

def test_register_grade_db_failure(sample_record):
    repo = Mock()
    repo.save.side_effect = ConnectionError("DB down")
    notifier = Mock()
    
    service = GradingService(repo, notifier)
    
    with pytest.raises(ConnectionError):
        service.register_grade(sample_record)
    notifier.send.assert_not_called()

@pytest.mark.asyncio
async def test_async_report_service():
    provider = AsyncMock()
    provider.fetch_report.return_value = {"status": "success"}
    
    service = AsyncReportService(provider)
    result = await service.generate(1)
    
    assert result == {"status": "success", "id": 1}
    provider.fetch_report.assert_awaited_once_with(1)