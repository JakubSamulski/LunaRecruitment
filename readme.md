# Luna Recruitment Task

## Setup

This project is fully dockerized and uses envirnoment variables to configure the application. To run the project you need to have docker installed on your machine.

1. Clone the repository
2. Create a ```.env``` file in the root directory, besides ```.env-template``` file. 
3. set environment variables in the ```.env``` file. You can use the ```.env-template``` file as a reference.
4. To run the app with docker run the following commands:
5. ```cd docker``` as there are docker files present
6. ```docker compose --env-file ..\.env up -d --build```
7. The app should be running on ```localhost:8000```


## API Documentation
 - The API documentation is available at ```localhost:8000/docs``` its swagger-ui documentation generated with drf-spectacular.

## Admin panel
- The admin panel is available at ```localhost:8000/admin```
- To create a superuser run the following command:
- ```docker exec -it backend python manage.py createsuperuser```

## Development
- To run the project in development mode you can run the following command:
- ```pip install -r requirements.txt``` to install the dependencies
- ```python manage.py migrate``` to run the migrations
- ```python maange.py runserver 8000``` or use some IDE like pycharm to run the app.
- There is a pre-commit hook setup with black and pylint to format and lint the code before commiting.
- To setup pre-commit hooks run the following command:
- ```pre-commit install```

## Testing
- To run the tests run the following command:
- ```python manage.py test Luna api_auth```

