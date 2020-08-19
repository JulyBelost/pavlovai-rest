FROM python:3.7-slim

WORKDIR /pavlovai_rest

RUN pip install fastapi fastapi-sqlalchemy pydantic psycopg2 uvicorn --system --dev

COPY . /pavlovai_rest

EXPOSE 8000