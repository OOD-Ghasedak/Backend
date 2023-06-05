FROM python:3.10.2-bullseye

WORKDIR /src/

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "manage.py"]
