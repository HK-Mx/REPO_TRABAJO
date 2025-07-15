FROM python:3.10.18-slim

RUN mkdir my_app
WORKDIR /my_app

COPY app.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt
CMD ["python","app.py"]
