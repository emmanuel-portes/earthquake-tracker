FROM python:3.12-slim 

WORKDIR /usr/local

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app
COPY ingestion ./ingestion
COPY workers ./workers
COPY make_app.py ./

EXPOSE 5000

RUN useradd lex
USER lex

CMD ["flask", "--app", "app:create_app()", "run", "--host=0.0.0.0"]