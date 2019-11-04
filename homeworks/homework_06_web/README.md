# Create user and database:
sudo -u postgres psql  
CREATE DATABASE flights;  
CREATE USER student WITH password 'student';  
GRANT ALL ON DATABASE flights TO student;  
psql -h localhost student flights -f flights.sql  
