FROM python:3.7

WORKDIR /pavlovai_rest

RUN pip install fastapi fastapi-sqlalchemy pydantic psycopg2 uvicorn

COPY . /pavlovai_rest

EXPOSE 8000