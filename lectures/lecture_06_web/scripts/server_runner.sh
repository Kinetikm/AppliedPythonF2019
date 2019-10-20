#!/bin/bash

gunicorn --bind 0.0.0.0:8070 flask_tester:app --workers 4