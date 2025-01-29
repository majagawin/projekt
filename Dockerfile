FROM python:3.10

WORKDIR /projekt

COPY .. /projekt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]