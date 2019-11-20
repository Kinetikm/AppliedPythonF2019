FROM python:3.7
COPY . /SERVICE
WORKDIR /SERVICE
RUN pip install -r requirements.txt
CMD ['./main.py runserver --port 5000']