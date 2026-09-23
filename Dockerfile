FROM python:3.13-slim

WORKDIR /workspace

COPY . .

RUN pip install --no-cache-dir pytest

CMD ["python", "-m", "pytest", "tasks/task_32", "-q"]