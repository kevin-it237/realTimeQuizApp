# Setup the app

1. Install the dependencies
`pip3 install -r requirements.txt`

Set debug mode to FALSE for dev environment in `settings.py`
DEBUG = True

2. Apply migration
`python manage.py makemigrations`
`python manage.py migrate`

3. Running the application
`python manage.py runserver`