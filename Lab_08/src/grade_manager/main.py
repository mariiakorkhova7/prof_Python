import uvicorn
from .api import app

if __name__ == "__main__":
    uvicorn.run("src.grade_manager.main:app", host="127.0.0.1", port=8000, reload=True)