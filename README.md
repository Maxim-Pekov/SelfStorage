# SelfStorage

Demo project in scope of dvmn.org eductional course.

## How to install

Python3 should be already installed. 

Create virtual environment and activate it:

```bash 
python3 -m venv env 
source env/bin/activate
```

Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

Install Redis server and run it:

```bash
sudo apt install redis-server
redis-server
```

Run celery worker under your virtual environment:

```bash
celery -A mailapp worker -l info
```

Run migrations:

```bash
python manage.py migrate
```

Run Django server:

```bash
python manage.py runserver
```

## Set up for ENV variables

Create .env file in the root directory of the project and set up the following variables:

```bash
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

