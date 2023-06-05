FROM python:3.10.2-bullseye

WORKDIR /src/

COPY requirements.txt .
RUN pip install --proxy http://proxy.cafebazaar.org:3128 -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
