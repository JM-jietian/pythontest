from pathlib import Path
import os

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    os.system(
        r"%s\virtualenvs\py3_django\Scripts\activate"
        r"&& python %s\code\csrf\WebA\manage.py runserver 127.0.0.1:9000"
        % (BASE_DIR, BASE_DIR)
    )