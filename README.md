# ghasedak

## Project setup

### Production
change the settings in manage.py to production.
```
docker-compose -f docker-compose.production.yaml up --build
```
### Development
change the settings in manage.py to production.

then bring up postgres using docker-compose with below command:
```
docker-compose -f docker-compose.development.yaml up --build
```
then export mandatory variables:
```
export DB_ENGINE="django.db.backends.postgresql" SECRET_KEY="some-key" DB_NAME="ghasedak" DB_PASSWORD="Password" DB_USER="ghasedak" DB_PORT="5432" DB_HOST="localhost"
```
after that run django server locally using below command:
```
./manage.py runserver
```

### Test
change the settings in manage.py to test.

then run django tests using below command:
```
 docker-compose -f docker-compose.test.yaml up --build --exit-code-from ghasedak
```
after that it will jump out of containers when it finishes testing.