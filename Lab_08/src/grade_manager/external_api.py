import asyncio
import httpx

async def fetch_average_with_retry(
    client: httpx.AsyncClient, 
    semaphore: asyncio.Semaphore, 
    url: str, 
    student_id: int, 
    attempts: int = 3
) -> dict:
    async with semaphore:
        for attempt in range(1, attempts + 1):
            try:
                response = await client.get(url)
                response.raise_for_status()
                return {"student_id": student_id, "average": response.json()}
            except (httpx.RequestError, httpx.HTTPStatusError):
                if attempt == attempts:
                    return {"student_id": student_id, "average": None, "error": "Failed after retries"}
                await asyncio.sleep(attempt)

async def fetch_many_averages(base_url: str, student_ids: list[int]) -> list[dict]:
    semaphore = asyncio.Semaphore(5) # Обмеження паралелізму[cite: 43]
    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = [
            asyncio.create_task( # Використання Task[cite: 42]
                fetch_average_with_retry(
                    client, 
                    semaphore, 
                    f"{base_url}/students/{student_id}/average", 
                    student_id
                )
            )
            for student_id in student_ids
        ]
        
        try:
            # Використання gather та timeout[cite: 44, 46]
            return await asyncio.wait_for(asyncio.gather(*tasks), timeout=10.0)
        except asyncio.TimeoutError:
            return [{"error": "Global timeout reached"}]