# Safe Passage

## Overview
This project implements a secure file-sharing system using Django and PostgreSQL, with two types of users: Operation User and Client User. Operation Users can upload files of specific types (pptx, docx, xlsx), while Client Users can sign up, verify their email, login, list all uploaded files, and download files using secure, encrypted URLs.

## Features
- *Operation User Actions*:
  - Signup
  - Login
  - Upload files (pptx, docx, xlsx only)

- *Client User Actions*:
  - Sign up (returns an encrypted URL)
  - Email verification
  - Login
  - List all uploaded files
  - Download files (secure, encrypted URL)

## Project Setup

### Prerequisites
- Python 3.x
- PostgreSQL
- Virtual environment (venv)

### Installation

1. *Clone the repository*:
    bash
    git clone <repository-url>
    cd <repository-directory>
    

2. *Set up virtual environment*:
    bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    

3. *Install dependencies*:
    bash
    pip install -r requirements.txt
    

4. *Configure PostgreSQL*:
    - Create a PostgreSQL database and user.
    - Update DATABASES settings in settings.py with your PostgreSQL configuration.

5. *Apply migrations*:
    bash
    python manage.py migrate
    

6. *Run the development server*:
    bash
    python manage.py runserver
    

### Project Structure

FileSharingSystem/                 
├── manage.py                
├── FileSharingSystem/       
│   ├── __init__.py
│   ├── settings.py          
│   ├── urls.py              
│   ├── wsgi.py              
│   └── asgi.py              
├── users/                   
│   ├── __init__.py
│   ├── middleware.py
│   ├── models.py            
│   ├── views.py             
│   ├── serializers.py       
│   ├── urls.py
│   ├── templates/               
│   │   ├── base1.html
│   │   ├── download_link.html
│   │   ├── home.html
│   │   ├── list_files.html
│   │   ├── login_client.html
│   │   ├── login_ops.html
│   │   ├── signup_client.html
│   │   ├── signup_ops.html
│   │   ├── upload_file.html
│   ├── static/               
│   │   ├── style.css
│   └── tests/
│       └── test_views.py        
├── files/                   
│   ├── __init__.py
│   ├── models.py            
│   ├── views.py             
│   ├── serializers.py       
│   ├── urls.py
│   └── tests/
│       └── test_views.py




### API Endpoints

#### Operation User
- *Sign Up*: /signup_ops/ (POST)
- *Login*: /login/_ops (POST)
- *Upload File*: /upload/_file (POST)

#### Client User
- *Sign Up*: /signup_client/ (POST)
- *Email Verify*: /users/verify-email/ (GET)
- *Login*: /login_client/ (POST)
- *List Files*: /list_files/ (GET)
- *Download File*: download-file/<int:pk>/ (GET)
- *Generate Download File*: generate-download-link/<int:pk>/ (GET)
- *Logout*: /logout(POST)


### Security Features
- Secure file upload and download mechanisms.
- Encrypted URLs for downloading files, accessible only by authorized Client Users.
- Email verification for Client Users.

## Frontend
- *HTML* and *CSS* templates are used for rendering the frontend.
- HTML files in the users/templates directory and CSS files in the users/static/css directory.

## Running Tests
To run the tests, use the following command:
bash
python manage.py users.test.test_views.py
