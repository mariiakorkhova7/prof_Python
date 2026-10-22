import pytest
from httpx import ASGITransport, AsyncClient
from src.grade_manager.api import app

@pytest.mark.asyncio
async def test_async_batch_average():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Створюємо тестові дані
        await client.post("/students", json={"first_name": "А", "last_name": "Б"})
        await client.post("/subjects", json={"name": "В"})
        await client.post("/grades", json={"student_id": 1, "subject_id": 1, "value": 85.5})
        
        # Перевіряємо агрегацію (тут ми тестуємо сам ендпоінт агрегації або базовий GET)
        response = await client.get("/students/1/average")
        assert response.status_code == 200
        assert response.json() == 85.5