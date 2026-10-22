import uvicorn
from grade_service.config import get_settings

def main():
    settings = get_settings()
    uvicorn.run(
        "grade_service.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.environment == "development" else False
    )

if __name__ == "__main__":
    main()