FROM python:3.7
COPY . /AUTH
WORKDIR /AUTH
RUN pip install -r requirements.txt
CMD ['./auth.py runserver --port 8000']