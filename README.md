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

Run celery worker:

```bash
celery -A selfstorage worker -l info
```
