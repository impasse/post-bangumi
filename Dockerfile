FROM python:3.11-bullseye

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R 1000.1000 /app

USER 1000:1000

CMD python main.py
