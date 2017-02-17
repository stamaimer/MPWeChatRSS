### MPWeChatRSS

1. create virtual environment

    - ./create_venv.sh
    
2. create mysql database named `mpwechatrss` with utf-8 encoding

3. `cp instance/config.py.example instance/config.py`

4. fill in the SECRET_KEY, BIND_URL, PROXY_URL, INFORM_URL, DB_USER, DB_PSWD, DB_HOST in `instance/config.py`

5. initial database(with venv activated)
    
    - python manage.py db init
    - python manage.py db migrate
    - python manage.py db upgrade
    
6. install rabbitmq

7. run celery(with venv activated)

    - celery -A celary.celery worker -B -l info

8. run server(with venv activated)

    - change SERVER_NAME in `config/__init__.py` (optional)

    - ./start.sh

