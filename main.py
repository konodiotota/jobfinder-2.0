from backend.config.app.engine import base, engine
import os
from backend.config.app.app import app

_JOBDIR= os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(_JOBDIR, "backend", "models")
API_DIR = os.path.join(_JOBDIR, "backend", "config", "api")

for _file in os.listdir(os.path.join(BACKEND_DIR, "company")):
    if _file.endswith('.py') and _file != "__init__.py":
        __import__(f"backend.models.company.{_file[:-3]}")

for _file in os.listdir(os.path.join(BACKEND_DIR,'shared')):
    if _file.endswith('.py') and _file != '__init__.py':
        __import__(f'backend.models.shared.{_file[:-3]}')

for _file in os.listdir(API_DIR):
    if _file.endswith('.py') and _file != "__init__.py":
        __import__(f'backend.config.api.{_file[:-3]}')

base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)
