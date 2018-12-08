# IoT Button Dashboard
This is a simple Django application that does two things:

    - Allows creation of Project entities in database so we can test Lambda functions

    - Monitors the network it's running on for Dash Button Presses.

In order to use the tool, virst create a virtualenv

```
virtualenv venv --python=python3
```

Then go ahead and activate it:

```
Mac:
source venv/bin/activate

Windows:
call venv\Scripts\activate
```

After that, go ahead and install all required packages by reading from the requirements.txt:

```
pip install -r requirements.txt
```

Finally, you should be able to run the server. But before you do so, make sure to make migrations so the database is prepped:

```
python manage.py makemigrations
python manage.py migrate
```

And run the server:

```
python manage.py runserver
```

You should find an ugly landing page at localhost:8000 now.

The general flow will be to add a Project Name and a Lambda Endpoint. Then, you should see a Test link, a Bind link, and a Delete link appear in the table below. Testing will emulate the Button press by calling the Lambda Endpoint directly from the Django app. Binding will make it so the Dash Button will trigger a specific endpoint, and we can test pressing the button now.