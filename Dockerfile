# syntax=docker/dockerfile:1
FROM python:2.7

WORKDIR /python-flasky
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 7007
COPY . .

CMD ["python", "app.py"]