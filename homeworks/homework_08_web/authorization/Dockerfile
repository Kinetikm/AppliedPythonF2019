FROM python:3.7
COPY . /authorization	
WORKDIR /authorization
RUN pip install -r requirements.txt 
CMD ['./manage.py runserver --port 4000']

