# Employee Management System

This is a Flask web application for managing employee information. It stores employee data in an AWS RDS MySQL database and employee images in an AWS S3 bucket.

## Setup Instructions

1. Update the `config.py` file with your AWS credentials:
   - customhost: Your RDS endpoint
   - customuser: Your RDS username
   - custompass: Your RDS password
   - customdb: Your database name
   - custombucket: Your S3 bucket name
   - customregion: Your AWS region

2. Install required dependencies: