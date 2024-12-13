import uvicorn
from src.core.config import Config
from src.main import app  # noqa: F401

if __name__ == "__main__":
    if Config.LOCAL == "True":
        uvicorn.run(
            "wsgi:app",
            host="127.0.0.1",
            port=4000,
            reload=True,
            reload_excludes=["tests/*"],
        )
    else:
        uvicorn.run("wsgi:app", host="0.0.0.0", port=4000, reload=True)
