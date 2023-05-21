FROM python:3.11.3-slim


WORKDIR /build_system
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY ./build_system .
WORKDIR /..
COPY ./builds ./builds
WORKDIR /build_system
CMD ["python", "-m", "main"]