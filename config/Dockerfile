FROM python:3.11

WORKDIR /app


COPY config/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY src ./src

CMD ["sh", "-c", "python -m src.infra.manage start_schema && python -m uvicorn src.controller.main:app --host 0.0.0.0 --port 8000"]
