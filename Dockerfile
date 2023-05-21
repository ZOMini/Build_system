FROM python:3.11.3-slim

COPY ./builds ./builds
WORKDIR /build_system
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY ./build_system .
CMD ["python", "-m", "main"]
# CMD ["python", "-m", "gunicorn", "main:app", "-k", "uvicorn.workers.UvicornH11Worker", "--bind", "0.0.0.0:8080", "--workers", "1", "--log-level", "info"]