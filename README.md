### MPWeChatRSS

1. create virtual environment

    - ./create_venv.sh
    
2. create mysql database named `mpwechatrss` with utf-8 encoding

3. fill in the DB_USER, DB_PSWD, DB_HOST in `instance/config.py`

4. initial database(with venv activated)
    
    - python manage.py db init
    - python manage.py db migrate
    - python manage.py db upgrade
    
5. install rabbitmq

6. run celery(with venv activated)

    - celery -A celary.celery worker -B -l info

7. run server(with venv activated)

    - ./start.sh

