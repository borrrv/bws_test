import uvicorn

from src.main import app  # noqa: F401

if __name__ == "__main__":
    uvicorn.run("wsgi:app", host="127.0.0.1", port=3000, reload=True, reload_excludes=["tests/*"])