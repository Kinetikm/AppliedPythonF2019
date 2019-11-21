# Create user and database:  
sudo -u postgres psql  
CREATE DATABASE flights;  
CREATE USER student WITH password 'student';  
GRANT ALL ON DATABASE flights TO student;  
psql -h localhost student flights -f flights.sql  

## Test:  
pytest --cov=./  manage.py data_processing.py auth.py test_hw_09_web.py  